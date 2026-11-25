"""
LESSON 3: Speed. Classify many comments AT THE SAME TIME.

Run:   python -m uv run python 03_async_parallel.py

In Week 2, comment 2 waited for comment 1 to finish, and so on.
Each AI call spends most of its time WAITING for Azure to answer.
With async, we send several requests and wait for all of them together.

It's the same idea as C#:
    var tasks = comments.Select(c => ClassifyAsync(c));
    var results = await Task.WhenAll(tasks);
Python:
    results = await asyncio.gather(*(classify_async(c) for c in comments))

A SEMAPHORE limits how many run at once (here: 5), so we don't flood
Azure and trigger 429 "too many requests" errors. C# has SemaphoreSlim
for exactly the same reason.

Cost: this lesson makes 20 small AI calls (well under 1 US cent).
"""

import asyncio   # Python's built-in async library
import csv
import time

from feedback import classify_async


async def main():                       # like: static async Task Main()
    with open("data/comments.csv", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))
    comments = [row["comment"] for row in rows[:10]]   # [:10] = the first 10 items, like .Take(10)

    # -----------------------------------------------------------
    # 1. ONE AT A TIME (the Week 2 way)
    # -----------------------------------------------------------
    print(f"Classifying {len(comments)} comments ONE AT A TIME...")
    start = time.perf_counter()         # a precise stopwatch, like Stopwatch.StartNew()
    for comment in comments:
        await classify_async(comment)
    one_at_a_time = time.perf_counter() - start
    print(f"  Took {one_at_a_time:.1f} seconds\n")

    # -----------------------------------------------------------
    # 2. IN PARALLEL (max 5 at the same time)
    # -----------------------------------------------------------
    semaphore = asyncio.Semaphore(5)

    async def classify_limited(comment: str):
        async with semaphore:           # wait here if 5 are already running
            return await classify_async(comment)

    print(f"Classifying {len(comments)} comments IN PARALLEL (5 at a time)...")
    start = time.perf_counter()
    results = await asyncio.gather(*(classify_limited(c) for c in comments))
    # The * "spreads" the items into separate arguments: gather(a, b, c, ...)
    in_parallel = time.perf_counter() - start
    print(f"  Took {in_parallel:.1f} seconds\n")

    print(f"Parallel was {one_at_a_time / in_parallel:.1f}x faster.\n")

    # gather() returns results in the SAME ORDER as the inputs, even though
    # they finished in a different order. So we can zip them back together.
    # zip() pairs items from two lists, like LINQ's .Zip()
    for comment, (feedback, cost) in zip(comments, results):
        print(f"[{feedback.sentiment:8}] urgent={str(feedback.urgent):5}  {comment[:60]}")


asyncio.run(main())   # starts the async program


# ---------------------------------------------------------------
# YOUR TURN (experiments)
# a) Change Semaphore(5) to Semaphore(1). How fast is it now? Why?
# b) Try Semaphore(10). Faster? (With only 10 comments, there's a limit.)
# c) Use all 20 comments: change rows[:10] to rows. (About 1 extra US cent at most.)
# ---------------------------------------------------------------
