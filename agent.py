import json
import os
from groq import Groq
from dotenv import load_dotenv

from sop import load_sop
from prompts import get_system_prompt, get_summary_prompt
from stages.escalation import check_hard_escalation, format_escalation_message
from stages.summary import parse_summary
from logger import log_escalation, log_summary

load_dotenv()

MAX_UNANSWERED = 2
MODEL = "llama-3.3-70b-versatile"


class ClosiraAgent:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.sop_text = load_sop()
        self.system_prompt = get_system_prompt(self.sop_text)
        self.history = []
        self.escalated = False
        self.escalation_reason = None
        self.unanswered_count = 0
        self.stage = "faq"

    def _call_groq(self, messages: list) -> str:
        """Make API call to Groq. Returns raw text content."""
        full_messages = [{"role": "system", "content": self.system_prompt}] + messages
        response = self.client.chat.completions.create(
            model=MODEL,
            max_tokens=1024,
            messages=full_messages
        )
        return response.choices[0].message.content

    def _parse_ai_response(self, raw: str) -> dict:
        """
        Parse AI's JSON response safely.
        If parsing fails, return a safe fallback that triggers escalation.
        """
        try:
            clean = raw.strip()
            if clean.startswith("```"):
                parts = clean.split("```")
                clean = parts[1].lstrip("json").strip() if len(parts) > 1 else clean
            return json.loads(clean)
        except json.JSONDecodeError:
            return {
                "reply": raw.strip(),
                "escalate": True,
                "escalation_reason": "AI response could not be parsed - flagged for human review",
                "stage": "escalated"
            }

    def respond(self, user_message: str) -> str:
        if self.escalated:
            return "Your enquiry has been passed to our team. They'll be in touch very soon! 🌸"

        hard_flag, hard_reason = check_hard_escalation(user_message)
        if hard_flag:
            self._trigger_escalation(hard_reason, user_message)
            return format_escalation_message()

        self.history.append({"role": "user", "content": user_message})

        raw_response = self._call_groq(self.history)
        parsed = self._parse_ai_response(raw_response)

        reply = parsed.get("reply", "I'm sorry, I didn't catch that. Could you rephrase?")
        ai_escalate = parsed.get("escalate", False)
        escalation_reason = parsed.get("escalation_reason", None)
        self.stage = parsed.get("stage", self.stage)

        if ai_escalate and escalation_reason and "out-of-scope" in escalation_reason.lower():
            self.unanswered_count += 1
        else:
            self.unanswered_count = 0

        if self.unanswered_count >= MAX_UNANSWERED:
            ai_escalate = True
            escalation_reason = f"More than {MAX_UNANSWERED} consecutive questions could not be answered from SOP"

        if ai_escalate and escalation_reason:
            self._trigger_escalation(escalation_reason, user_message)
            reply = format_escalation_message()

        self.history.append({"role": "assistant", "content": reply})
        return reply

    def _trigger_escalation(self, reason: str, trigger_message: str):
        self.escalated = True
        self.escalation_reason = reason
        log_escalation(self.session_id, reason, trigger_message)
        print(f"\n🚨 ESCALATION TRIGGERED: {reason}")

    def generate_summary(self) -> dict:
        if not self.history:
            return {"error": "No conversation to summarise"}

        summary_prompt = get_summary_prompt(self.history)

        response = self.client.chat.completions.create(
            model=MODEL,
            max_tokens=1024,
            messages=[{"role": "user", "content": summary_prompt}]
        )

        raw_summary = response.choices[0].message.content
        summary = parse_summary(raw_summary)

        summary["escalation_occurred"] = self.escalated
        if self.escalated:
            summary["escalation_reason"] = self.escalation_reason

        log_summary(self.session_id, summary)
        return summary