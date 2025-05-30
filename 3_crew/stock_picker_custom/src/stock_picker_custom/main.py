#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from stock_picker_custom.crew import StockPickerCustom

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the crew.
    """
    inputs = {"sector": "Technology"}

    try:
        StockPickerCustom().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
