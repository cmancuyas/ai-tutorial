"""
LESSON 3: Structured outputs. The most useful skill in business AI.

Run:   python -m uv run python 03_structured_output.py

Problem: normal AI answers are free text. Your code can't easily use
"The sentiment seems mostly negative, I think..." in an if-statement.

Solution: give the model a Pydantic class (like a C# DTO). The model
MUST answer in exactly that shape, and you get back a typed object.
Now the AI behaves like a normal API that returns JSON.
"""

from typing import Literal

from pydantic import BaseModel, Field

from ai_client import MODEL, client, cost_usd


# The shape we want back. Like a C# class:
#   public class Feedback { public string Sentiment; public string Topic; ... }
# Literal[...] = only these exact values are allowed (like a C# enum).
# Field(description=...) tells the AI what each field means.
class Feedback(BaseModel):
    sentiment: Literal["positive", "neutral", "negative"]
    topic: str = Field(description="Main subject in 1 to 3 words, e.g. 'waiting time', 'staff attitude'")
    urgent: bool = Field(description="True if the office should act on this quickly")
    summary: str = Field(description="One short sentence in English")
    language: Literal["english", "tagalog", "taglish"] = Field(description="The language of the comment")


SYSTEM_PROMPT = (
    "You classify citizen feedback about government office services in the Philippines. "
    "Comments may be in English, Tagalog, or Taglish."
)


def classify(comment: str) -> tuple[Feedback, float]:
    """Send one comment to the AI and get back a typed Feedback object + the cost."""
    response = client.chat.completions.parse(   # .parse (not .create) = structured output
        model=MODEL,
        reasoning_effort="minimal",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": comment},
        ],
        response_format=Feedback,               # "answer in this shape"
    )
    feedback = response.choices[0].message.parsed   # already a Feedback object!
    cost = cost_usd(response.usage.prompt_tokens, response.usage.completion_tokens)
    return feedback, cost
    # "return a, b" returns a tuple (two values), like C#'s (Feedback, double)


# "if __name__ == '__main__':" means: only run this part when THIS file is run
# directly. When another file imports classify() from here (the exercise does),
# this demo is skipped. It's like the Main() method in a C# console app.
if __name__ == "__main__":
    comments = [
        "Waited 3 hours and the staff were rude. Never again.",
        "Mabilis ang serbisyo at mabait ang guard. Salamat po!",
        "The online form keeps crashing when I upload my documents. Deadline is tomorrow!",
        "It was okay. Nothing special.",
        "Wow, only 5 hours of waiting. Amazing service."
    ]

    for comment in comments:
        feedback, cost = classify(comment)          # "unpacking" the tuple into 2 variables
        print(f"Comment:   {comment}")
        print(f"Sentiment: {feedback.sentiment}")   # typed! your editor autocompletes .sentiment
        print(f"Topic:     {feedback.topic}")
        print(f"Language:  {feedback.language}")
        print(f"Urgent:    {feedback.urgent}")
        print(f"Summary:   {feedback.summary}")
        print(f"Cost:      ${cost:.6f}")
        print("-" * 60)                             # prints 60 dashes

        # Because it's typed, normal code can use it directly:
        if feedback.urgent:
            print(">>> ALERT: send this to the office manager!\n")


# ---------------------------------------------------------------
# YOUR TURN (experiments)
# a) Add your own comments to the list, including tricky ones, e.g. sarcasm:
#    "Wow, only 5 hours of waiting. Amazing service."  Does it get it right?
# b) Add a new field to Feedback:  language: Literal["english", "tagalog", "taglish"]
#    Re-run. You changed what the AI returns just by changing a class.
# c) Add a field  score: Literal[1, 2, 3, 4, 5]  for a 1-5 rating the AI guesses
#    from the comment. (Literal with numbers works like an enum of allowed values.)
# ---------------------------------------------------------------
