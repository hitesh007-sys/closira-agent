import json

def parse_summary(raw_response: str) -> dict:
    """
    Parse the AI's JSON summary response safely.
    Falls back to a default structure if parsing fails.
    """
    try:
        # Strip any accidental markdown fences
        clean = raw_response.strip()
        if clean.startswith("```"):
            clean = clean.split("```")[1]
            if clean.startswith("json"):
                clean = clean[4:]
        return json.loads(clean)
    except (json.JSONDecodeError, IndexError):
        return {
            "customer_intent": "Could not parse summary",
            "details_collected": {},
            "sop_gaps": [],
            "escalation_occurred": False,
            "escalation_reason": None,
            "recommended_next_action": "Manual review required"
        }


def format_summary_for_display(summary: dict) -> str:
    """Format summary dict as readable CLI output."""
    lines = [
        "\n" + "="*50,
        "📋 SESSION SUMMARY",
        "="*50,
        f"🎯 Customer Intent: {summary.get('customer_intent', 'N/A')}",
        "\n📌 Details Collected:"
    ]
    
    details = summary.get("details_collected", {})
    for key, value in details.items():
        if value:
            lines.append(f"   • {key.replace('_', ' ').title()}: {value}")
    
    gaps = summary.get("sop_gaps", [])
    if gaps:
        lines.append("\n⚠️  SOP Gaps Identified:")
        for gap in gaps:
            lines.append(f"   • {gap}")
    
    escalated = summary.get("escalation_occurred", False)
    lines.append(f"\n🚨 Escalation Occurred: {'Yes' if escalated else 'No'}")
    if escalated and summary.get("escalation_reason"):
        lines.append(f"   Reason: {summary['escalation_reason']}")
    
    lines.append(f"\n✅ Recommended Next Action: {summary.get('recommended_next_action', 'N/A')}")
    lines.append("="*50 + "\n")
    
    return "\n".join(lines)