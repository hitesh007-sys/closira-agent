# Test Transcript 2 — Out-of-Scope Question

**Scenario:** Customer asks about a service not in the SOP.  
**Expected behaviour:** AI acknowledges it doesn't have that info, escalates rather than guessing.  
**Stage:** FAQ → Escalation

---

**Aria:** Hello! Welcome to Bloom Aesthetics Clinic. 🌸 How can I help you today?

**Customer:** Do you offer laser hair removal?

**Aria:** I don't have that information to hand, but a member of our team can help clarify exactly which treatments we offer. I'm connecting you with someone now — they'll be in touch shortly! 🌸

**[ESCALATION TRIGGERED]**
- Reason: Out-of-scope question — laser hair removal not found in SOP
- Logged to: logs/escalation_[session_id].json

**Customer:** OK thanks

**Aria:** Your enquiry has been passed to our team. They'll be in touch very soon! 🌸

---

**Post-escalation session ended.**

**Summary:**
- Customer intent: Enquiry about laser hair removal
- SOP gaps: "Do you offer laser hair removal?" — not covered in SOP
- Escalation: Yes — out-of-scope question
- Recommended action: Human agent to confirm service offering and update SOP if needed