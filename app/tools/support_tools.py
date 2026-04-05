from langchain_core.tools import tool
import random
from datetime import datetime, timedelta

@tool
def check_class_schedule(student_id: str = "current_student") -> str:
    """Check the upcoming class schedule for a student."""
    # Mock behavior
    future_time = datetime.now() + timedelta(days=1)
    return f"Next class is scheduled for {future_time.strftime('%Y-%m-%d %H:%00')}."

@tool
def reschedule_class(current_time: str, new_time: str) -> str:
    """Reschedule a class from a current_time to a new_time."""
    # Mock behavior
    return f"Successfully rescheduled class from {current_time} to {new_time}."

@tool
def create_support_ticket(issue_description: str) -> str:
    """Create a support ticket for technical or unresolved issues."""
    ticket_id = f"TKT-{random.randint(1000, 9999)}"
    return f"Support ticket {ticket_id} created for issue: '{issue_description}'."

TOOLS = [check_class_schedule, reschedule_class, create_support_ticket]
