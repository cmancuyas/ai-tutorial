"""
EXERCISE (Week 3 project): the RELIABLE version of your Week 2 pipeline.

Run:   python -m uv run python 05_exercise_reliable_pipeline.py

Upgrade the Week 2 pipeline with everything from this week:
  - the improved prompt (feedback.py)                    -> already used by classify_async
  - parallel processing with a semaphore                 -> TODO 2
  - if ONE comment fails, DON'T crash the whole run:
    record it as an error and keep going                  -> TODO 1
  - a report: urgent, suspicious, failures, time, cost    -> TODO 3 and 4

Fill in the 4 TODOs. Run the file after each one.
Cost: 20 small AI calls, well under 1 US cent.
"""

import asyncio
import csv
import time
from collections import Counter

from feedback import classify_async


async def process(row: dict, semaphore: asyncio.Semaphore) -> dict:
    """Classify ONE row. Always returns a dict, even if the AI call fails."""
    async with semaphore:
        # TODO 1: wrap the code below in try / except Exception as error:
        #   - in "try": keep the 3 lines below (classify, then return the dict)
        #   - in "except": return a dict with the same keys, but
        #       "sentiment": "error", "topic": "", "urgent": False,
        #       "suspicious": False, "summary": str(error), "cost": 0.0
        #   Why? With 10,000 comments, one bad comment shouldn't lose the other 9,999.
        feedback, cost = await classify_async(row["comment"])
        return {
            "office": row["office"],
            "comment": row["comment"],
            "sentiment": feedback.sentiment,
            "topic": feedback.topic,
            "urgent": feedback.urgent,
            "suspicious": feedback.suspicious_instructions,
            "summary": feedback.summary,
            "cost": cost,
        }


async def main():
    with open("data/comments.csv", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))
    print(f"Loaded {len(rows)} comments.")

    start = time.perf_counter()
    semaphore = asyncio.Semaphore(5)

    # TODO 2: run process() for EVERY row in parallel and put the answers in "results".
    #   Hint: look at how Lesson 3 uses asyncio.gather(*(... for ... in ...))
    #   Each item should be:  process(row, semaphore)
    results = []   # replace [] with your gather call (don't forget "await")

    seconds = time.perf_counter() - start
    print(f"Classified {len(results)} comments in {seconds:.1f} seconds.\n")

    # Save to results.csv (already done for you)
    if results:
        with open("results.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
        print("Saved results.csv\n")

    # Report
    print(f"Sentiments: {dict(Counter(r['sentiment'] for r in results))}")

    # TODO 3: print the URGENT comments (urgent is True), with their office.
    #   Same as Week 2's TODO 4.

    # TODO 4: print the comments that need HUMAN REVIEW:
    #   (a) the suspicious ones (suspicious is True)  -> possible prompt injection
    #   (b) the failed ones (sentiment == "error")    -> need to be re-run
    #   Print a count for each, then the list.

    total_cost = sum(r["cost"] for r in results)
    print(f"\nTotal cost: ${total_cost:.6f}")


asyncio.run(main())


# ---------------------------------------------------------------
# BONUS (after it works)
# 1. Test TODO 1: add a row to data/comments.csv with an EMPTY comment, or
#    temporarily change AI_MODEL in .env to a wrong name. Does your pipeline
#    still finish and report the failures instead of crashing?
#    (Change AI_MODEL back afterwards!)
# 2. Compare: how long did Week 2's pipeline take for 12 comments, and how
#    long does this one take for 20?
# ---------------------------------------------------------------
