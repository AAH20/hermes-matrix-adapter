"""Benchmark suite for Hermes skill execution and episodic memory recall."""

from __future__ import annotations

import sys
import time
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from hermes_matrix_adapter.adapter import HermesPaperclipMatrixAdapter


def main() -> None:
    print("=" * 72)
    print(" hermes-matrix-adapter: Skill Dispatch & Heartbeat Benchmark")
    print(" Pure Python 3.10+ Standard Library — Zero External Dependencies")
    print("=" * 72)

    adapter = HermesPaperclipMatrixAdapter("bench_hermes")

    # Benchmark: 10,000 skill dispatches & ActionReceipt issues
    iterations = 10000
    print(f"[*] Benchmarking {iterations:,} skill executions + ActionLedger receipts...")
    t0 = time.perf_counter()
    for i in range(iterations):
        adapter.skills.execute_skill("matrix_simulate_blast_radius", {"target_node_id": f"node_{i % 100}"})
        adapter.ledger.issue_receipt("matrix_simulate_blast_radius", f"node_{i % 100}")
    total_ms = (time.perf_counter() - t0) * 1000.0
    avg_us = (total_ms / iterations) * 1000.0

    print(f"[+] Total execution time: {total_ms:.2f} ms")
    print(f"[+] Average dispatch latency: {avg_us:.2f} µs ({avg_us / 1000.0:.4f} ms)")
    assert avg_us < 500.0, "Latency exceeds 500µs threshold"
    print("[✔] SUB-MILLISECOND SKILL DISPATCH THRESHOLD SATISFIED.")
    print("=" * 72)


if __name__ == "__main__":
    main()
