"""
LESSON 2: A chat program that remembers the conversation.

Run:   python -m uv run python 02_chat.py
Type your messages. Type "exit" to quit.

The BIG idea of this lesson:
The AI model has NO memory. Every call starts from zero.
To make it "remember", we keep a list of all messages and send
the WHOLE list every time. That's why each turn costs a bit more
than the last: the history keeps growing.
"""

from ai_client import MODEL, client, cost_usd

# The conversation history. It starts with just the system message
messages = [
    {"role": "system", "content": "You are a helpful assistant for a C# developer learning Python. Keep answers short."},
]

total_cost = 0.0
print("Chat started. Type 'exit' to quit.\n")

while True:                                  # loop forever, until we "break"
    user_text = input("You: ")               # like Console.ReadLine()
    if user_text.strip().lower() == "exit":
        break

    messages.append({"role": "user", "content": user_text})

    response = client.chat.completions.create(model=MODEL, messages=messages, reasoning_effort="minimal")
    answer = response.choices[0].message.content

    # Save the AI's answer in the history too, so it "remembers" it next turn.
    messages.append({"role": "assistant", "content": answer})
    
    usage = response.usage
    cost = cost_usd(usage.prompt_tokens, usage.completion_tokens)
    total_cost += cost

    print(f"AI: {answer}")
    print(f"   [tokens in: {usage.prompt_tokens}, out: {usage.completion_tokens}, "
          f"cost: ${cost:.6f}, total: ${total_cost:.6f}]\n")

print(f"Goodbye! This chat cost ${total_cost:.6f} in total, over {len(messages)} messages.")


# ---------------------------------------------------------------
# YOUR TURN (experiments)
# a) Tell the AI your name, then 3 messages later ask "What's my name?"
#    It remembers, because we resend the history.
# b) Watch "tokens in" grow every turn. Why does that happen?
# c) Comment out the line  messages.append({"role": "assistant", ...})
#    and try (a) again. What happens now, and why?
# d) Add a command: if the user types "reset", clear the history back to
#    only the system message. Hint: messages = messages[:1]
# ---------------------------------------------------------------
