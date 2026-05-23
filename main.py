import sys
from logger import get_session_id, log_conversation
from agent import ClosiraAgent
from stages.summary import format_summary_for_display

def print_banner():
    print("\n" + "="*55)
    print("  🌸  Bloom Aesthetics Clinic — AI Support Agent  🌸")
    print("="*55)
    print("  Type your message and press Enter to chat.")
    print("  Type 'quit' or 'exit' to end the session.")
    print("="*55 + "\n")


def run():
    session_id = get_session_id()
    agent = ClosiraAgent(session_id=session_id)

    print_banner()
    print(f"Aria: Hello! Welcome to Bloom Aesthetics Clinic. 🌸 How can I help you today?\n")

    # Seed the assistant's opening line into history for summary context
    agent.history.append({
        "role": "assistant",
        "content": "Hello! Welcome to Bloom Aesthetics Clinic. 🌸 How can I help you today?"
    })

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n[Session interrupted by user]")
            break

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit", "bye", "goodbye"):
            print("\nAria: Thank you for reaching out to Bloom Aesthetics Clinic. Have a lovely day! 🌸\n")
            break

        # Get AI response
        reply = agent.respond(user_input)
        print(f"\nAria: {reply}\n")

        # After escalation, offer to end session
        if agent.escalated:
            print("[Session escalated to human agent. Generating summary...]\n")
            break

    # ── End of session ───────────────────────────────────────────────────────
    log_conversation(session_id, agent.history)

    print("\n[Generating session summary...]\n")
    summary = agent.generate_summary()
    print(format_summary_for_display(summary))


if __name__ == "__main__":
    run()