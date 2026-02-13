from typing import Any, Dict, Callable, List

subscribers: Dict[str, List[Callable]] = {}

def subscribe(event_type: str, handler: Callable):
    if event_type not in subscribers:
        subscribers[event_type] = []
    subscribers[event_type].append(handler)

def emit(event_type: str, payload: Dict[str, Any]):
    print(f"[EVENT] {event_type} triggered with payload: {payload}")
    if event_type in subscribers:
        for handler in subscribers[event_type]:
            try:
                handler(payload)
            except Exception as e:
                print(f"Error in event handler for {event_type}: {e}")

# Pre-defined attributes for known events
NEW_CONTACT = "NEW_CONTACT"
BOOKING_CREATED = "BOOKING_CREATED"
BOOKING_REMINDER = "BOOKING_REMINDER"
FORM_PENDING = "FORM_PENDING"
FORM_OVERDUE = "FORM_OVERDUE"
INVENTORY_LOW = "INVENTORY_LOW"
STAFF_REPLY = "STAFF_REPLY"
FORM_SUBMITTED = "FORM_SUBMITTED"
