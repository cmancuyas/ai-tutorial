"""
LESSON 1: Your first AI call.

Run:   python -m uv run python 01_hello_ai.py

What you learn:
- How to send a message to an AI model and read the answer
- "Messages" with roles: system (instructions) and user (the question)
- Tokens: the units the model reads and writes, and what you pay for
"""

from ai_client import MODEL, client, cost_usd

response = client.chat.completions.create(
    model=MODEL,  # your deployment name from .env
    reasoning_effort="minimal",  
    messages=[
        # SYSTEM message = instructions for how the AI should behave.
        # The user never sees it. Think of it as the AI's "job description".
        {"role": "system", "content": "You are a friendly teacher. Answer in 2 short sentences."},
        # USER message = the actual question.
        {"role": "user", "content": "What is a REST API? Explain it to a C# developer."},
    ],
)

# The answer is inside choices[0].message.content
# (There is usually exactly 1 choice.)
answer = response.choices[0].message.content
print("AI answer:")
print(answer)

# Every response tells you how many tokens were used.
# Roughly: 1 token = about 4 characters of English = about 3/4 of a word.
usage = response.usage
print()
print(f"Tokens in (your messages): {usage.prompt_tokens}")
print(f"Tokens out (the answer):   {usage.completion_tokens}")
print(f"Cost of this call:         ${cost_usd(usage.prompt_tokens, usage.completion_tokens):.6f}")


# ---------------------------------------------------------------
# YOUR TURN (experiments) - change one thing at a time and re-run
# a) Change the system message to "Answer like a pirate." What changes?
# b) Change the system message to "Answer in Tagalog." Does it work?
# c) Ask for a longer answer ("Explain in 10 sentences"). Watch the
#    output tokens and the cost go up.
# d) Remove the system message completely. How is the answer different?
# ---------------------------------------------------------------
