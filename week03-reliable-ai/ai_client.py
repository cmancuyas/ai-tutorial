"""
Shared setup: reads .env and creates TWO clients.

- client   : normal (synchronous) calls, like Week 2
- aclient  : async calls, for running many requests at the same time (Lesson 3)

New this week: timeout and max_retries.
- timeout=30      : give up on a call after 30 seconds instead of waiting forever
- max_retries=3   : if Azure is busy (429), times out, or has a server error (5xx),
                    the SDK automatically waits and tries again, up to 3 times.
                    Lesson 2 shows how this works by building it yourself.
"""

import os
import sys

from dotenv import load_dotenv
from openai import AsyncOpenAI, OpenAI

load_dotenv()

ENDPOINT = os.getenv("AI_ENDPOINT", "")
API_KEY = os.getenv("AI_API_KEY", "")
MODEL = os.getenv("AI_MODEL", "")
PRICE_INPUT = float(os.getenv("PRICE_INPUT_PER_MILLION", "0"))
PRICE_OUTPUT = float(os.getenv("PRICE_OUTPUT_PER_MILLION", "0"))

if not ENDPOINT or not API_KEY or not MODEL or "your-" in ENDPOINT + API_KEY + MODEL:
    print("Setup needed: copy your .env file from week02-first-llm-call into this folder.")
    print("See README.md, Step 6.")
    sys.exit(1)

if ENDPOINT.rstrip("/").endswith("responses"):
    print("Your AI_ENDPOINT ends with 'responses'. Remove that word: it must end with /openai/v1/")
    sys.exit(1)

client = OpenAI(base_url=ENDPOINT, api_key=API_KEY, timeout=30, max_retries=3)
aclient = AsyncOpenAI(base_url=ENDPOINT, api_key=API_KEY, timeout=30, max_retries=3)


def cost_usd(input_tokens: int, output_tokens: int) -> float:
    """How much a call cost, in US dollars."""
    return (input_tokens * PRICE_INPUT + output_tokens * PRICE_OUTPUT) / 1_000_000
