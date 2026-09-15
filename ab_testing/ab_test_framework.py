"""A/B testing utilities for product experiments."""

from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats


class ABTestFramework:
    """Evaluate a binary-conversion experiment at the session level."""

    def __init__(self, data_path):
        df = pd.read_csv(data_path)
        self.sessions = (
            df.groupby("session_id", as_index=False)
            .agg(
                experiment_group=("experiment_group", "first"),
                converted=("conversion", "max"),
                revenue=("revenue", "sum"),
            )
        )

    def calculate_conversion_rates(self):
        results = (
            self.sessions.groupby("experiment_group")
            .agg(
                sessions=("session_id", "nunique"),
                conversions=("converted", "sum"),
                revenue=("revenue", "sum"),
            )
        )
        results["conversion_rate"] = results["conversions"] / results["sessions"]
        results["revenue_per_session"] = results["revenue"] / results["sessions"]
        return results

    def run_statistical_test(self, alpha=0.05):
        """Run a two-sided pooled z-test and return decision-oriented output."""
        rates = self.calculate_conversion_rates()
        required_groups = {"control", "treatment"}
        if not required_groups.issubset(rates.index):
            raise ValueError("Dataset must contain control and treatment groups")

        control_total = int(rates.loc["control", "sessions"])
        treatment_total = int(rates.loc["treatment", "sessions"])
        control_conv = int(rates.loc["control", "conversions"])
        treatment_conv = int(rates.loc["treatment", "conversions"])

        if control_total == 0 or treatment_total == 0:
            raise ValueError("Both experiment groups must contain sessions")

        p_control = control_conv / control_total
        p_treatment = treatment_conv / treatment_total
        difference = p_treatment - p_control
        p_pooled = (control_conv + treatment_conv) / (control_total + treatment_total)
        pooled_se = np.sqrt(
            p_pooled
            * (1 - p_pooled)
            * ((1 / control_total) + (1 / treatment_total))
        )

        if pooled_se == 0:
            z_score = 0.0
            p_value = 1.0
        else:
            z_score = difference / pooled_se
            p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))

        unpooled_se = np.sqrt(
            (p_control * (1 - p_control) / control_total)
            + (p_treatment * (1 - p_treatment) / treatment_total)
        )
        z_critical = stats.norm.ppf(0.975)
        ci_low = difference - z_critical * unpooled_se
        ci_high = difference + z_critical * unpooled_se
        lift = (difference / p_control) * 100 if p_control else np.nan
        significant = p_value < alpha

        if significant and difference > 0:
            recommendation = "Treatment is a candidate to ship, pending guardrail review."
        elif significant and difference < 0:
            recommendation = "Do not ship treatment; it significantly reduced conversion."
        else:
            recommendation = (
                "Result is inconclusive at the selected alpha; collect more data or revisit the hypothesis."
            )

        return {
            "control_sessions": control_total,
            "treatment_sessions": treatment_total,
            "control_rate": p_control,
            "treatment_rate": p_treatment,
            "absolute_difference": difference,
            "lift_percent": lift,
            "z_score": z_score,
            "p_value": p_value,
            "confidence_interval_95": (ci_low, ci_high),
            "statistically_significant": significant,
            "recommendation": recommendation,
        }


if __name__ == "__main__":
    dataset = Path(__file__).resolve().parents[1] / "data" / "ecommerce_data.csv"
    ab_test = ABTestFramework(dataset)
    results = ab_test.run_statistical_test()
    print("A/B Test Decision Report")
    print("=" * 50)
    for key, value in results.items():
        print(f"{key}: {value}")
