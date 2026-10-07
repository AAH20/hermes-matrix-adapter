"""Hermes_Matrix_Adapter: Persistent Episodic Memory Bridge.

Retains incident history, verified post-mortems, and remediation lessons across sessions.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class EpisodeRecord:
    """An individual episodic memory entry from an incident remediation."""
    episode_id: str
    incident_id: str
    impacted_node_id: str
    symptom: str
    remediation_action: str
    success: bool
    lessons_learned: str
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "episode_id": self.episode_id,
            "incident_id": self.incident_id,
            "impacted_node_id": self.impacted_node_id,
            "symptom": self.symptom,
            "remediation_action": self.remediation_action,
            "success": self.success,
            "lessons_learned": self.lessons_learned,
            "timestamp": self.timestamp,
        }


class HermesEpisodicMemory:
    """Memory manager providing fast associative retrieval for Hermes Agent."""

    def __init__(self) -> None:
        self.episodes: List[EpisodeRecord] = []

    def record_episode(
        self,
        incident_id: str,
        impacted_node_id: str,
        symptom: str,
        remediation_action: str,
        success: bool,
        lessons_learned: str,
    ) -> EpisodeRecord:
        """Store an incident remediation outcome into persistent memory."""
        ep_id = f"ep_{len(self.episodes) + 1:04d}"
        record = EpisodeRecord(
            episode_id=ep_id,
            incident_id=incident_id,
            impacted_node_id=impacted_node_id,
            symptom=symptom,
            remediation_action=remediation_action,
            success=success,
            lessons_learned=lessons_learned,
        )
        self.episodes.append(record)
        return record

    def recall_for_node(self, node_id: str) -> List[EpisodeRecord]:
        """Find past episodes for a specific node."""
        return [e for e in self.episodes if e.impacted_node_id == node_id]

    def recall_by_symptom(self, keyword: str) -> List[EpisodeRecord]:
        """Search past episodes matching symptom keyword."""
        kw = keyword.lower()
        return [e for e in self.episodes if kw in e.symptom.lower()]

    def serialize_json(self) -> str:
        return json.dumps([e.to_dict() for e in self.episodes], indent=2)

    def load_json(self, data_str: str) -> None:
        items = json.loads(data_str)
        self.episodes = [
            EpisodeRecord(
                episode_id=it["episode_id"],
                incident_id=it["incident_id"],
                impacted_node_id=it["impacted_node_id"],
                symptom=it["symptom"],
                remediation_action=it["remediation_action"],
                success=it["success"],
                lessons_learned=it["lessons_learned"],
                timestamp=it.get("timestamp", time.time()),
            )
            for it in items
        ]
