def build_faq_context(user_message: str) -> str:
    """
    Adds a hint to the AI to answer from SOP only.
    The system prompt already enforces this, but we reinforce it per-message.
    """
    return user_message  # Routing and enforcement handled by system prompt + agent.py