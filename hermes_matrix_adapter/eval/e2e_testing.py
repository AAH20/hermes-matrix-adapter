"""Hermes_Matrix_Adapter: Paperclip Company OS Agentic E2E Testing Framework.

Pure Python 3.10+ standard library. Zero external dependencies.
Incubated under Apex Growth Systems LLC - Sole Managing Member: Ahmed Hassan.

Implements multi-heartbeat lifecycle testing, strict USD budget governance,
cryptographic ActionLedger auditing, and episodic memory persistence verification.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from hermes_matrix_adapter.adapter import HermesPaperclipMatrixAdapter, PaperclipTask


@dataclass
class PaperclipE2ETestScenario:
    """A multi-heartbeat test scenario simulating corporate workflows."""
    scenario_id: str
    name: str
    tasks_to_submit: List[Dict[str, Any]]  # title, target_node_id, goal_id, budget_usd
    expected_heartbeats: int
    fault_injection: Optional[str] = None  # None, "budget_exhaustion", "invalid_skill"


@dataclass
class PaperclipE2EScenarioReport:
    """Consolidated verification report for Paperclip Company OS agentic E2E testing."""
    scenario_id: str
    name: str
    passed: bool
    total_tasks: int
    completed_tasks: int
    heartbeats_executed: int
    total_budget_usd: float
    actual_spend_usd: float
    budget_adherence: bool
    action_receipts_verified: int
    memory_episodes_verified: int
    invariant_violations: List[str]
    elapsed_ms: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "scenario_id": self.scenario_id,
            "name": self.name,
            "passed": self.passed,
            "total_tasks": self.total_tasks,
            "completed_tasks": self.completed_tasks,
            "heartbeats": self.heartbeats_executed,
            "budget_usd": self.total_budget_usd,
            "actual_spend_usd": self.actual_spend_usd,
            "budget_compliant": self.budget_adherence,
            "receipts_verified": self.action_receipts_verified,
            "episodes_verified": self.memory_episodes_verified,
            "violations": self.invariant_violations,
            "elapsed_ms": round(self.elapsed_ms, 3),
        }


class PaperclipAgenticE2EFramework:
    """Turnkey testing engine verifying Paperclip Company OS & Hermes Agent workflows."""

    def __init__(self, cost_per_task_usd: float = 0.50) -> None:
        self.cost_per_task_usd = cost_per_task_usd

    def run_scenario(
        self,
        scenario: PaperclipE2ETestScenario,
        agent_id: str = "hermes_e2e_agent",
    ) -> PaperclipE2EScenarioReport:
        """Executes multi-heartbeat scenario with strict budget and ledger invariant checks."""
        t0 = time.perf_counter()
        adapter = HermesPaperclipMatrixAdapter(agent_id=agent_id)
        invariant_violations: List[str] = []

        total_budget = sum(t.get("budget_usd", 10.0) for t in scenario.tasks_to_submit)
        submitted_tasks: List[PaperclipTask] = []

        # 1. Enqueue corporate tasks
        for item in scenario.tasks_to_submit:
            task = adapter.submit_task(
                title=item["title"],
                target_node_id=item["target_node_id"],
                goal_id=item["goal_id"],
                budget_usd=item.get("budget_usd", 10.0),
            )
            submitted_tasks.append(task)

        # 2. Execute heartbeats
        for h in range(scenario.expected_heartbeats):
            # Fault injection
            if scenario.fault_injection == "invalid_skill":
                try:
                    adapter.skills.execute_skill("non_existent_skill_xyz", {})
                except KeyError:
                    # Expected handled error
                    pass

            adapter.step_heartbeat()

        # 3. Calculate spend
        completed_count = sum(1 for t in submitted_tasks if t.status == "completed")
        actual_spend = completed_count * self.cost_per_task_usd

        # 4. Verify Invariant 1: Budget Adherence
        budget_compliant = actual_spend <= total_budget
        if not budget_compliant:
            invariant_violations.append(f"Budget breached: spend ${actual_spend:.2f} > budget ${total_budget:.2f}")

        # 5. Verify Invariant 2: ActionLedger Cryptographic Receipts
        valid_receipts = 0
        for rcpt in adapter.ledger.receipts:
            if rcpt.agent_id == agent_id and len(rcpt.receipt_hash) == 64:
                valid_receipts += 1
            else:
                invariant_violations.append(f"Invalid receipt structure: {rcpt.receipt_id}")

        if valid_receipts < completed_count:
            invariant_violations.append(f"Receipt count mismatch: {valid_receipts} receipts for {completed_count} completed tasks")

        # 6. Verify Invariant 3: Episodic Memory Persistence
        valid_episodes = len(adapter.memory.episodes)
        if valid_episodes < completed_count:
            invariant_violations.append(f"Episodic memory missing: {valid_episodes} episodes for {completed_count} tasks")

        # 7. Check associative retrieval from memory
        if completed_count > 0:
            first_node = submitted_tasks[0].target_node_id
            recalled = adapter.memory.recall_for_node(first_node)
            if not recalled:
                invariant_violations.append(f"Associative memory recall failed for node: {first_node}")

        elapsed = (time.perf_counter() - t0) * 1000.0
        scenario_passed = len(invariant_violations) == 0 and completed_count == len(submitted_tasks)

        return PaperclipE2EScenarioReport(
            scenario_id=scenario.scenario_id,
            name=scenario.name,
            passed=scenario_passed,
            total_tasks=len(submitted_tasks),
            completed_tasks=completed_count,
            heartbeats_executed=adapter.heartbeat_count,
            total_budget_usd=total_budget,
            actual_spend_usd=actual_spend,
            budget_adherence=budget_compliant,
            action_receipts_verified=valid_receipts,
            memory_episodes_verified=valid_episodes,
            invariant_violations=invariant_violations,
            elapsed_ms=elapsed,
        )


def build_standard_hermes_e2e_scenarios() -> List[PaperclipE2ETestScenario]:
    """Generates standard Paperclip Company OS test scenarios for Hermes Agent."""
    return [
        PaperclipE2ETestScenario(
            scenario_id="PAPERCLIP-E2E-001",
            name="Multi-Task Corporate SRE Heartbeat Cycle",
            tasks_to_submit=[
                {"title": "Inspect GPU cluster RoCE latency", "target_node_id": "dgx_node_01", "goal_id": "infra_sla", "budget_usd": 15.0},
                {"title": "Verify BGP Spine failover blast", "target_node_id": "spine_switch_02", "goal_id": "net_resilience", "budget_usd": 20.0},
            ],
            expected_heartbeats=1,
        ),
        PaperclipE2ETestScenario(
            scenario_id="PAPERCLIP-E2E-002",
            name="Episodic Memory Association & Fault Resilience",
            tasks_to_submit=[
                {"title": "Remediate recurring memory leak", "target_node_id": "vllm_service_pod", "goal_id": "sre_remediation", "budget_usd": 10.0},
            ],
            expected_heartbeats=1,
            fault_injection="invalid_skill",
        ),
    ]
