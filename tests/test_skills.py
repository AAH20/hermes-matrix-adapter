"""Unit tests for Hermes skill registry and tool execution."""

import unittest

from hermes_matrix_adapter.skills import HermesSkillRegistry


class TestSkills(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = HermesSkillRegistry()

    def test_list_skills(self) -> None:
        skills = self.registry.list_skills()
        names = [s["name"] for s in skills]
        self.assertIn("matrix_query_topology", names)
        self.assertIn("matrix_simulate_blast_radius", names)
        self.assertIn("matrix_export_palantir_ontology", names)

    def test_execute_blast_radius_skill(self) -> None:
        res = self.registry.execute_skill(
            "matrix_simulate_blast_radius",
            {"target_node_id": "dgx_node_01", "attenuation_factor": 0.8},
        )
        self.assertEqual(res["target_node_id"], "dgx_node_01")
        self.assertEqual(res["attenuation_factor"], 0.8)
        self.assertTrue(res["impact_score"] > 0)

    def test_execute_palantir_export_skill(self) -> None:
        res = self.registry.execute_skill(
            "matrix_export_palantir_ontology",
            {"ontology_rid": "ri.ontology.test"},
        )
        self.assertEqual(res["status"], "exported")
        self.assertEqual(res["ontologyRid"], "ri.ontology.test")


if __name__ == "__main__":
    unittest.main()
