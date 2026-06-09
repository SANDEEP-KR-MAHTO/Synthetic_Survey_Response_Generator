"""
Core generation logic — same pipeline as the original project,
now using the LangChain chain for open-text generation.

Strategy:
1. Pick a persona for each respondent.
2. Sample numeric/choice answers from persona-specific weighted distributions.
3. Clamp NPS to a range consistent with satisfaction score.
4. Call the LangChain chain only for the open-text question.
"""

import random
import time
from persona import pick_persona, sample_rating, sample_category, clamp_nps
from llm_chain import generate_open_text
from survey_definition import SURVEY


def generate_one_response() -> dict:
    """Generate a single coherent survey response."""
    persona = pick_persona()
    response = {"persona": persona["name"]}
    numeric_context = {}

    for q in SURVEY["questions"]:
        qid = q["id"]

        if q["type"] == "rating":
            value = sample_rating(persona["satisfaction_weights"], q["min"])
            response[qid] = value
            numeric_context["satisfaction"] = value

        elif q["type"] == "nps":
            raw_nps = sample_rating(persona["nps_weights"], q["min"])
            value = clamp_nps(raw_nps, numeric_context["satisfaction"])
            response[qid] = value
            numeric_context["nps"] = value

        elif q["type"] == "single_choice":
            if qid == "q3_category":
                value = sample_category(q["options"], persona["category_weights"])
                response[qid] = value
                numeric_context["category"] = value

            elif qid == "q4_delivery":
                on_time = random.random() < persona["delivery_on_time_prob"]
                response[qid] = "Yes" if on_time else "No"
                numeric_context["delivery_on_time"] = on_time

        elif q["type"] == "open_text":
            # LangChain chain call — grounded in all numeric answers
            response[qid] = generate_open_text(numeric_context)
            time.sleep(2.7)  # prevent Groq free-tier rate limit

    return response


def generate_responses(n: int, verbose: bool = True) -> list[dict]:
    """Generate N survey responses with progress logging."""
    responses = []
    for i in range(n):
        if verbose and (i + 1) % 10 == 0:
            print(f"  Generated {i + 1}/{n} responses...")
        responses.append(generate_one_response())
    return responses
