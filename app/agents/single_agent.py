"""Milestone 1: a single agent with one mock tool, no orchestration framework.

This is the smallest possible slice that proves the core loop end to end:
user message -> Claude decides whether to call a tool -> tool runs -> Claude
answers using the tool result. Router/specialist split, the API layer, the
queue, and persistent state all get layered on in later milestones.
"""

import os

from anthropic import Anthropic

from app.tools.order_status import check_order_status

SYSTEM_PROMPT = """You are a support agent for an e-commerce company. \
You can look up order status using the check_order_status tool when a \
customer asks about their order. Be concise and helpful. If an order \
isn't found, say so clearly and ask the customer to double-check the \
order ID."""

TOOLS = [
    {
        "name": "check_order_status",
        "description": (
            "Look up the current shipping/fulfillment status of a customer's "
            "order by its order ID."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "The order ID, e.g. 'ORD-1001'.",
                }
            },
            "required": ["order_id"],
        },
    }
]

TOOL_IMPLEMENTATIONS = {
    "check_order_status": lambda input_: check_order_status(input_["order_id"]),
}

MAX_TOOL_ITERATIONS = 5


class SingleAgent:
    """A minimal Claude tool-use loop, wired to exactly one mock tool."""

    def __init__(self, model: str | None = None):
        self.client = Anthropic()
        self.model = model or os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")

    def run(self, user_message: str) -> str:
        messages = [{"role": "user", "content": user_message}]

        for _ in range(MAX_TOOL_ITERATIONS):
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=SYSTEM_PROMPT,
                tools=TOOLS,
                messages=messages,
            )

            if response.stop_reason != "tool_use":
                return "".join(
                    block.text for block in response.content if block.type == "text"
                )

            messages.append({"role": "assistant", "content": response.content})

            tool_results = []
            for block in response.content:
                if block.type != "tool_use":
                    continue
                implementation = TOOL_IMPLEMENTATIONS[block.name]
                result = implementation(block.input)
                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": str(result),
                    }
                )
            messages.append({"role": "user", "content": tool_results})

        return "Reached max tool-call iterations without a final answer."
