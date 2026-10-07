"""Hermes_Matrix_Adapter Evaluation and Evolution Suite.

Pure Python 3.10+ standard library. Zero external dependencies.
Incubated under Apex Growth Systems LLC - Sole Managing Member: Ahmed Hassan.
"""

from hermes_matrix_adapter.eval.e2e_testing import (
    PaperclipAgenticE2EFramework,
    PaperclipE2EScenarioReport,
    PaperclipE2ETestScenario,
    build_standard_hermes_e2e_scenarios,
)
from hermes_matrix_adapter.eval.evolution import (
    HermesAdapterGenome,
    HermesDynamicEvolutionEngine,
    HermesEvolutionProgress,
    HermesSkillFitness,
)
from hermes_matrix_adapter.eval.swe_agent_eval import (
    HermesSWEAgentHarness,
    HermesSWETask,
    HermesSWETrajectoryResult,
    HermesToolCall,
    build_hermes_swe_sample_tasks,
)

__all__ = [
    "HermesSWETask",
    "HermesToolCall",
    "HermesSWETrajectoryResult",
    "HermesSWEAgentHarness",
    "build_hermes_swe_sample_tasks",
    "PaperclipE2ETestScenario",
    "PaperclipE2EScenarioReport",
    "PaperclipAgenticE2EFramework",
    "build_standard_hermes_e2e_scenarios",
    "HermesSkillFitness",
    "HermesAdapterGenome",
    "HermesEvolutionProgress",
    "HermesDynamicEvolutionEngine",
]
