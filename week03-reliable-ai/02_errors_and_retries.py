"""
LESSON 2: When AI calls fail.

Run:   python -m uv run python 02_errors_and_retries.py

In production, calls WILL fail sometimes: Azure is busy (429), the network
drops, a call takes too long, or your config is wrong. A good AI engineer
knows which errors to RETRY and which to FIX.

  Retry these (temporary):   429 rate limit, timeouts, connection errors, 5xx server errors
  Don't retry (your mistake): 400 bad request, 401 wrong key, 404 wrong endpoint/model

Python's try/except = C#'s try/catch.
"""

import time

import openai   # the error classes live here: openai.NotFoundError, openai.RateLimitError...

from ai_client import MODEL, client

# ---------------------------------------------------------------
# PART A: an error you should FIX, not retry (wrong deployment name -> 404)
# ---------------------------------------------------------------
print("PART A: calling a model that doesn't exist")
try:
    client.chat.completions.create(
        model="this-model-does-not-exist",
        messages=[{"role": "user", "content": "Hi"}],
    )
except openai.NotFoundError as error:      # like: catch (NotFoundException ex)
    print(f"  Caught NotFoundError, status {error.status_code}.")
    print("  Fix: check AI_MODEL in .env. Retrying would never help here.\n")


# ---------------------------------------------------------------
# PART B: a temporary error (timeout)
# with_options() makes a copy of the client with different settings.
# timeout=0.01 seconds is impossibly short, so the call must time out.
# ---------------------------------------------------------------
print("PART B: a call with a 0.01 second timeout")
impatient_client = client.with_options(timeout=0.01, max_retries=0)
try:
    impatient_client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": "Hi"}],
        reasoning_effort="minimal",
    )
except openai.APITimeoutError:
    print("  Caught APITimeoutError. This one IS worth retrying.\n")
except openai.APIConnectionError:
    # APITimeoutError is a CHILD class of APIConnectionError, so it must be caught FIRST.
    # Same rule as C#: catch the most specific exception first.
    print("  Caught APIConnectionError (network problem). Also worth retrying.\n")


# ---------------------------------------------------------------
# PART C: build your own retry with "exponential backoff"
# Wait 1s, then 2s, then 4s... Each failure waits twice as long, giving a
# busy server time to recover instead of hammering it.
# ---------------------------------------------------------------
class TemporaryError(Exception):
    """A pretend error for our simulation. Like: class TemporaryException : Exception {}"""


def call_with_retry(func, retry_on: tuple, max_attempts: int = 4):
    """Call func(). If it raises one of the retry_on errors, wait and try again."""
    for attempt in range(1, max_attempts + 1):     # range(1, 5) = 1, 2, 3, 4
        try:
            return func()                          # success: return immediately
        except retry_on as error:
            if attempt == max_attempts:
                print(f"  Attempt {attempt} failed. Giving up.")
                raise                              # re-throw, like "throw;" in C#
            wait = 2 ** (attempt - 1)              # ** = power: 1, 2, 4, 8 seconds
            print(f"  Attempt {attempt} failed ({error}). Waiting {wait}s, then retrying...")
            time.sleep(wait)


# A pretend service that fails twice, then works.
# We count calls in a dict, because a dict can be changed inside a function
# without "global" (remember the list vs. number lesson from Week 1?).
state = {"calls": 0}


def flaky_service() -> str:
    state["calls"] += 1
    if state["calls"] < 3:
        raise TemporaryError("server busy")
    return "Success on call number " + str(state["calls"])


print("PART C: retrying a flaky service")
result = call_with_retry(flaky_service, retry_on=(TemporaryError,))
print(f"  Result: {result}\n")
# Note: (TemporaryError,) with a comma is a tuple with ONE item.
# Without the comma, Python would treat the brackets as normal brackets.


# ---------------------------------------------------------------
# PART D: retrying a REAL AI call
# "lambda: ..." is a small inline function, exactly like C#'s () => ...
# ---------------------------------------------------------------
print("PART D: a real AI call wrapped in call_with_retry")
RETRYABLE = (openai.RateLimitError, openai.APITimeoutError, openai.APIConnectionError, openai.InternalServerError)
response = call_with_retry(
    lambda: client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": "Say hello in Tagalog, in 3 words."}],
        reasoning_effort="minimal",
    ),
    retry_on=RETRYABLE,
)
print(f"  AI: {response.choices[0].message.content}\n")

print("GOOD NEWS: in real projects you rarely write this loop yourself.")
print("ai_client.py sets max_retries=3, so the OpenAI SDK already retries 429s,")
print("timeouts and 5xx errors with backoff for you. Now you know what it does.")


# ---------------------------------------------------------------
# YOUR TURN (experiments)
# a) Change flaky_service so it fails 5 times (state["calls"] < 6).
#    What happens with max_attempts=4? Wrap the PART C call in try/except
#    so the program prints a friendly message instead of crashing.
# b) In PART A, add "except openai.AuthenticationError:" for a wrong key (401).
#    Test it by temporarily using  client.with_options(api_key="wrong")
# c) Why is retrying a 404 pointless, but retrying a 429 smart? Write your
#    answer as a comment. (This is a common interview question!)
# ---------------------------------------------------------------
