"""Unit tests for SWE Benchmark and Agentic E2E Testing Framework in hermes-matrix-adapter.

Pure Python 3.10+ standard library. Zero external dependencies.
Incubated under Apex Growth Systems LLC - Sole Managing Member: Ahmed Hassan.
"""

from __future__ import annotations

import unittest
from typing import Dict, List, Optional, Tuple

from hermes_matrix_adapter.eval.e2e_testing import (
    PaperclipAgenticE2EFramework,
    PaperclipE2ETestScenario,
    build_standard_hermes_e2e_scenarios,
)
from hermes_matrix_adapter.eval.evolution import (
    HermesAdapterGenome,
    HermesDynamicEvolutionEngine,
    HermesSkillFitness,
)
from hermes_matrix_adapter.eval.swe_agent_eval import (
    HermesSWEAgentHarness,
    HermesSWETask,
    HermesToolCall,
    build_hermes_swe_sample_tasks,
)


class TestHermesSWEAgentHarness(unittest.TestCase):
    """Test Hermes Agent SWE evaluation and trajectory recording."""

    def setUp(self):
        self.harness = HermesSWEAgentHarness(agent_id="test_hermes_eval")
        self.tasks = build_hermes_swe_sample_tasks()

    def test_sample_tasks_loaded(self):
        self.assertGreaterEqual(len(self.tasks), 2)
        task_ids = [t.task_id for t in self.tasks]
        self.assertIn("HERMES-SWE-001-SLA-BOUNDARY", task_ids)
        self.assertIn("HERMES-SWE-002-RECEIPT-TAG", task_ids)

    def test_successful_swe_trajectory(self):
        task = self.tasks[0]

        def solver_steps(t: HermesSWETask, files: Dict[str, str], history: List[HermesToolCall]) -> Optional[Tuple[str, Dict]]:
            if len(history) == 0:
                return ("view_file", {"filepath": "monitor.py"})
            elif len(history) == 1:
                return ("edit_file", {
                    "filepath": "monitor.py",
                    "target_content": "return latency_ms > max_threshold",
                    "replacement_content": "return latency_ms >= max_threshold",
                })
            return None

        result = self.harness.run_swe_trajectory(task, solver_steps, max_turns=5)
        self.assertTrue(result.resolved)
        self.assertEqual(result.total_turns, 2)
        self.assertEqual(result.tool_call_precision, 1.0)
        self.assertGreaterEqual(result.receipt_count, 2)
        self.assertLess(result.elapsed_ms, 50.0)

    def test_unresolved_swe_trajectory(self):
        task = self.tasks[0]

        def failing_solver(t: HermesSWETask, files: Dict[str, str], history: List[HermesToolCall]) -> Optional[Tuple[str, Dict]]:
            if len(history) == 0:
                return ("view_file", {"filepath": "monitor.py"})
            return None

        result = self.harness.run_swe_trajectory(task, failing_solver, max_turns=2)
        self.assertFalse(result.resolved)


class TestPaperclipAgenticE2EFramework(unittest.TestCase):
    """Test Paperclip Company OS multi-heartbeat E2E testing framework."""

    def setUp(self):
        self.framework = PaperclipAgenticE2EFramework(cost_per_task_usd=0.25)
        self.scenarios = build_standard_hermes_e2e_scenarios()

    def test_standard_e2e_scenarios_pass(self):
        for scenario in self.scenarios:
            report = self.framework.run_scenario(scenario, agent_id="hermes_unit_tester")
            self.assertTrue(report.passed, f"Scenario {scenario.scenario_id} failed: {report.invariant_violations}")
            self.assertTrue(report.budget_adherence)
            self.assertEqual(report.completed_tasks, report.total_tasks)
            self.assertGreaterEqual(report.action_receipts_verified, report.completed_tasks)
            self.assertGreaterEqual(report.memory_episodes_verified, report.completed_tasks)

    def test_budget_breach_detection(self):
        expensive_framework = PaperclipAgenticE2EFramework(cost_per_task_usd=50.0)
        scenario = PaperclipE2ETestScenario(
            scenario_id="BUDGET-TEST",
            name="Deliberate Budget Breach Test",
            tasks_to_submit=[{"title": "Task A", "target_node_id": "n1", "goal_id": "g1", "budget_usd": 10.0}],
            expected_heartbeats=1,
        )
        report = expensive_framework.run_scenario(scenario)
        self.assertFalse(report.passed)
        self.assertFalse(report.budget_adherence)
        self.assertTrue(any("Budget breached" in v for v in report.invariant_violations))


class TestHermesDynamicEvolutionEngine(unittest.TestCase):
    """Test Hermes dynamic skill fitness tracking, parameter mutation, and evolution."""

    def setUp(self):
        self.engine = HermesDynamicEvolutionEngine(seed=42)

    def test_skill_fitness_calculation(self):
        self.engine.record_skill_execution("matrix_simulate_blast_radius", success=True, latency_ms=1.5)
        self.engine.record_skill_execution("matrix_simulate_blast_radius", success=True, latency_ms=2.0)
        fit = self.engine.skill_fitness["matrix_simulate_blast_radius"]

        self.assertEqual(fit.invocations, 2)
        self.assertEqual(fit.success_rate, 1.0)
        self.assertGreater(fit.fitness_score, 0.9)

    def test_genome_mutation_bounds(self):
        parent = HermesAdapterGenome(genome_id="root", generation=0, attenuation_factor=0.85)
        child = parent.mutate(mutation_rate=1.0)

        self.assertEqual(child.generation, 1)
        self.assertGreaterEqual(child.attenuation_factor, 0.5)
        self.assertLessEqual(child.attenuation_factor, 0.99)
        self.assertGreaterEqual(child.max_budget_per_task, 5.0)

    def test_genome_evaluation(self):
        genome = HermesAdapterGenome(genome_id="g_eval", generation=0)
        score = self.engine.evaluate_genome(genome)

        self.assertGreater(score, 0.5)
        self.assertEqual(genome.swe_resolution_rate, 1.0)
        self.assertEqual(genome.e2e_pass_rate, 1.0)

    def test_multi_generation_evolution_loop(self):
        best_genome, history = self.engine.run_evolution_loop(
            generations=3,
            population_size=3,
            mutation_rate=0.35,
        )

        self.assertEqual(len(history), 3)
        self.assertIsNotNone(best_genome)
        self.assertGreaterEqual(best_genome.fitness_score, 0.8)
        self.assertIn("Hermes SRE Heuristic", best_genome.guidance_heuristics)


if __name__ == "__main__":
    unittest.main()
