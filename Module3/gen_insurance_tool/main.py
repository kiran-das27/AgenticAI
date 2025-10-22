#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from gen_insurance_tool.crew import GenInsuranceTool

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'name': 'Kiran Das',
        'age': '40',
        'employmentType':'Salaried',
        'monthlyincome':'100000',
        'preferedPayingFor': '5'
    }
    
    try:
        result=GenInsuranceTool().crew().kickoff(inputs=inputs)
            # Print the result
        print("\n\n=== FINAL DECISION ===\n\n")
        print(result.raw)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")



if __name__ == "__main__":
    run()