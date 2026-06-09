"""
LangChain-based open-text generator.

Uses:
- ChatGroq          : LLM wrapper for Groq API
- PromptTemplate    : clean named-variable prompt management
- StrOutputParser   : parses LLM output directly to a clean string
- Chain (|)         : pipes prompt → LLM → parser in one readable line
"""

import os
import time
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# --- Build the LangChain chain once at module load ---

# 1. Prompt Template — named variables keep the prompt clean and reusable
prompt = PromptTemplate(
    input_variables=["satisfaction", "nps", "category", "delivery", "sentiment"],
    template=(
        "You are simulating a real e-commerce customer filling in a satisfaction survey.\n"
        "Their answers so far:\n"
        "- Overall satisfaction: {satisfaction}/5\n"
        "- Likelihood to recommend: {nps}/10\n"
        "- Category purchased: {category}\n"
        "- Delivery was: {delivery}\n"
        "- Overall sentiment: {sentiment}\n\n"
        "Write their answer to: 'What could we improve?'\n"
        "Rules:\n"
        "- 1 sentence only, short and casual like texting a friend\n"
        "- Tone MUST match the {sentiment} sentiment\n"
        "- Be specific to the {category} product and {delivery} delivery\n"
        "- Do NOT start with 'I'\n"
        "- Output only the answer text, nothing else, no quotes"
    ),
)

# 2. LLM — ChatGroq wraps the Groq API
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.9,
    max_tokens=50,
    api_key=os.environ.get("GROQ_API_KEY", ""),
)

# 3. Output Parser — strips the response to clean plain text
output_parser = StrOutputParser()

# 4. Chain — pipes prompt → LLM → parser using LangChain's | operator
chain = prompt | llm | output_parser


def generate_open_text(context: dict, retries: int = 3) -> str:
    """
    Generate open-text survey answer using the LangChain chain.
    context keys: satisfaction, nps, category, delivery_on_time
    """
    satisfaction = context["satisfaction"]
    nps = context["nps"]
    delivery = "on time" if context["delivery_on_time"] else "late"
    category = context["category"]

    # Derive sentiment from satisfaction score
    if satisfaction >= 4 and nps >= 7:
        sentiment = "positive"
    elif satisfaction <= 2 or nps <= 3:
        sentiment = "negative"
    else:
        sentiment = "mixed"

    inputs = {
        "satisfaction": satisfaction,
        "nps": nps,
        "category": category,
        "delivery": delivery,
        "sentiment": sentiment,
    }

    for attempt in range(retries):
        try:
            result = chain.invoke(inputs)
            return result.strip().strip('"')
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
            else:
                return _fallback_text(sentiment, category, delivery)


def _fallback_text(sentiment: str, category: str, delivery: str) -> str:
    """Fallback text if the LangChain chain fails. Respects delivery status."""
    cat = category.lower()
    if delivery == "late":
        if sentiment == "positive":
            return f"The {cat} product was great but getting it on time would make the experience perfect."
        elif sentiment == "negative":
            return f"The {cat} delivery was late and the overall experience was really disappointing."
        else:
            return f"The {cat} order arrived late which brought down what was otherwise an okay experience."
    else:
        if sentiment == "positive":
            return f"Everything was great with my {cat} order, keep it up!"
        elif sentiment == "negative":
            return f"The {cat} product quality did not meet my expectations despite arriving on time."
        else:
            return f"The {cat} product was decent but the description could be more accurate."
