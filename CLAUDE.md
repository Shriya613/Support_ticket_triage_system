# Agentic support system with eval harness

## Purpose
Portfolio project demonstrating end-to-end production AI engineering: multi-agent
orchestration, async processing, and a real eval pipeline. Built to fill a gap
in an NLP-heavy resume — this project should read as "systems / production AI,"
not "another NLP project." Target audience: FDE-style roles that care about
evals, reliability, and deployment (not just model quality).

## What we're building
A support-ticket triage system:
1. A **router agent** classifies an incoming request (billing / technical / refund).
2. A **specialist agent** per category handles it, using a small toolset
   (mocked functions returning realistic fake data — no real backend needed).
3. Requests flow through a **queue** (async, retryable) instead of being
   handled synchronously in the API request.
4. Conversation state persists across turns (**state store**).
5. A separate **eval harness** runs a fixed set of golden test cases through
   the same agent pipeline and scores accuracy, latency, and cost — this is
   the centerpiece of the project, not an afterthought.

## Tech stack
- Python, FastAPI
- LangGraph (or CrewAI) for agent orchestration
- Redis or SQS-compatible local queue (start with a simple Redis list if SQS
  setup is friction — the concept matters more than the exact broker)
- SQLite or Redis for state store (SQLite is fine to start)
- Plain Python script for the eval harness — no need for a framework

## Build order (do NOT skip ahead or build everything in one pass)
Each milestone = one commit, working end to end before moving on.

1. **Skeleton** — single agent, one mock tool (`check_order_status()`),
   callable from a plain Python script. No API yet.
2. **Multi-agent split** — router agent + specialist agents (billing,
   technical, refund), each with 1-2 mock tools.
3. **FastAPI wrapper** — expose the agent pipeline over an HTTP endpoint.
4. **Queue** — API enqueues requests; a worker process dequeues and runs
   the agent pipeline; add retry/dead-letter handling.
5. **State store** — persist conversation history per user/session, reload
   on follow-up requests.
6. **Eval harness** — 30-50 golden test cases (input → expected tool call /
   outcome), a runner script that scores accuracy, latency, cost per
   resolution, and a simple report (markdown table or Streamlit) tracking
   results across versions.
7. **Deploy** — Docker Compose locally at minimum; a live Cloud Run/EC2
   deployment is the stretch goal.

## Conventions
- Commit after every milestone above, even if small — the point of this
  project is a visible, incremental commit history.
- Keep mock tools honest: return varied, semi-realistic fake data (not
  always the happy path) so the eval harness has something real to catch.
- Prefer explicit, readable code over cleverness — this repo doubles as a
  portfolio piece a hiring engineer will actually read.
- README should explain the *why* (production concerns: async processing,
  evals, reliability) as much as the *what*.

## Explicitly out of scope for v1
- Real LLM-hosted production infra, auth, multi-tenancy
- A polished frontend — a CLI or minimal API is enough
- Anything NLP-heavy (translation, NER, etc.) — this project exists to
  balance out an NLP-heavy resume, so keep the focus on orchestration,
  systems, and evals
