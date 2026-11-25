"""
LESSON 1: Prompt engineering, MEASURED.

Run:   python -m uv run python 01_prompt_engineering.py

We compare two versions on the same 7 tricky comments:
  V1 = a lazy prompt:  "Classify this feedback."
  V2 = the improved prompt in feedback.py (rules + examples + "mixed")

Each comment has the answer a careful human would give ("expected").
We count how many each version gets right. That's called an EVALUATION
("eval"): instead of saying "V2 feels better", you can say "V2 scored 6/7,
V1 scored 3/7". Real AI teams decide everything this way.

IMPORTANT RULE: the test comments must be DIFFERENT from the examples
inside the prompt. Testing on your own examples is like giving students
the exam answers in advance.
"""

from typing import Literal

from pydantic import BaseModel

from ai_client import MODEL, client
from feedback import classify


# ---------------------------------------------------------------
# V1: the lazy version (like Week 2, but with almost no instructions)
# ---------------------------------------------------------------
class SimpleFeedback(BaseModel):
    sentiment: Literal["positive", "neutral", "negative"]   # note: no "mixed"
    urgent: bool


def classify_v1(comment: str) -> SimpleFeedback:
    response = client.chat.completions.parse(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Classify this feedback."},
            {"role": "user", "content": comment},
        ],
        response_format=SimpleFeedback,
        reasoning_effort="minimal",
    )
    return response.choices[0].message.parsed


# ---------------------------------------------------------------
# The test set: (comment, expected sentiment, expected urgent)
# A list of tuples. Like C#: List<(string, string, bool)>
# ---------------------------------------------------------------
TEST_SET = [
    ("Mabait ang staff pero sobrang init sa loob, walang aircon.", "mixed", False),
    ("Wow, only 5 hours of waiting. Amazing service.", "negative", False),
    ("An employee said he could 'fast-track' my license for 2000 pesos.", "negative", True),
    ("My passport appointment is tomorrow and the system still shows my payment as unpaid.", "negative", True),
    ("Ang bilis! 15 minutes lang tapos na ako.", "positive", False),
    ("The guard shouted at an elderly woman and pushed her out of the line.", "negative", True),
    ("It was fine.", "neutral", False),
]

score_v1 = 0
score_v2 = 0

for comment, expected_sentiment, expected_urgent in TEST_SET:   # unpack each tuple
    v1 = classify_v1(comment)
    v2, _ = classify(comment)     # "_" = "I don't need this value" (the cost)

    v1_correct = v1.sentiment == expected_sentiment and v1.urgent == expected_urgent
    v2_correct = v2.sentiment == expected_sentiment and v2.urgent == expected_urgent
    score_v1 += v1_correct        # True counts as 1, False as 0
    score_v2 += v2_correct

    print(f"Comment:  {comment}")
    print(f"Expected: {expected_sentiment:9} urgent={expected_urgent}")
    print(f"V1:       {v1.sentiment:9} urgent={v1.urgent}   {'OK' if v1_correct else 'WRONG'}")
    print(f"V2:       {v2.sentiment:9} urgent={v2.urgent}   {'OK' if v2_correct else 'WRONG'}")
    print(f"V2 reason: {v2.urgent_reason}")
    print("-" * 70)
    # {x:9} pads the text to 9 characters so the columns line up, like {x,-9} in C#

total = len(TEST_SET)
print(f"\nSCORE  V1 (lazy prompt):     {score_v1}/{total}")
print(f"SCORE  V2 (improved prompt): {score_v2}/{total}")


# ---------------------------------------------------------------
# YOUR TURN (experiments)
# a) Run it 2 or 3 times. Do the scores change? (AI answers vary a bit.)
#    This is why real evals use 50 to 500 test cases, not 7.
# b) Open feedback.py and delete the EXAMPLES part of SYSTEM_PROMPT.
#    Run again. Did V2's score drop? Put the examples back afterwards.
# c) Add 2 tricky comments of your own to TEST_SET, with your expected answers.
# d) Find a comment where V2 is WRONG. Then improve the RULES in feedback.py
#    until it's right, and check that the other comments are still right.
#    That loop (find a failure -> fix the prompt -> re-run the eval) IS
#    prompt engineering.
# ---------------------------------------------------------------
