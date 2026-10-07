"""Hermes_Matrix_Adapter: SWE Agent Evaluation Harness.

Pure Python 3.10+ standard library. Zero external dependencies.
Incubated under Apex Growth Systems LLC - Sole Managing Member: Ahmed Hassan.

Implements Nous Hermes function-calling SWE-bench evaluation, tool precision/recall
metrics, virtual file editing, and ActionLedger receipt auditing.
"""

from __future__ import annotations

import difflib
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple

from hermes_matrix_adapter.action_ledger import HermesActionLedger, HermesActionReceipt


@dataclass
class HermesSWETask:
    """An SWE problem instance for Hermes Agent."""
    task_id: str
    repo_name: str
    issue_text: str
    initial_files: Dict[str, str]
    test_suite: Dict[str, Callable[[Dict[str, str]], bool]]
    fail_to_pass: List[str]
    pass_to_pass: List[str]


@dataclass
class HermesToolCall:
    """A tool invocation step within Hermes SWE trajectory."""
    tool_name: str
    arguments: Dict[str, Any]
    output: Any
    latency_ms: float
    receipt_id: Optional[str] = None


@dataclass
class HermesSWETrajectoryResult:
    """Outcome and telemetry of Hermes agent solving an SWE task."""
    task_id: str
    resolved: bool
    tool_calls: List[HermesToolCall]
    total_turns: int
    tool_call_precision: float
    tool_call_recall: float
    receipt_count: int
    elapsed_ms: float
    estimated_cost_usd: float
    error_message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "resolved": self.resolved,
            "turns": self.total_turns,
            "tool_calls_count": len(self.tool_calls),
            "tool_call_precision_pct": round(self.tool_call_precision * 100, 2),
            "tool_call_recall_pct": round(self.tool_call_recall * 100, 2),
            "receipts_issued": self.receipt_count,
            "elapsed_ms": round(self.elapsed_ms, 3),
            "estimated_cost_usd": round(self.estimated_cost_usd, 4),
        }


class HermesSWEAgentHarness:
    """Turnkey SWE-bench evaluation harness customized for Hermes Agent."""

    def __init__(self, agent_id: str = "hermes_swe_evaluator") -> None:
        self.agent_id = agent_id
        self.ledger = HermesActionLedger(agent_id=agent_id)

    def run_swe_trajectory(
        self,
        task: HermesSWETask,
        agent_step_fn: Callable[[HermesSWETask, Dict[str, str], List[HermesToolCall]], Optional[Tuple[str, Dict[str, Any]]]],
        max_turns: int = 10,
    ) -> HermesSWETrajectoryResult:
        """Executes multi-turn Hermes tool interaction trajectory to solve an SWE issue."""
        t0 = time.perf_counter()
        virtual_files = {k: v for k, v in task.initial_files.items()}
        tool_history: List[HermesToolCall] = []
        valid_tool_calls = 0
        total_attempted_calls = 0

        # Run multi-turn loop
        for turn in range(max_turns):
            s_t0 = time.perf_counter()
            action = agent_step_fn(task, virtual_files, tool_history)
            if not action:
                # Agent completed / stopped
                break

            tool_name, arguments = action
            total_attempted_calls += 1
            tool_output = None
            rcpt_id = None

            # Execute tool in virtual environment
            if tool_name == "view_file":
                path = arguments.get("filepath", "")
                tool_output = virtual_files.get(path, "FileNotFoundError")
                valid_tool_calls += 1
            elif tool_name == "edit_file":
                path = arguments.get("filepath", "")
                old_str = arguments.get("target_content", "")
                new_str = arguments.get("replacement_content", "")
                if path in virtual_files and old_str in virtual_files[path]:
                    virtual_files[path] = virtual_files[path].replace(old_str, new_str, 1)
                    tool_output = "Edit applied successfully"
                    valid_tool_calls += 1
                else:
                    tool_output = "Target content not found in file"
            elif tool_name == "matrix_simulate_blast":
                target = arguments.get("target_node_id", "cluster_01")
                tool_output = {"target": target, "impact_score": 10.5, "status": "safe"}
                valid_tool_calls += 1
            else:
                tool_output = f"Unknown tool: {tool_name}"

            # Issue ActionLedger cryptographic receipt
            rcpt = self.ledger.issue_receipt(
                skill_name=f"hermes_swe_{tool_name}",
                target_node_id=arguments.get("filepath", arguments.get("target_node_id", "swe_workspace")),
            )
            rcpt_id = rcpt.receipt_id

            call_lat = (time.perf_counter() - s_t0) * 1000.0
            tool_history.append(HermesToolCall(
                tool_name=tool_name,
                arguments=arguments,
                output=tool_output,
                latency_ms=call_lat,
                receipt_id=rcpt_id,
            ))

        # Test verification
        f2p_passed = True
        for t_name in task.fail_to_pass:
            if t_name in task.test_suite:
                if not task.test_suite[t_name](virtual_files):
                    f2p_passed = False
                    break

        p2p_passed = True
        for t_name in task.pass_to_pass:
            if t_name in task.test_suite:
                if not task.test_suite[t_name](virtual_files):
                    p2p_passed = False
                    break

        resolved = f2p_passed and p2p_passed
        elapsed = (time.perf_counter() - t0) * 1000.0

        precision = valid_tool_calls / max(1, total_attempted_calls)
        recall = 1.0 if resolved else (valid_tool_calls / max(1, total_attempted_calls + 1))
        cost_est = (total_attempted_calls * 0.0015) + (len(str(virtual_files)) * 0.000001)

        return HermesSWETrajectoryResult(
            task_id=task.task_id,
            resolved=resolved,
            tool_calls=tool_history,
            total_turns=len(tool_history),
            tool_call_precision=precision,
            tool_call_recall=recall,
            receipt_count=len(tool_history),
            elapsed_ms=elapsed,
            estimated_cost_usd=cost_est,
        )


def build_hermes_swe_sample_tasks() -> List[HermesSWETask]:
    """Generates standard Hermes SWE benchmark tasks."""
    tasks: List[HermesSWETask] = []

    # Task 1: Fix latency threshold comparison
    t1_code = """def check_sla_breach(latency_ms, max_threshold=50.0):
    # Bug: > instead of >=
    return latency_ms > max_threshold
"""
    def t1_f2p(files: Dict[str, str]) -> bool:
        ns = {}
        exec(files.get("monitor.py", ""), ns)
        fn = ns.get("check_sla_breach")
        # Exactly 50.0 must breach SLA
        return bool(fn and fn(50.0, 50.0) is True)

    def t1_p2p(files: Dict[str, str]) -> bool:
        ns = {}
        exec(files.get("monitor.py", ""), ns)
        fn = ns.get("check_sla_breach")
        return bool(fn and fn(45.0, 50.0) is False and fn(55.0, 50.0) is True)

    tasks.append(HermesSWETask(
        task_id="HERMES-SWE-001-SLA-BOUNDARY",
        repo_name="hermes-matrix-adapter",
        issue_text="SLA monitor fails to trigger on exact threshold boundary: latency_ms == max_threshold must breach.",
        initial_files={"monitor.py": t1_code},
        test_suite={"test_sla_exact": t1_f2p, "test_sla_bounds": t1_p2p},
        fail_to_pass=["test_sla_exact"],
        pass_to_pass=["test_sla_bounds"],
    ))

    # Task 2: Fix missing receipt SHA-256 formatting
    t2_code = """def format_receipt_tag(prefix, hash_hex):
    # Bug: missing prefix delimiter
    return f"{prefix}{hash_hex[:8]}"
"""
    def t2_f2p(files: Dict[str, str]) -> bool:
        ns = {}
        exec(files.get("receipt.py", ""), ns)
        fn = ns.get("format_receipt_tag")
        return bool(fn and fn("rcpt", "abcdef123456") == "rcpt_abcdef12")

    def t2_p2p(files: Dict[str, str]) -> bool:
        ns = {}
        exec(files.get("receipt.py", ""), ns)
        fn = ns.get("format_receipt_tag")
        return bool(fn and len(fn("test", "0123456789ab")) >= 8)

    tasks.append(HermesSWETask(
        task_id="HERMES-SWE-002-RECEIPT-TAG",
        repo_name="hermes-matrix-adapter",
        issue_text="Receipt tag must separate prefix with an underscore: expected 'rcpt_abcdef12'.",
        initial_files={"receipt.py": t2_code},
        test_suite={"test_tag_delimiter": t2_f2p, "test_tag_length": t2_p2p},
        fail_to_pass=["test_tag_delimiter"],
        pass_to_pass=["test_tag_length"],
    ))

    return tasks
