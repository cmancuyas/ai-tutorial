"""
Shared setup used by every lesson: reads your .env file and creates the AI client.

You don't run this file directly. The lessons do:   from ai_client import client, MODEL
(Like a shared service class you register once in Program.cs.)
"""

import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # copies the values from .env into environment variables

ENDPOINT = os.getenv("AI_ENDPOINT", "")
API_KEY = os.getenv("AI_API_KEY", "")
MODEL = os.getenv("AI_MODEL", "")
PRICE_INPUT = float(os.getenv("PRICE_INPUT_PER_MILLION", "0"))
PRICE_OUTPUT = float(os.getenv("PRICE_OUTPUT_PER_MILLION", "0"))

# Stop early with a clear message if the .env file is missing or not filled in.
if not ENDPOINT or not API_KEY or not MODEL or "your-" in ENDPOINT + API_KEY + MODEL:
    print("Setup needed: your .env file is missing or still has the example values.")
    print("Follow README.md, Part A (Azure) and Step 6 (.env file).")
    sys.exit(1)

client = OpenAI(base_url=ENDPOINT, api_key=API_KEY)


def cost_usd(input_tokens: int, output_tokens: int) -> float:
    """How much a call cost, in US dollars."""
    return (input_tokens * PRICE_INPUT + output_tokens * PRICE_OUTPUT) / 1_000_000
