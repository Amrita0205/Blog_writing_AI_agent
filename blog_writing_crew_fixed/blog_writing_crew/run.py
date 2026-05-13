#!/usr/bin/env python
"""
Run this directly instead of 'crewai run':
    python run.py

Place this file next to pyproject.toml, i.e. inside blog_writing_crew/
"""
import sys
import os
import warnings
import time
from datetime import datetime

# Make sure the src package is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

# Load .env from same directory as this script
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Ensure output directory exists
os.makedirs(os.path.join(os.path.dirname(__file__), "output"), exist_ok=True)

from blog_writing_crew.crew import BlogWritingCrew

# ── Task completion callback ──────────────────────────────────────────────────
# Groq free tier: 12,000 tokens/minute. After each task completes we pause
# briefly to let the TPM window reset before the next agent fires.
COOLDOWN_SECONDS = 20

def task_done_callback(task_output):
    print(f"\n⏳ Task complete. Cooling down {COOLDOWN_SECONDS}s to avoid "
          f"Groq rate limits...\n")
    time.sleep(COOLDOWN_SECONDS)
# ─────────────────────────────────────────────────────────────────────────────


def run():
    inputs = {
        "topic": "The Injustice of Hostel Curfews Imposed on Indian Women Students: "
                 "When Safety Becomes Surveillance and Foreign Students Walk Free",
        "current_year": str(datetime.now().year),
    }

    crew_instance = BlogWritingCrew().crew()

    # Attach cooldown callback to every task
    for t in crew_instance.tasks:
        t.callback = task_done_callback

    crew_instance.kickoff(inputs=inputs)


if __name__ == "__main__":
    run()