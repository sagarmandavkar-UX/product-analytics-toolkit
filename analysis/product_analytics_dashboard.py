"""
Product Analytics Dashboard
Author: Sagar Mandavkar

A lightweight product analytics engine for an illustrative e-commerce dataset.
The goal is to turn behavioral data into product decisions through KPI tracking,
funnel diagnosis, segmentation, and revenue analysis.
"""

from pathlib import Path
import warnings

import matplotlib.pyplot as plt
import pandas as pd

warnings.filterwarnings("ignore")

OUTPUT_DIR = Path(__file__).resolve().parents[1] / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


class ProductAnalyticsDashboard:
    """Analyze product behavior at the session level."""

    def __init__(self, data_path):
        self.df = pd.read_csv(data_path)
        self.df["timestamp"] = pd.to_datetime(self.df["timestamp"])
        self.df["date"] = self.df["timestamp"].dt.date
        self.sessions = self._build_session_table()

    def _build_session_table(self):
        """Create one row per session to avoid double-counting event-level rows."""
        session_dimensions = (
            self.df.sort_values("timestamp")
            .groupby("session_id", as_index=False)
            .agg(
                user_id=("user_id", "first"),
                date=("date", "first"),
                device=("device", "first"),
                channel=("channel", "first"),
                country=("country", "first"),
                experiment_group=("experiment_group", "first"),
                revenue=("revenue", "sum"),
                converted=("conversion", "max"),
            )
        )

        event_flags = (
            self.df.assign(value=1)
            .pivot_table(
                index="session_id",
                columns="event_type",
                values="value",
                aggfunc="max",
                fill_value=0,
            )
            .reset_index()
        )

        sessions = session_dimensions.merge(event_flags, on="session_id", how="left")
        for col in ["page_view", "add_to_cart", "purchase"]:
            if col not in sessions:
                sessions[col] = 0
        return sessions

    def calculate_conversion_metrics(self):
        """Calculate decision-oriented product KPIs."""
        total_sessions = self.sessions["session_id"].nunique()
        total_users = self.sessions["user_id"].nunique()
        purchases = int(self.sessions["purchase"].sum())
        carts = int(self.sessions["add_to_cart"].sum())
        total_revenue = self.sessions["revenue"].sum()

        conversion_rate = purchases / total_sessions if total_sessions else 0
        cart_abandonment = (carts - purchases) / carts if carts else 0
        avg_order_value = total_revenue / purchases if purchases else 0
        revenue_per_session = total_revenue / total_sessions if total_sessions else 0

        return {
            "Total Sessions": total_sessions,
            "Total Users": total_users,
            "Purchases": purchases,
            "Purchase Conversion Rate": f"{conversion_rate:.2%}",
            "Cart Abandonment Rate": f"{cart_abandonment:.2%}",
            "Total Revenue": f"${total_revenue:,.2f}",
            "Average Order Value": f"${avg_order_value:,.2f}",
            "Revenue per Session": f"${revenue_per_session:,.2f}",
        }

    def funnel_analysis(self):
        """Measure stage reach, stage-to-stage conversion, and drop-off."""
        stages = [
            ("Page View", "page_view"),
            ("Add to Cart", "add_to_cart"),
            ("Purchase", "purchase"),
        ]

        rows = []
        first_stage_sessions = None
        previous_sessions = None

        for stage_name, column in stages:
            sessions = int(self.sessions[column].sum())
            if first_stage_sessions is None:
                first_stage_sessions = sessions

            overall_conversion = sessions / first_stage_sessions if first_stage_sessions else 0
            stage_conversion = sessions / previous_sessions if previous_sessions else 1.0
            stage_drop_off = 1 - stage_conversion if previous_sessions else 0

            rows.append(
                {
                    "Stage": stage_name,
                    "Sessions": sessions,
                    "Overall Conversion": round(overall_conversion * 100, 2),
                    "Stage Conversion": round(stage_conversion * 100, 2),
                    "Stage Drop-off": round(stage_drop_off * 100, 2),
                }
            )
            previous_sessions = sessions

        return pd.DataFrame(rows)

    def segment_analysis(self, dimension):
        """Compare conversion and monetization across a product segment."""
        if dimension not in {"device", "channel", "country", "experiment_group"}:
            raise ValueError("Unsupported segment dimension")

        metrics = (
            self.sessions.groupby(dimension)
            .agg(
                sessions=("session_id", "nunique"),
                users=("user_id", "nunique"),
                purchases=("purchase", "sum"),
                revenue=("revenue", "sum"),
            )
            .reset_index()
        )
        metrics["conversion_rate"] = metrics["purchases"] / metrics["sessions"]
        metrics["revenue_per_session"] = metrics["revenue"] / metrics["sessions"]
        return metrics.sort_values("conversion_rate", ascending=False)

    def product_opportunities(self):
        """Surface simple diagnostic opportunities for PM follow-up."""
        funnel = self.funnel_analysis()
        largest_drop = funnel.iloc[1:].sort_values("Stage Drop-off", ascending=False).iloc[0]

        device = self.segment_analysis("device")
        channel = self.segment_analysis("channel")

        return {
            "largest_funnel_drop": (
                f"{largest_drop['Stage']} has the largest stage drop-off "
                f"({largest_drop['Stage Drop-off']:.1f}%)."
            ),
            "highest_converting_device": str(device.iloc[0]["device"]),
            "highest_converting_channel": str(channel.iloc[0]["channel"]),
            "recommended_next_step": (
                "Form an experiment hypothesis around the largest funnel drop, "
                "then validate it by segment before shipping broadly."
            ),
        }

    def plot_funnel(self, funnel_df):
        plt.figure(figsize=(10, 6))
        plt.barh(funnel_df["Stage"], funnel_df["Sessions"])
        plt.xlabel("Sessions")
        plt.title("E-commerce Conversion Funnel")
        plt.gca().invert_yaxis()
        plt.tight_layout()
        path = OUTPUT_DIR / "funnel_analysis.png"
        plt.savefig(path, dpi=200, bbox_inches="tight")
        plt.close()
        return path

    def plot_revenue_trends(self):
        daily_revenue = self.sessions.groupby("date")["revenue"].sum().reset_index()
        plt.figure(figsize=(10, 5))
        plt.plot(daily_revenue["date"], daily_revenue["revenue"], marker="o")
        plt.xlabel("Date")
        plt.ylabel("Revenue ($)")
        plt.title("Daily Revenue")
        plt.xticks(rotation=45)
        plt.tight_layout()
        path = OUTPUT_DIR / "revenue_trends.png"
        plt.savefig(path, dpi=200, bbox_inches="tight")
        plt.close()
        return path

    def generate_full_report(self):
        print("=" * 68)
        print("PRODUCT ANALYTICS DECISION REPORT")
        print("=" * 68)

        print("\n1. NORTH-STAR SUPPORTING KPIs")
        for key, value in self.calculate_conversion_metrics().items():
            print(f"{key:30s}: {value}")

        funnel = self.funnel_analysis()
        print("\n2. FUNNEL DIAGNOSIS")
        print(funnel.to_string(index=False))

        print("\n3. DEVICE PERFORMANCE")
        print(self.segment_analysis("device").to_string(index=False))

        print("\n4. CHANNEL PERFORMANCE")
        print(self.segment_analysis("channel").to_string(index=False))

        print("\n5. PRODUCT OPPORTUNITIES")
        for key, value in self.product_opportunities().items():
            print(f"{key}: {value}")

        self.plot_funnel(funnel)
        self.plot_revenue_trends()
        print(f"\nCharts saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    dataset = Path(__file__).resolve().parents[1] / "data" / "ecommerce_data.csv"
    ProductAnalyticsDashboard(dataset).generate_full_report()
