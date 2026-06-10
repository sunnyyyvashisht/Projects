import os
from openai import OpenAI
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Conversation memory — stores the full chat history
conversation_history = [
    {
        "role": "system",
        "content": (
            "You are a smart, friendly, and helpful AI assistant. "
            "Answer questions clearly and concisely. "
            "If you don't know something, say so honestly."
        )
    }
]


def chat(user_message: str) -> str:
    """
    Send a user message and return the assistant's reply.
    Maintains full conversation history for context.
    """
    conversation_history.append({
        "role": "user",
        "content": user_message
    })

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation_history,
        temperature=0.7,          # 0 = focused, 1 = creative
        max_tokens=1000,
    )

    reply = response.choices[0].message.content.strip()

    conversation_history.append({
        "role": "assistant",
        "content": reply
    })

    return reply


def save_chat_history(filename: str = "chat_history.txt"):
    """Save the conversation to a text file."""
    with open(filename, "w", encoding="utf-8") as f:
        for msg in conversation_history:
            if msg["role"] == "system":
                continue
            role = "You" if msg["role"] == "user" else "Bot"
            f.write(f"{role}: {msg['content']}\n\n")
    print(f"\n💾 Chat saved to {filename}")


def main():
    """Run the chatbot in the terminal."""
    print("=" * 50)
    print("        🤖  AI Chatbot  (GPT-3.5-turbo)")
    print("=" * 50)
    print("Commands:  'quit' to exit  |  'save' to save chat")
    print("           'clear' to reset conversation history")
    print("-" * 50 + "\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nBot: Goodbye! 👋")
            break

        if not user_input:
            continue

        if user_input.lower() in ["quit", "exit", "bye"]:
            print("Bot: Goodbye! 👋")
            break

        if user_input.lower() == "save":
            save_chat_history()
            continue

        if user_input.lower() == "clear":
            # Keep only the system prompt
            conversation_history.clear()
            conversation_history.append({
                "role": "system",
                "content": "You are a smart, friendly, and helpful AI assistant."
            })
            print("Bot: Conversation cleared. Fresh start! 🧹\n")
            continue

        try:
            response = chat(user_input)
            print(f"Bot: {response}\n")
        except Exception as e:
            print(f"⚠️  Error: {e}\n")
            print("Make sure your OPENAI_API_KEY in .env is correct.\n")


if __name__ == "__main__":
    main()
