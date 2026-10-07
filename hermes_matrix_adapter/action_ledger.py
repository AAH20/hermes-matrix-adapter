"""Hermes_Matrix_Adapter: ActionLedger Cryptographic Receipts.

Integrates with AAH20/fde-bounty-snr to emit immutable SHA-256 receipts for Hermes actions.
"""

from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass, field
from typing import List


@dataclass
class HermesActionReceipt:
    """Immutable audit token generated upon Hermes tool completion."""
    receipt_id: str
    agent_id: str
    skill_name: str
    target_node_id: str
    receipt_hash: str
    timestamp: float = field(default_factory=time.time)


class HermesActionLedger:
    """Manages continuous cryptographic audit logging for Hermes Agent."""

    def __init__(self, agent_id: str = "hermes_fde_01") -> None:
        self.agent_id = agent_id
        self.receipts: List[HermesActionReceipt] = []

    def issue_receipt(self, skill_name: str, target_node_id: str) -> HermesActionReceipt:
        raw = f"{self.agent_id}:{skill_name}:{target_node_id}:{time.time()}"
        r_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        receipt = HermesActionReceipt(
            receipt_id=f"rcpt_hermes_{r_hash[:10]}",
            agent_id=self.agent_id,
            skill_name=skill_name,
            target_node_id=target_node_id,
            receipt_hash=r_hash,
        )
        self.receipts.append(receipt)
        return receipt
