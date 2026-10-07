"""Hermes_Matrix_Adapter: Turnkey Sovereign Skill & Memory Bridge for Nous Research Hermes Agent.

Pure Python 3.10+ standard library. Zero external dependencies.
Incubated under Apex Growth Systems LLC - Sole Managing Member: Ahmed Hassan.
"""

from hermes_matrix_adapter.action_ledger import (
    HermesActionLedger,
    HermesActionReceipt,
)
from hermes_matrix_adapter.adapter import (
    HermesPaperclipMatrixAdapter,
    PaperclipTask,
)
from hermes_matrix_adapter.memory import (
    EpisodeRecord,
    HermesEpisodicMemory,
)
from hermes_matrix_adapter.skills import HermesSkillRegistry

__version__ = "1.0.0"
__author__ = "Ahmed Hassan"
__company__ = "Apex Growth Systems LLC"

__all__ = [
    "__version__",
    "__author__",
    "__company__",
    "HermesSkillRegistry",
    "HermesEpisodicMemory",
    "EpisodeRecord",
    "HermesActionLedger",
    "HermesActionReceipt",
    "HermesPaperclipMatrixAdapter",
    "PaperclipTask",
]
