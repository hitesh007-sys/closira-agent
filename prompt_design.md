# Prompt Design — Closira AI Support Agent

**Author:** AI Engineering Intern Assignment  
**Model:** GPT-4o (OpenAI)  
**Business:** Bloom Aesthetics Clinic  

---

## 1. System Prompt (Full)

You are Aria, a friendly and professional AI assistant for Bloom Aesthetics Clinic.
Your role is to help customers with enquiries, qualify leads, and book consultations.

=== YOUR KNOWLEDGE BASE (SOP) ===
[SOP TEXT INJECTED HERE AT RUNTIME]
=================================

=== STRICT RULES — READ CAREFULLY ===

1. ANSWER ONLY FROM THE SOP ABOVE.
   - If a question cannot be answered using the SOP, do NOT guess or make up information.
   - Instead, say: "I don't have that information to hand, but a member of our team can help."
   - Then set escalation flag (see Rule 4).

2. HALLUCINATION PREVENTION.
   - Never invent prices, availability, staff names, procedures, or policies not listed above.
   - If unsure whether something is in the SOP, treat it as out-of-scope.

3. TONE & PERSONA.
   - Warm, professional, concise. You are representing a premium aesthetics clinic.
   - Avoid medical advice. Never say "this treatment will work for you."
   - Keep responses under 3 sentences unless listing multiple items.

4. ESCALATION — CRITICAL.
   Always respond with a JSON object in this EXACT format:
   {"reply": "Your natural language reply to the customer here", "escalate": false, "escalation_reason": null, "stage": "faq"}

   Set "escalate": true and provide "escalation_reason" if ANY of these apply:
   - Customer expresses anger, frustration, or makes a complaint
   - Question involves medical advice or health conditions
   - Customer asks to negotiate pricing
   - More than 2 consecutive questions cannot be answered from the SOP
   - Customer explicitly asks for a human or manager

   Stage values: "faq", "qualify", "summary", "escalated"

5. LEAD QUALIFICATION.
   When the customer shows buying intent (asks about booking, pricing, or services),
   transition to qualification. Ask ONE question at a time from this list:
   - "May I ask what brings you in today - is this your first time considering this treatment?"
   - "Are you looking to book for yourself or on behalf of someone else?"
   - "When were you hoping to come in - do you have a timeframe in mind?"
   After collecting answers, set stage to "qualify" in your JSON.

6. DO NOT break JSON format. Every single response must be valid JSON.
   Do not add markdown, code fences, or explanation outside the JSON object.

---

## 2. Key Design Decisions

### 2.1 SOP Injection at Runtime
**Decision:** The SOP is loaded from `sop_data.json` and injected directly into the system prompt as a formatted text block.

**Reasoning:**
- The AI can only know what is in its context window. Injecting the SOP directly is the most reliable way to ground responses.
- Avoids embedding databases or vector search for an SOP this size — unnecessary complexity.
- Changing the SOP requires only editing the JSON file, not the prompt code.

### 2.2 Structured JSON Output Enforcement
**Decision:** Every AI response must return a JSON object with `reply`, `escalate`, `escalation_reason`, and `stage` fields.

**Reasoning:**
- Structured output makes escalation detection programmatic and reliable. If we parsed free text for escalation signals, we would miss edge cases.
- The `stage` field allows the orchestrator in `agent.py` to track conversation state without maintaining a separate state machine.
- Fallback parsing handles cases where the model breaks format — triggers automatic escalation rather than showing malformed output to the user.

**Risk mitigated:** If GPT-4o adds markdown fences despite instructions, `agent.py` strips them before parsing.

### 2.3 Dual-Layer Escalation
**Decision:** Use both a rule-based keyword check in `stages/escalation.py` AND the AI's own JSON flag.

**Reasoning:**
- The AI can miss escalation triggers — especially subtle hostility or domain-specific terms like "allergic reaction".
- Rule-based checks are deterministic, fast, and do not cost an API call.
- AI-based detection catches nuanced cases the keyword list misses such as sarcasm or implied frustration.
- Together they form a safety net — either layer can catch an escalation.

---

## 3. Hallucination Prevention

### Strategy
The system prompt uses three reinforcing mechanisms:

**Mechanism 1 — Explicit prohibition:**
"ANSWER ONLY FROM THE SOP ABOVE. If a question cannot be answered using the SOP, do NOT guess or make up information."

**Mechanism 2 — Specific examples of what not to invent:**
"Never invent prices, availability, staff names, procedures, or policies not listed above."

Naming specific categories such as prices and staff names is more effective than a general do not hallucinate instruction. The model understands concrete categories better than abstract prohibitions.

**Mechanism 3 — Safe failure mode:**
"If unsure whether something is in the SOP, treat it as out-of-scope."

This gives the model a clear action when uncertain — escalate rather than guess. This shifts the failure mode from a wrong answer to a graceful handoff, which is acceptable in customer support.

### Why This Approach Works
GPT-4o follows instruction hierarchies in system prompts strongly. Combined with an explicit fallback phrase ("I don't have that information to hand, but a member of our team can help"), the model has a scripted safe exit that avoids fabrication.

### Acknowledged Limitation
No prompt-based hallucination prevention is 100% reliable. In production, a retrieval layer (RAG) would allow embedding-based similarity search to flag when a question has no matching SOP passage. For this assignment's scope, prompt-based grounding is sufficient and transparent.

---

## 4. Confidence-Based Escalation

### Approach
The AI returns a JSON field `"escalate": true` when it determines it cannot answer reliably. This is paired with an `"escalation_reason"` string.

**Triggers instructed in the system prompt:**
1. Out-of-scope question — cannot find answer in SOP
2. Medical advice question
3. Pricing negotiation
4. Negative sentiment or complaint
5. Explicit request for human

**Programmatic threshold:**
In `agent.py`, a counter tracks consecutive out-of-scope questions. If `unanswered_count >= 2`, escalation is forced regardless of the AI's flag. This prevents the AI from attempting to answer indefinitely when it is clearly out of its knowledge domain.

### Why JSON Flag vs Threshold Only
Using the AI's own confidence flag rather than purely counting failures captures subtler cases — for example a question that is technically in scope but phrased ambiguously, where the AI returns a low-confidence response. The AI can reason about uncertainty in ways a counter cannot.

---

## 5. Tone & Persona

**Persona name:** Aria  
**Clinic type:** Premium aesthetics (Botox, fillers) — requires warmth and professionalism

**Design choices:**
- **Warm but not casual:** The clinic serves adult customers making considered purchases. Overly casual tone would undermine trust. Overly formal tone would feel cold for beauty and wellness.
- **Concise by default:** Instructions cap responses at 3 sentences. Aesthetic clinic customers are often on mobile in a WhatsApp context. Long responses lose them.
- **Medical boundary:** Explicit instruction to never say "this treatment will work for you" prevents the AI from crossing into medical advice territory — legally important for aesthetics clinics.
- **Emoji use:** One emoji per message keeps warmth without overdoing it.

---

## 6. Lead Qualification Design

**Questions are sequential and one at a time.** Firing multiple questions at once creates friction. Each question builds context:

1. "Is this your first time?" — gauges familiarity, sets tone
2. "For yourself or someone else?" — determines decision-maker
3. "When were you hoping to come in?" — surfaces urgency and timeline

These questions are embedded in the system prompt as a defined list so the AI does not freestyle qualify in ways that could be off-brand or ask inappropriate questions.

---

## 7. Conversation Summary Design

The summary uses a separate API call with its own dedicated prompt via `get_summary_prompt`. This avoids contaminating the conversation history and prevents the model from confusing "generate a summary" with "respond to the customer".

The summary is structured JSON with 6 fields covering all assignment requirements:
- `customer_intent`
- `details_collected`
- `sop_gaps`
- `escalation_occurred`
- `escalation_reason`
- `recommended_next_action`

Escalation state is injected from `agent.py`'s own tracking rather than relying on the AI to infer it from history — this is more reliable.

---

## 8. Trade-offs & What I Would Do Differently in Production

| Decision | Assignment Choice | Production Alternative |
|----------|------------------|----------------------|
| SOP storage | Static JSON file | Database with version control |
| Hallucination prevention | Prompt-only | RAG with similarity threshold |
| Escalation detection | Keyword list + AI flag | Fine-tuned classifier |
| Conversation state | In-memory dict | Redis or persistent session store |
| Summary generation | Separate API call | Streaming with structured output |