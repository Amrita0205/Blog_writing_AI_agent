#!/usr/bin/env python
import sys
import warnings
from datetime import datetime

from blog_writing_crew.crew import BlogWritingCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    inputs = {
        "topic": "The Injustice of Hostel Curfews Imposed on Indian Women Students: "
                 "When Safety Becomes Surveillance and Foreign Students Walk Free",
        "current_year": str(datetime.now().year),
    }
    try:
        BlogWritingCrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year),
    }
    try:
        BlogWritingCrew().crew().train(
            n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs
        )
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    try:
        BlogWritingCrew().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year),
    }
    try:
        BlogWritingCrew().crew().test(
            n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs
        )
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
