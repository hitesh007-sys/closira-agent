# Test Transcript 3 — Escalation Trigger (Complaint / Anger)

**Scenario:** Customer expresses frustration/complaint.  
**Expected behaviour:** AI detects sentiment, escalates immediately with reason logged.  
**Stage:** FAQ → Escalation (Rule-based keyword detection)

---

**Aria:** Hello! Welcome to Bloom Aesthetics Clinic. 🌸 How can I help you today?

**Customer:** I came in last week and the results are terrible. This is completely unacceptable — I want to speak to a manager right now.

**[HARD ESCALATION TRIGGERED — Rule-based layer]**
- Keyword matched: "unacceptable", "speak to a manager"
- Reason: Customer expressed frustration/complaint + requested human agent
- Logged to: logs/escalation_[session_id].json
- Note: This was caught BEFORE the API call — no API cost incurred

**Aria:** I want to make sure you get the best support possible. I'm connecting you with a member of our team right now — they'll be in touch shortly. Thank you for your patience. 🌸

---

**Session escalated. Ended.**

**Summary:**
- Customer intent: Complaint about treatment results
- Details collected: None (escalated immediately)
- SOP gaps: Post-treatment complaint handling not in SOP
- Escalation: Yes — customer complaint + request for manager
- Recommended action: Senior staff member to call customer within 1 hour to resolve complaint