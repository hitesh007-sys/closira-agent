import json
import os
from datetime import datetime

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)


def get_session_id():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def log_conversation(session_id: str, history: list):
    """Save full conversation history to a JSON log file."""
    path = os.path.join(LOG_DIR, f"conversation_{session_id}.json")
    with open(path, "w") as f:
        json.dump({"session_id": session_id, "history": history}, f, indent=2)
    print(f"\n📁 Conversation saved to {path}")


def log_escalation(session_id: str, reason: str, trigger_message: str):
    """Log escalation events separately for review."""
    path = os.path.join(LOG_DIR, f"escalation_{session_id}.json")
    entry = {
        "session_id": session_id,
        "timestamp": datetime.now().isoformat(),
        "escalation_reason": reason,
        "trigger_message": trigger_message
    }
    with open(path, "w") as f:
        json.dump(entry, f, indent=2)
    print(f"🚨 Escalation logged to {path}")


def log_summary(session_id: str, summary: dict):
    """Save session summary to a JSON file."""
    path = os.path.join(LOG_DIR, f"summary_{session_id}.json")
    with open(path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"📋 Summary saved to {path}")