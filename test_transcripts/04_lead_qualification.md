# Test Transcript 4 — Lead Qualification Flow

**Scenario:** Customer shows buying intent; AI transitions to qualification.  
**Expected behaviour:** AI asks 3 structured questions one at a time, collects answers.  
**Stage:** FAQ → Qualify (Stage 2)

---

**Aria:** Hello! Welcome to Bloom Aesthetics Clinic. 🌸 How can I help you today?

**Customer:** I'm interested in getting some work done — I've been thinking about fillers.

**Aria:** That's wonderful — fillers are one of our most popular treatments! We offer dermal fillers from £250, with results lasting 6–12 months. May I ask what brings you in today — is this your first time considering this treatment? 🌸

**Customer:** Yes, it's my first time. I've been thinking about it for a while.

**Aria:** How exciting — first-time consultations are always a lovely experience here! Are you looking to book for yourself, or on behalf of someone else? 🌸

**Customer:** For myself, yes.

**Aria:** Perfect! And when were you hoping to come in — do you have a timeframe in mind? 🌸

**Customer:** Ideally sometime next month, around mid-July.

**Aria:** Mid-July works beautifully — we'd love to get you booked in for a free consultation first so we can talk through exactly what you're looking for. You can book via WhatsApp or our website at your convenience! 🌸

---

**Session ended by customer typing 'quit'.**

**Summary:**
```json
{
  "customer_intent": "First-time enquiry about dermal fillers, interested in booking",
  "details_collected": {
    "treatment_interest": "Dermal fillers",
    "booking_intent": "yes",
    "timeframe": "Mid-July",
    "first_time": "Yes",
    "booking_for": "Self"
  },
  "sop_gaps": [],
  "escalation_occurred": false,
  "escalation_reason": null,
  "recommended_next_action": "Send booking link via WhatsApp; priority lead — clear intent and timeline"
}
```