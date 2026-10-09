"""Fail-closed, synthetic agent/tool authorization contract.

Caller authentication, peer identity and reviewer authentication MUST be done
by an upstream IAM/gateway; this library cannot authenticate HTTP traffic.
HMAC tickets model action binding and replay refusal, not an enterprise PAM.
"""
from __future__ import annotations
import hashlib
import hmac
import json
import time
from dataclasses import dataclass, field

@dataclass(frozen=True)
class Agent:
    agent_id: str
    version: str
    tenant: str
    owner: str
    state: str
    allowed_tools: frozenset[str]
    max_autonomy: int = 1

@dataclass(frozen=True)
class Tool:
    name: str
    required_scopes: frozenset[str]
    requires_review: bool = False

@dataclass(frozen=True)
class Decision:
    allowed: bool
    code: str

@dataclass(frozen=True)
class ApprovalTicket:
    agent_id: str
    version: str
    tenant: str
    tool: str
    args_digest: str
    reviewer: str
    expires_at: int
    nonce: str
    signature: str

def args_digest(arguments: dict) -> str:
    data = json.dumps(arguments, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)
    return hashlib.sha256(data.encode()).hexdigest()

def _ticket_bytes(ticket: ApprovalTicket) -> bytes:
    data = [ticket.agent_id, ticket.version, ticket.tenant, ticket.tool,
            ticket.args_digest, ticket.reviewer, str(ticket.expires_at), ticket.nonce]
    return json.dumps(data, separators=(",", ":"), ensure_ascii=True).encode()

def mint_approval(agent: Agent, tool: Tool, arguments: dict, *, reviewer: str,
                  nonce: str, expires_at: int, signing_key: bytes) -> ApprovalTicket:
    """Only a trusted, authenticated approval service may call this in real use."""
    if not reviewer.strip() or not nonce.strip() or len(signing_key) < 32:
        raise ValueError("trusted reviewer, nonce and 256-bit signing key required")
    draft = ApprovalTicket(agent.agent_id, agent.version, agent.tenant, tool.name,
                           args_digest(arguments), reviewer, expires_at, nonce, "")
    sig = hmac.new(signing_key, _ticket_bytes(draft), hashlib.sha256).hexdigest()
    return ApprovalTicket(**{**draft.__dict__, "signature": sig})

@dataclass
class PolicyEngine:
    tools: dict[str, Tool]
    signing_key: bytes
    used_nonces: set[tuple[str, str]] = field(default_factory=set)

    def authorize(self, agent: Agent, *, caller: str, authenticated: bool,
                  tenant: str, scopes: frozenset[str], tool: str, arguments: dict,
                  approval: ApprovalTicket | None = None, now: int | None = None) -> Decision:
        # No model-provided identity, scope, approval flag or tool description is trusted.
        if authenticated is not True or not isinstance(caller, str) or not caller.strip():
            return Decision(False, "UNAUTHENTICATED")
        if agent.state != "DEPLOYED":
            return Decision(False, "AGENT_NOT_ACTIVE")
        if tenant != agent.tenant:
            return Decision(False, "TENANT_MISMATCH")
        if tool not in self.tools or tool not in agent.allowed_tools:
            return Decision(False, "TOOL_NOT_ALLOWED")
        policy = self.tools[tool]
        if not isinstance(scopes, frozenset) or not policy.required_scopes.issubset(scopes):
            return Decision(False, "INSUFFICIENT_SCOPE")
        if not isinstance(arguments, dict):
            return Decision(False, "INVALID_ARGUMENTS")
        try:
            digest = args_digest(arguments)
        except (TypeError, ValueError):
            return Decision(False, "INVALID_ARGUMENTS")
        if not policy.requires_review:
            return Decision(True, "ALLOW")
        if approval is None:
            return Decision(False, "APPROVAL_REQUIRED")
        if not isinstance(approval, ApprovalTicket):
            return Decision(False, "BAD_APPROVAL_TYPE")
        if not isinstance(approval.signature, str):
            return Decision(False, "BAD_APPROVAL_SIGNATURE")
        if len(self.signing_key) < 32:
            return Decision(False, "UNTRUSTED_APPROVAL_KEY")
        sig = hmac.new(self.signing_key, _ticket_bytes(approval), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(sig, approval.signature):
            return Decision(False, "BAD_APPROVAL_SIGNATURE")
        if (approval.agent_id != agent.agent_id or approval.version != agent.version
                or approval.tenant != tenant or approval.tool != tool or approval.args_digest != digest):
            return Decision(False, "APPROVAL_SCOPE_MISMATCH")
        if approval.reviewer == caller or not approval.reviewer:
            return Decision(False, "SEPARATION_OF_DUTIES")
        if approval.expires_at <= (int(time.time()) if now is None else now):
            return Decision(False, "APPROVAL_EXPIRED")
        nonce_key = (approval.agent_id, approval.nonce)
        if nonce_key in self.used_nonces:
            return Decision(False, "APPROVAL_REPLAY")
        self.used_nonces.add(nonce_key)
        return Decision(True, "ALLOW_APPROVED")
