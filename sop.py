import json
import os

def load_sop(path="sop_data.json"):
    """Load and return SOP data as a formatted string for injection into prompts."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"SOP file not found at: {path}")
    
    with open(path, "r") as f:
        data = json.load(f)
    
    # Format SOP as clean readable text for the AI
    sop_text = f"""
BUSINESS: {data['business_name']}
HOURS: {data['hours']}

SERVICES:
"""
    for service in data["services"]:
        sop_text += f"- {service['name']}: from {service['price_from']}. {service['details']}\n"

    sop_text += f"""
BOOKING: Via {', '.join(data['booking']['methods'])}. {data['booking']['cancellation_policy']}.

ESCALATE IF: {', '.join(data['escalation_triggers'])}.
"""
    return sop_text.strip()


def load_sop_raw(path="sop_data.json"):
    """Return raw SOP dict for programmatic use."""
    with open(path, "r") as f:
        return json.load(f)