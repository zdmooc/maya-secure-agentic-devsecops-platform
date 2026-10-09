"""Responsible AI BFI baseline regression: synthetic policies and attacks only."""
import json
import unittest
from dataclasses import replace
from pathlib import Path

from rai_bfi.guardrails import evaluate_text, validate_structured_answer
from rai_bfi.policy import Agent, Tool, PolicyEngine, mint_approval
from rai_bfi.registry import AgentRegistry

BASE = Path(__file__).resolve().parents[1]
KEY = b"synthetic-test-signing-key-32bytes--never-reuse"

class GuardrailTests(unittest.TestCase):
    def test_corpus(self):
        cases = json.loads((BASE / "redteam/rai-bfi-2026/attack_cases.json").read_text())["cases"]
        self.assertGreaterEqual(len(cases), 8)
        for case in cases:
            with self.subTest(attack=case["id"]):
                actual = evaluate_text(case["text"], boundary=case["boundary"])
                self.assertEqual(actual.code, case["expected"])
                self.assertEqual(actual.allowed, case["expected"] == "PASS")

    def test_strict_output_schema(self):
        good = {"status":"ANSWER", "answer":"Bounded response.", "evidence_refs":["repo:doc.md"]}
        self.assertTrue(validate_structured_answer(good).allowed)
        for bad in (
            "{broken", {"status":"ANSWER","answer":"ok","evidence_refs":[]},
            {"status":"EXECUTE","answer":"ok","evidence_refs":["repo:x"]},
            {"status":"ANSWER","answer":"password=abcd123456","evidence_refs":["repo:x"]},
            {"status":"ANSWER","answer":"ok","evidence_refs":["http://untrusted"]},
            {"status":"ABSTAIN","answer":"","evidence_refs":[],"run_shell":True},
        ):
            with self.subTest(candidate=bad):
                self.assertFalse(validate_structured_answer(bad).allowed)

    def test_limits(self):
        self.assertEqual(evaluate_text("x"*6001, boundary="user_input").code, "SIZE_LIMIT")
        self.assertEqual(evaluate_text("hello", boundary="unknown").code, "UNSUPPORTED_BOUNDARY")
        self.assertEqual(evaluate_text("a\x00b", boundary="user_input").code, "CONTROL_CHARACTER")
        self.assertEqual(evaluate_text(None, boundary="user_input").code, "EMPTY_OR_INVALID")

    def test_private_key_and_email(self):
        self.assertEqual(evaluate_text("-----BEGIN PRIVATE KEY-----", boundary="llm_output").code, "SENSITIVE_OUTPUT")
        self.assertEqual(evaluate_text("john.doe@example.test", boundary="tool_result").code, "SENSITIVE_OUTPUT")

class ToolPolicyTests(unittest.TestCase):
    def setUp(self):
        self.agent = Agent("payment-ops", "1.0.0", "synthetic-bfi", "architect-owner", "DEPLOYED",
                           frozenset({"mq.read", "payment.restart"}))
        self.tools = {
            "mq.read": Tool("mq.read", frozenset({"mq:read"})),
            "payment.restart": Tool("payment.restart", frozenset({"payment:manage"}), True),
            "admin.dump": Tool("admin.dump", frozenset({"admin"}))
        }
        self.engine = PolicyEngine(self.tools, KEY)

    def call(self, tool="mq.read", args=None, approval=None, **overrides):
        opts = dict(caller="ops-reader", authenticated=True, tenant="synthetic-bfi",
                    scopes=frozenset({"mq:read", "payment:manage"}), tool=tool,
                    arguments={"queue":"PAYMENT.REQUEST.Q"} if args is None else args,
                    approval=approval, now=100)
        opts.update(overrides)
        return self.engine.authorize(self.agent, **opts)

    def test_allow_bounded_read(self):
        self.assertEqual(self.call().code, "ALLOW")

    def test_reject_identity_and_tenant(self):
        self.assertEqual(self.call(authenticated=False).code, "UNAUTHENTICATED")
        self.assertEqual(self.call(tenant="another-tenant").code, "TENANT_MISMATCH")

    def test_reject_tools_and_scopes(self):
        self.assertEqual(self.call(tool="admin.dump").code, "TOOL_NOT_ALLOWED")
        self.assertEqual(self.call(tool="unknown").code, "TOOL_NOT_ALLOWED")
        self.assertEqual(self.call(scopes=frozenset()).code, "INSUFFICIENT_SCOPE")

    def test_agent_suspension(self):
        self.agent = replace(self.agent, state="SUSPENDED")
        self.assertEqual(self.call().code, "AGENT_NOT_ACTIVE")

    def ticket(self, args=None, nonce="nonce-1", expiry=200):
        return mint_approval(self.agent, self.tools["payment.restart"],
                             {"payment":"synthetic-123"} if args is None else args,
                             reviewer="security-reviewer", nonce=nonce, expires_at=expiry,
                             signing_key=KEY)

    def test_mutation_needs_review(self):
        self.assertEqual(self.call(tool="payment.restart", args={"payment":"synthetic-123"}).code,
                         "APPROVAL_REQUIRED")

    def test_valid_ticket_then_replay_denied(self):
        ticket = self.ticket()
        self.assertEqual(self.call(tool="payment.restart", args={"payment":"synthetic-123"}, approval=ticket).code,
                         "ALLOW_APPROVED")
        self.assertEqual(self.call(tool="payment.restart", args={"payment":"synthetic-123"}, approval=ticket).code,
                         "APPROVAL_REPLAY")

    def test_argument_escalation_rejected(self):
        ticket = self.ticket()
        self.assertEqual(self.call(tool="payment.restart", args={"payment":"real-client-payment"}, approval=ticket).code,
                         "APPROVAL_SCOPE_MISMATCH")

    def test_signature_tampering_rejected(self):
        ticket = replace(self.ticket(), signature="00"*32)
        self.assertEqual(self.call(tool="payment.restart", args={"payment":"synthetic-123"}, approval=ticket).code,
                         "BAD_APPROVAL_SIGNATURE")

    def test_expired_ticket_denied(self):
        ticket = self.ticket(expiry=99)
        self.assertEqual(self.call(tool="payment.restart", args={"payment":"synthetic-123"}, approval=ticket).code,
                         "APPROVAL_EXPIRED")

    def test_reviewer_must_differ(self):
        ticket = mint_approval(self.agent, self.tools["payment.restart"],
                               {"payment":"synthetic-123"}, reviewer="ops-reader", nonce="n2",
                               expires_at=200, signing_key=KEY)
        self.assertEqual(self.call(tool="payment.restart", args={"payment":"synthetic-123"}, approval=ticket).code,
                         "SEPARATION_OF_DUTIES")

    def test_version_change_invalidates_approval(self):
        ticket = self.ticket()
        self.agent = replace(self.agent, version="1.0.1")
        self.assertEqual(self.call(tool="payment.restart", args={"payment":"synthetic-123"}, approval=ticket).code,
                         "APPROVAL_SCOPE_MISMATCH")

    def test_cannot_mint_with_weak_key(self):
        with self.assertRaises(ValueError):
            mint_approval(self.agent, self.tools["payment.restart"], {}, reviewer="r", nonce="n",
                          expires_at=200, signing_key=b"weak")

    def test_reject_invalid_argument(self):
        self.assertEqual(self.call(args={"q":object()}).code, "INVALID_ARGUMENTS")

class RegistryTests(unittest.TestCase):
    def test_lifecycle_happy_path_and_deny(self):
        reg = AgentRegistry()
        agent = Agent("a", "1", "synthetic", "owner", "DESIGN", frozenset({"mq.read"}))
        reg.register(agent)
        for state in ("REGISTERED", "APPROVED", "DEPLOYED", "SUSPENDED", "RETIRED"):
            reg.transition("a", state, authorized_reviewer=True)
            self.assertEqual(reg.get("a").state, state)
        with self.assertRaises(ValueError):
            reg.transition("a", "DEPLOYED", authorized_reviewer=True)

    def test_no_unapproved_transition(self):
        reg = AgentRegistry()
        reg.register(Agent("a", "1", "synthetic", "owner", "DESIGN", frozenset()))
        with self.assertRaises(PermissionError):
            reg.transition("a", "REGISTERED", authorized_reviewer=False)
        with self.assertRaises(ValueError):
            reg.transition("a", "DEPLOYED", authorized_reviewer=True)

    def test_duplicate_registration(self):
        reg = AgentRegistry()
        agent = Agent("a", "1", "synthetic", "owner", "DESIGN", frozenset())
        reg.register(agent)
        with self.assertRaises(ValueError):
            reg.register(agent)

if __name__ == "__main__":
    unittest.main()
