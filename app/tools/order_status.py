"""Mock order-status lookup tool.

Returns fake but realistic order data, including edge cases (not found,
delayed, cancelled) so downstream agents and the eval harness have more
than just the happy path to handle.
"""

_FAKE_ORDERS = {
    "ORD-1001": {
        "status": "delivered",
        "carrier": "UPS",
        "tracking_number": "1Z999AA10123456784",
        "estimated_delivery": "2026-07-05",
        "last_update": "Delivered to front door 2026-07-05 14:32",
    },
    "ORD-1002": {
        "status": "in_transit",
        "carrier": "FedEx",
        "tracking_number": "789123456789",
        "estimated_delivery": "2026-07-16",
        "last_update": "Departed regional facility, Memphis TN",
    },
    "ORD-1003": {
        "status": "delayed",
        "carrier": "USPS",
        "tracking_number": "9400111899561234567890",
        "estimated_delivery": "2026-07-22",
        "last_update": "Weather delay at origin facility",
    },
    "ORD-1004": {
        "status": "processing",
        "carrier": None,
        "tracking_number": None,
        "estimated_delivery": "2026-07-18",
        "last_update": "Order received, awaiting fulfillment",
    },
    "ORD-1005": {
        "status": "cancelled",
        "carrier": None,
        "tracking_number": None,
        "estimated_delivery": None,
        "last_update": "Cancelled by customer on 2026-07-10",
    },
}


def check_order_status(order_id: str) -> dict:
    """Look up the status of an order by ID.

    Args:
        order_id: The order identifier, e.g. "ORD-1001".

    Returns:
        A dict describing the order's current status. If the order_id
        isn't recognized, returns a dict with status "not_found" instead
        of raising, so the calling agent can handle it gracefully.
    """
    order = _FAKE_ORDERS.get(order_id.strip().upper())
    if order is None:
        return {
            "order_id": order_id,
            "status": "not_found",
            "message": f"No order found with ID {order_id!r}.",
        }
    return {"order_id": order_id.strip().upper(), **order}
