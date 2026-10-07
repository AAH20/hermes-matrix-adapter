"""End-to-End Walkthrough: Hermes SWE Agent Evaluation & Evolution in hermes-matrix-adapter.

Demonstrates Nous Hermes function-calling SWE problem solving, Paperclip Company OS
multi-heartbeat E2E testing with budget governance, and dynamic skill evolution.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from hermes_matrix_adapter.eval import (
    HermesDynamicEvolutionEngine,
    HermesSWEAgentHarness,
    PaperclipAgenticE2EFramework,
    build_hermes_swe_sample_tasks,
    build_standard_hermes_e2e_scenarios,
)


def main():
    print("=" * 72)
    print(" Hermes_Matrix_Adapter: SWE Evaluation & Paperclip E2E Walkthrough")
    print("=" * 72)

    # Step 1: Run Hermes SWE Benchmark
    print("\n[Step 1] Running Hermes Agent SWE Problem Solving Trajectory...")
    swe_harness = HermesSWEAgentHarness(agent_id="hermes_walkthrough_sre")
    tasks = build_hermes_swe_sample_tasks()

    def hermes_agent_solver(task, files, history):
        print(f"  -> Hermes reasoning turn {len(history) + 1} for task: {task.task_id}")
        if len(history) == 0:
            return ("view_file", {"filepath": "monitor.py"})
        elif len(history) == 1:
            return ("edit_file", {
                "filepath": "monitor.py",
                "target_content": "return latency_ms > max_threshold",
                "replacement_content": "return latency_ms >= max_threshold",
            })
        return None

    res = swe_harness.run_swe_trajectory(tasks[0], hermes_agent_solver, max_turns=5)
    print(f"  SWE Resolved: {res.resolved}")
    print(f"  Turns Taken: {res.total_turns}")
    print(f"  Tool Precision: {res.tool_call_precision * 100:.1f}%")
    print(f"  ActionLedger Receipts Issued: {res.receipt_count}")
    print(f"  Latency: {res.elapsed_ms:.3f} ms")

    # Step 2: Run Paperclip Company OS E2E Testing
    print("\n[Step 2] Executing Paperclip Company OS Agentic E2E Scenarios...")
    e2e_framework = PaperclipAgenticE2EFramework(cost_per_task_usd=0.50)
    scenarios = build_standard_hermes_e2e_scenarios()

    for sc in scenarios:
        report = e2e_framework.run_scenario(sc, agent_id="hermes_corp_sre")
        status = "PASSED" if report.passed else "FAILED"
        print(f"  [{status}] {sc.scenario_id}: {sc.name}")
        print(f"       Tasks: {report.completed_tasks}/{report.total_tasks} | Budget: ${report.actual_spend_usd:.2f}/${report.total_budget_usd:.2f} | Receipts: {report.action_receipts_verified} | Latency: {report.elapsed_ms:.3f} ms")

    # Step 3: Dynamic Skill & Memory Evolution
    print("\n[Step 3] Running Hermes Dynamic Skill & Memory Evolution Loop (5 Generations)...")
    evolution = HermesDynamicEvolutionEngine(seed=42)
    best_genome, history = evolution.run_evolution_loop(generations=5, population_size=3, mutation_rate=0.35)

    print(f"  Optimal Genome: {best_genome.genome_id}")
    print(f"  Composite Fitness: {best_genome.fitness_score:.4f}")
    print(f"  Attenuation Factor: {best_genome.attenuation_factor:.3f}")
    print(f"  Task Budget Ceiling: ${best_genome.max_budget_per_task:.1f}")
    print(f"  Synthesized Heuristics: {best_genome.guidance_heuristics}")
    print("=" * 72)


if __name__ == "__main__":
    main()
