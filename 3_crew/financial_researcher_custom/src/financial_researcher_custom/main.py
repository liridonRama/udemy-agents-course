#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from financial_researcher_custom.crew import FinancialResearcherCustom

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the crew.
    """
    inputs = {"company": "Tesla"}

    try:
        FinancialResearcherCustom().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
