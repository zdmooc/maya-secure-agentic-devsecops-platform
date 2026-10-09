"""Minimal in-memory agent lifecycle. Never claim service registry deployment."""
from __future__ import annotations
from dataclasses import replace
from .policy import Agent

TRANSITIONS = {
    "DESIGN": {"REGISTERED"},
    "REGISTERED": {"APPROVED", "RETIRED"},
    "APPROVED": {"DEPLOYED", "SUSPENDED", "RETIRED"},
    "DEPLOYED": {"SUSPENDED", "RETIRED"},
    "SUSPENDED": {"APPROVED", "RETIRED"},
    "RETIRED": set(),
}

class AgentRegistry:
    def __init__(self) -> None:
        self._records: dict[str, Agent] = {}

    def register(self, agent: Agent) -> Agent:
        if not agent.agent_id or not agent.owner or not agent.tenant or not agent.version:
            raise ValueError("owner, identity, tenant and version required")
        if agent.state != "DESIGN" or agent.agent_id in self._records:
            raise ValueError("new agents must start in DESIGN with unique id")
        self._records[agent.agent_id] = agent
        return agent

    def transition(self, agent_id: str, state: str, *, authorized_reviewer: bool) -> Agent:
        if not authorized_reviewer:
            raise PermissionError("trusted reviewer approval required")
        old = self._records[agent_id]
        if state not in TRANSITIONS[old.state]:
            raise ValueError(f"illegal lifecycle transition {old.state}->{state}")
        new = replace(old, state=state)
        self._records[agent_id] = new
        return new

    def get(self, agent_id: str) -> Agent:
        return self._records[agent_id]
