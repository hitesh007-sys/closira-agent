# Test Transcript 5 — Full Conversation with Session Summary

**Scenario:** Full end-to-end conversation covering FAQ, qualification, and session summary.  
**Expected behaviour:** AI handles multiple topics, collects qualification data, generates structured summary at end.  
**Stages:** FAQ → Qualify → Summary (Stages 1, 2, 4)

---

**Aria:** Hello! Welcome to Bloom Aesthetics Clinic. 🌸 How can I help you today?

**Customer:** Hi! What days are you open?

**Aria:** We're open Monday to Saturday, 9am to 7pm. Is there anything else I can help you with? 🌸

**Customer:** Great. What's included in a free consultation?

**Aria:** Our free consultation is a relaxed conversation with one of our practitioners to discuss your goals and which treatments might suit you best — no commitment or pressure at all! 🌸

**Customer:** I'm thinking about Botox. How long does it last?

**Aria:** Botox results typically last around 3 to 4 months, and our treatments start from £200. A free consultation is a great first step to find out what's right for you! 🌸

**Customer:** That sounds good, I'd like to book.

**Aria:** Wonderful! May I ask — is this your first time considering Botox? 🌸

**Customer:** Yes, first time!

**Aria:** How exciting! Are you looking to book for yourself, or on behalf of someone else? 🌸

**Customer:** Just for myself.

**Aria:** Perfect. When were you hoping to come in — do you have a timeframe in mind? 🌸

**Customer:** Probably in the next couple of weeks.

**Aria:** Lovely — we'd be happy to get you in soon! You can book via WhatsApp or our website, and we require 24 hours notice if you ever need to cancel. Looking forward to welcoming you! 🌸

**Customer:** exit

---

**Session ended.**

**Generated Summary:**
```json
{
  "customer_intent": "First-time customer enquiring about Botox pricing and booking a consultation",
  "details_collected": {
    "name": null,
    "treatment_interest": "Botox",
    "booking_intent": "yes",
    "timeframe": "Next 2 weeks",
    "first_time": "Yes",
    "booking_for": "Self"
  },
  "sop_gaps": [],
  "escalation_occurred": false,
  "escalation_reason": null,
  "recommended_next_action": "Send WhatsApp booking confirmation link; high-intent lead with clear timeline — follow up within 24 hours"
}
```