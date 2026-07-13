"""Milestone 1 entrypoint: run the single agent from the command line.

Usage:
    python scripts/run_single_agent.py "Where is my order ORD-1002?"

With no argument, drops into an interactive REPL.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv

load_dotenv()

from app.agents.single_agent import SingleAgent


def main():
    agent = SingleAgent()

    if len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])
        print(agent.run(message))
        return

    print("Support agent ready. Type a message (Ctrl+C to exit).")
    while True:
        try:
            message = input("> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not message.strip():
            continue
        print(agent.run(message))


if __name__ == "__main__":
    main()
