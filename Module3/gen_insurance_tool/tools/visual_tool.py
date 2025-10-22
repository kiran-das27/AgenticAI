# tools/visual_tool.py

from crewai.tools import BaseTool
from typing import Optional, Dict
import matplotlib.pyplot as plt
import json
import os

class PolicyVisualizerTool(BaseTool):
    name:str = "Policy Visualizer"
    description :str = (
        "Generates a bar chart comparing insurance policies based on maturity amount and premium."
        " Expects a list of policies in JSON format with keys: name, premium, maturity_amount."
    )

    def _run(self, policy_data: str, parameters: Optional[Dict] = None) -> str:
        try:
            data = json.loads(policy_data)

            # Extract data
            names = [p["name"] for p in data]
            premiums = [p["premium"] for p in data]
            maturities = [p["maturity_amount"] for p in data]

            # Plot
            plt.figure(figsize=(10, 6))
            plt.bar(names, maturities, label="Maturity Amount", color="green")
            plt.plot(names, premiums, marker="o", label="Annual Premium", color="blue")
            plt.title("Insurance Policy Comparison")
            plt.xlabel("Policy")
            plt.ylabel("INR (₹)")
            plt.legend()
            plt.tight_layout()

            # Ensure output folder exists
            os.makedirs("output", exist_ok=True)
            chart_path = "output/policy_comparison_chart.png"
            plt.savefig(chart_path)
            plt.close()

            return f"Chart saved at {chart_path}"

        except Exception as e:
            return f"Error generating chart: {str(e)}"
