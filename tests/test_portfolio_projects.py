"""Smoke and invariant tests for every portfolio case study."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


def load(relative: str, name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


class PortfolioTests(unittest.TestCase):
    def test_did_recovers_known_effect(self):
        module = load("projects/01_policy_causal_evaluation/analysis.py", "causal")
        result = module.estimate_did(module.make_demo_panel())
        self.assertLess(result["effect"], -2.5)
        self.assertGreater(result["effect"], -3.8)
        self.assertLess(result["ci_low"], result["ci_high"])

    def test_hospital_pipeline_removes_bad_rows(self):
        module = load("projects/02_hospital_price_transparency/analysis.py", "prices")
        clean, quality = module.clean_rates(module.make_demo_rates())
        self.assertEqual(quality["invalid_rates"], 1)
        self.assertEqual(quality["duplicates_removed"], 2)
        self.assertTrue((clean["rate"] > 0).all())

    def test_llm_scorecard_is_bounded(self):
        module = load("projects/03_llm_evaluation_lab/evaluation.py", "llm_eval")
        summary, _, agreement = module.evaluate(module.make_demo_judgments(n=80))
        self.assertTrue(summary["accuracy"].between(0, 1).all())
        self.assertGreater(agreement["cohen_kappa"], 0.5)

    def test_experiment_produces_decision(self):
        module = load("projects/04_experimentation_decision_engine/experiment.py", "experiment")
        result = module.analyze(module.make_demo_experiment(n=6000))
        self.assertIn(result["decision"], {"LAUNCH", "DO NOT LAUNCH"})
        self.assertGreater(result["cuped_variance_reduction"], 0)

    def test_churn_economics_reconcile(self):
        module = load("projects/05_retention_churn_copilot/pipeline.py", "churn")
        scored, _, auc = module.train_and_score(module.make_demo_accounts(n=800))
        case = module.intervention_business_case(scored)
        self.assertGreater(auc, 0.7)
        self.assertAlmostEqual(case["net_value"], case["expected_revenue_saved"] - case["intervention_cost"])


if __name__ == "__main__":
    unittest.main()
