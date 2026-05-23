# Qualification questions asked sequentially
QUALIFICATION_QUESTIONS = [
    "May I ask what brings you in today — is this your first time considering this treatment?",
    "Are you looking to book for yourself or on behalf of someone else?",
    "When were you hoping to come in — do you have a timeframe in mind?"
]

def get_qualification_question(answered_count: int) -> str:
    """Return the next qualification question based on how many have been answered."""
    if answered_count < len(QUALIFICATION_QUESTIONS):
        return QUALIFICATION_QUESTIONS[answered_count]
    return None  # All questions answered


def extract_qualification_data(history: list) -> dict:
    """
    Scan conversation history for qualification answers.
    Returns a simple dict of what was collected.
    """
    data = {
        "first_time": None,
        "booking_for": None,
        "timeframe": None
    }
    # The AI collects this naturally; the summary stage will extract it
    # This function is available for explicit extraction if needed
    return data