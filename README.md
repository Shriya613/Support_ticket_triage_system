# Agentic Support Ticket Triage System

A support-ticket triage system built to demonstrate production AI engineering:
multi-agent orchestration, async processing, and a real eval pipeline —
not just prompting a model and calling it done.

## Why this exists

Most NLP portfolio projects stop at "the model gives a good answer." The
harder, more relevant problems in production AI systems are elsewhere:

- **Reliability** — what happens when a tool call fails, or the model picks
  the wrong tool? Does the system retry, degrade gracefully, or silently fail?
- **Async processing** — real systems don't block an HTTP request on an LLM
  call chain; work gets queued and processed independently.
- **Evals** — "it works when I tried it" isn't an engineering claim. This
  project treats a golden-test eval harness as the centerpiece, not an
  afterthought, so accuracy/latency/cost regressions are caught the same way
  a test suite catches a broken build.

This project is built incrementally, one working milestone at a time, with a
commit at each step — see [CLAUDE.md](CLAUDE.md) for the full build order.

## Status: Milestone 1 — skeleton

A single agent with one mock tool (`check_order_status`), callable from a
plain Python script. No API, no queue, no state store yet — this milestone
only proves the core loop: user message -> Claude decides whether to call a
tool -> tool runs -> Claude answers using the result.

```
app/
  agents/
    single_agent.py     # Claude tool-use loop
  tools/
    order_status.py     # mock check_order_status() with varied fake data
scripts/
  run_single_agent.py   # plain-Python entrypoint
```

### Running it

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then fill in ANTHROPIC_API_KEY

python scripts/run_single_agent.py "Where is my order ORD-1002?"
# or, interactively:
python scripts/run_single_agent.py
```

Try order IDs `ORD-1001` through `ORD-1005` (delivered, in transit, delayed,
processing, cancelled) or an unknown ID to see the not-found path.
