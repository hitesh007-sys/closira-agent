# 🌸 Closira AI Support Agent — Bloom Aesthetics Clinic

A Python-based AI customer support workflow built with the OpenAI API. Handles inbound customer enquiries using a structured SOP, qualifies leads, detects escalation triggers, and generates conversation summaries.

---

## 📁 Project Structure

closira-agent/
├── main.py                  # Entry point — CLI conversation loop
├── agent.py                 # Core AI logic, API calls, state management
├── sop.py                   # SOP data loader and formatter
├── prompts.py               # All system prompts (centralised)
├── logger.py                # Conversation and escalation logging
├── sop_data.json            # SOP knowledge base (single source of truth)
├── stages/
│   ├── faq.py               # Stage 1: FAQ answering helpers
│   ├── qualify.py           # Stage 2: Lead qualification questions
│   ├── escalation.py        # Stage 3: Rule-based escalation detection
│   └── summary.py           # Stage 4: Summary parsing and formatting
├── logs/                    # Auto-generated session logs
├── test_transcripts/        # Sample conversations for each behaviour
├── prompt_design.md         # Prompt design decisions and rationale
└── README.md

---

## ⚙️ Setup Instructions

### Prerequisites
- Python 3.10 or higher
- An OpenAI API key ([get one here](https://platform.openai.com/api-keys))

### 1. Clone the repository

git clone https://github.com/hitesh007-sys/closira-agent.git
cd closira-agent

### 2. Install dependencies

pip install openai python-dotenv

### 3. Configure your API key

Create a `.env` file in the project root:

OPENAI_API_KEY=your_api_key_here

> ⚠️ Never commit your `.env` file. It is excluded via `.gitignore`.

### 4. Run the agent

python main.py

---

## 🧠 How It Works — The 4 Stages

| Stage | What It Does |
|-------|-------------|
| **1. FAQ Answering** | Answers questions strictly from `sop_data.json`. Will not guess or hallucinate. |
| **2. Lead Qualification** | Asks 3 structured questions when buying intent is detected. |
| **3. Escalation Detection** | Dual-layer detection: rule-based keyword check + AI confidence flag. |
| **4. Conversation Summary** | Structured JSON summary generated at session end. |

---

## 🗂️ SOP Data

The AI operates **exclusively** from `sop_data.json`:

- **Business:** Bloom Aesthetics Clinic
- **Hours:** Monday–Saturday, 9am–7pm
- **Services:** Botox (from £200), Fillers (from £250), Free Consultation
- **Booking:** WhatsApp or website; 24hr cancellation policy
- **Escalate if:** complaint, medical question, pricing negotiation, or more than 2 unanswered questions

---

## 🚨 Escalation Logic

Escalation uses two layers for reliability:

**Layer 1 — Rule-based (instant, no API call needed):**
Keywords like "complaint", "manager", "allergic", "discount", "sue" trigger immediate escalation.

**Layer 2 — AI-flagged:**
The AI returns `"escalate": true` in its JSON when it detects low confidence, out-of-scope questions, or negative sentiment.

Both layers log to `logs/escalation_<session_id>.json`.

---

## 📋 Test Transcripts

See the `test_transcripts/` folder for sample conversations covering:

1. In-SOP question (Botox pricing)
2. Out-of-scope question
3. Escalation trigger (complaint/anger)
4. Lead qualification flow
5. Full conversation with summary

---

## 🧪 Running Test Scenarios

Test 1 — In-SOP
"What are your Botox prices?"

Test 2 — Out of scope
"Do you offer laser hair removal?"

Test 3 — Escalation
"This is unacceptable, I want to speak to a manager"

Test 4 — Qualification
"I'm interested in booking a treatment"

Test 5 — Full session + summary
Type 'exit' or 'quit' to trigger summary generation

---

## ⚠️ Known Limitations & Trade-offs

| Limitation | Reason / Trade-off |
|------------|--------------------|
| No persistent memory across sessions | By design — each session is stateless for privacy |
| JSON parsing may occasionally fail | Handled with safe fallback; triggers human escalation |
| No web or WhatsApp interface | CLI only, as per assignment requirements |
| SOP is static JSON | Sufficient for demo; production would use a database |

---

## 📦 Dependencies

openai>=1.0.0
python-dotenv>=1.0.0

No LangChain, vector databases, Docker, or complex frameworks used. Pure Python.