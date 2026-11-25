"""
EXERCISE (Week 2 project): classify a whole CSV file of survey comments.

Run:   python -m uv run python 04_classify_csv.py

This is a real business task: an office gets hundreds of comments and
wants to know what people complain about and which ones are urgent.
You will reuse classify() from Lesson 3.

Fill in the 4 TODOs. Run the file after each one to check your progress.
"""

import csv   # built-in CSV reader/writer, no install needed
from collections import Counter

# Reuse the Feedback class and classify() function from Lesson 3.
# (Python can't import a file that starts with a number, so we load it this way.)
import importlib
lesson3 = importlib.import_module("03_structured_output")  # its demo is skipped (see __main__ in Lesson 3)
classify = lesson3.classify

# ---------------------------------------------------------------
# Step 1: read the comments from data/comments.csv
# csv.DictReader gives you each row as a dict: {"office": "Manila", "comment": "..."}
# ---------------------------------------------------------------
with open("data/comments.csv", encoding="utf-8") as file:   # "with" = C# "using", closes the file for you
    rows = list(csv.DictReader(file))

print(f"Loaded {len(rows)} comments. Classifying...\n")

results = []      # we'll put one dict per comment in here
total_cost = 0.0

for row in rows:
    # TODO 1: call classify(row["comment"]) and unpack it into  feedback, cost
    feedback, cost = classify(row["comment"])
    
    # TODO 2: add the cost to total_cost
    total_cost += cost
    # TODO 3: append a dict to results with these keys:
    #         office, comment, sentiment, topic, urgent, summary
    #         Hint: {"office": row["office"], "sentiment": feedback.sentiment, ...}
    #pass  # "pass" means "do nothing". Delete it once you've written your code.
    results.append({
        "office": row["office"],
        "comment": row["comment"],
        "sentiment": feedback.sentiment,
        "topic": feedback.topic,
        "urgent": feedback.urgent,
        "summary": feedback.summary,
        "language": feedback.language,
    })
    print(f"Done: {row['office']} -> {feedback.sentiment}")

# ---------------------------------------------------------------
# Step 2: save the results to results.csv (open it in Excel afterwards!)
# ---------------------------------------------------------------
# TODO 4: print only the URGENT comments, with their office.
#         Hint: a for-loop over results with an if, or a list comprehension.
print("\nURGENT comments:")
for r in results:
    if r["urgent"]:
        print(f"- [{r['office']}] {r['comment']}")

if results:
    with open("results.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    print("Saved results.csv")

# ---------------------------------------------------------------
# Step 3: a small report
# Counter counts things, like LINQ .GroupBy(x => x).Select(g => (g.Key, g.Count()))
# ---------------------------------------------------------------
sentiments = Counter(r["sentiment"] for r in results)
print(f"Sentiments: {dict(sentiments)}")



print(f"\nTotal cost for {len(rows)} comments: ${total_cost:.6f}")
