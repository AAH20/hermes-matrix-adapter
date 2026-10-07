"""Unit tests for HermesPaperclipMatrixAdapter, episodic memory, and ActionLedger."""

import unittest

from hermes_matrix_adapter.adapter import HermesPaperclipMatrixAdapter


class TestAdapter(unittest.TestCase):
    def setUp(self) -> None:
        self.adapter = HermesPaperclipMatrixAdapter("test_hermes_01")

    def test_submit_and_heartbeat(self) -> None:
        task = self.adapter.submit_task(
            title="Isolate flapping RoCE interface",
            target_node_id="dgx_node_02",
            goal_id="goal_uptime_01",
            budget_usd=5.0,
        )
        self.assertEqual(task.status, "queued")

        pulse = self.adapter.step_heartbeat()
        self.assertEqual(pulse["heartbeat"], 1)
        self.assertEqual(pulse["processed_tasks"], 1)
        self.assertEqual(task.status, "completed")
        self.assertIsNotNone(task.result)
        self.assertIn("receipt_id", task.result)

    def test_memory_recall(self) -> None:
        self.adapter.submit_task(
            title="High latency on node_03",
            target_node_id="node_03",
            goal_id="goal_latency",
        )
        self.adapter.step_heartbeat()

        recalled = self.adapter.memory.recall_for_node("node_03")
        self.assertEqual(len(recalled), 1)
        self.assertTrue(recalled[0].success)


if __name__ == "__main__":
    unittest.main()
