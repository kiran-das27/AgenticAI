from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from typing import Type

class PolicyVisualizerInput(BaseModel):
    inputs: dict = Field(..., description="Input data containing policies and selected policy")



class PolicyVisualizerTool(BaseTool):
    name: str = "Policy Textual Visualizer"
    description: str = "Generates a text-based or Markdown comparison of policies."
    args_schema: Type[BaseModel] = PolicyVisualizerInput

    def _run(self, inputs: dict) -> str:
        data = inputs.get("inputs", {})

        traditional_policies = data.get("find_traditional_policies", {})
        marketlinked_policies = data.get("find_marketlinked_policies", {})
        selected_policy = data.get("pick_best_policy", "")

        output = "# 📊 Policy Comparison Report\n\n"

        output += "## Traditional Policies\n"
        for policy in traditional_policies.get("companies", []):
            output += f"- **{policy['policy_name']}**: ₹{policy['premium_amount']}/yr, Term: {policy['policy_term']} yrs, Maturity: ₹{policy['Maturity_amount']}\n"

        output += "\n## Market-Linked Policies\n"
        for policy in marketlinked_policies.get("companies", []):
            output += f"- **{policy['policy_name']}**: ₹{policy['premium_amount']}/yr, Term: {policy['policy_term']} yrs, Maturity: ₹{policy['Maturity_amount']}\n"

        output += f"\n## ✅ Selected Policy\n\n**{selected_policy}**\n"

        with open("terminal_output.md","w") as f:
            f.write(output)

        return output
