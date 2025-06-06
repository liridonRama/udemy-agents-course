#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from coder_custom.crew import CoderCustom

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

assignment = "Write a python program to calculate the first 10,000 terms \
     of this series, multiplying the total by 4: 1 - 1/3 + 1/5 - 1/7 + ..."


def run():
    """
    Run the crew.
    """
    inputs = {"assignment": assignment}

    try:
        result = CoderCustom().crew().kickoff(inputs=inputs)
        print(result.raw)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
