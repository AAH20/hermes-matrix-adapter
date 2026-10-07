"""Hermes + Paperclip + Matrix full walkthrough demo."""

from __future__ import annotations

import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from hermes_matrix_adapter import HermesPaperclipMatrixAdapter

# 1. Initialize master adapter
adapter = HermesPaperclipMatrixAdapter(agent_id="hermes_forward_deployed_01")

# 2. Paperclip assigns task to Hermes
task = adapter.submit_task(
    title="Thermal throttle on DGX GPU Cluster 02",
    target_node_id="dgx_cluster_node_02",
    goal_id="goal_gpu_availability_99",
    budget_usd=10.0,
)
print(f"Task Enqueued: {task.task_id} ('{task.title}')")

# 3. Paperclip heartbeat triggers execution
pulse = adapter.step_heartbeat()
print(f"Heartbeat #{pulse['heartbeat']} processed {pulse['processed_tasks']} tasks.")

# 4. Inspect result & cryptographic ActionReceipt
print(f"Task Result Status: {task.status}")
print(f"Receipt ID: {task.result['receipt_id']}")
print(f"Receipt Hash: {task.result['receipt_hash'][:16]}...")
print(f"Blast Radius Impact: {task.result['blast_radius']['impact_score']}")

# 5. Recall past episode from persistent memory
past = adapter.memory.recall_for_node("dgx_cluster_node_02")
print(f"Recalled Memory: {past[0].lessons_learned}")
