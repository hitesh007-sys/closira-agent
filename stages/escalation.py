# Keywords that should trigger escalation regardless of AI response
HARD_ESCALATION_KEYWORDS = [
    "complaint", "complain", "angry", "furious", "disgusting", "unacceptable",
    "speak to a human", "speak to someone", "real person", "manager",
    "sue", "refund", "legal", "allergic", "reaction", "injury", "hurt",
    "can you do it cheaper", "discount", "negotiate", "better price"
]

def check_hard_escalation(user_message: str) -> tuple[bool, str]:
    """
    Rule-based safety net: catches escalation triggers the AI might miss.
    Returns (should_escalate: bool, reason: str)
    """
    message_lower = user_message.lower()
    
    for keyword in HARD_ESCALATION_KEYWORDS:
        if keyword in message_lower:
            if any(w in keyword for w in ["complaint", "complain", "angry", "furious", "disgusting", "unacceptable"]):
                return True, f"Customer expressed frustration/complaint (detected: '{keyword}')"
            elif any(w in keyword for w in ["human", "someone", "person", "manager"]):
                return True, f"Customer requested human agent (detected: '{keyword}')"
            elif any(w in keyword for w in ["allergic", "reaction", "injury", "hurt"]):
                return True, "Medical concern raised — requires human review"
            elif any(w in keyword for w in ["cheaper", "discount", "negotiate", "price"]):
                return True, "Customer requesting pricing negotiation"
    
    return False, ""


def format_escalation_message() -> str:
    """Standard escalation message shown to customer."""
    return (
        "I want to make sure you get the best support possible. "
        "I'm connecting you with a member of our team right now — "
        "they'll be in touch shortly. Thank you for your patience. 🌸"
    )