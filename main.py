"""
Entry point: generate N synthetic survey responses and export to CSV.

Usage:
    python main.py              # generates 200 responses (default)
    python main.py --n 50       # generates 50 responses
    python main.py --no-llm     # skip LangChain, use fallback text only
"""

import argparse
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

from generator import generate_responses

OUTPUT_DIR = "output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "responses.csv")

COLUMN_LABELS = {
    "q1_satisfaction": "Q1: Overall Satisfaction (1-5)",
    "q2_nps":          "Q2: Likelihood to Recommend (0-10)",
    "q3_category":     "Q3: Category Purchased",
    "q4_delivery":     "Q4: Delivery On Time",
    "q5_improve":      "Q5: What Could We Improve",
}


def main():
    parser = argparse.ArgumentParser(description="Synthetic Survey Response Generator — LangChain version")
    parser.add_argument("--n", type=int, default=200, help="Number of responses to generate")
    parser.add_argument("--no-llm", action="store_true", help="Use fallback text only, skip LangChain")
    args = parser.parse_args()

    if args.no_llm:
        import llm_chain
        llm_chain.generate_open_text = lambda ctx, **kw: llm_chain._fallback_text(
            "positive" if ctx["satisfaction"] >= 4 else
            ("negative" if ctx["satisfaction"] <= 2 else "mixed"),
            ctx["category"],
            "on time" if ctx["delivery_on_time"] else "late",
        )
        print("Running in --no-llm mode (fallback text only).")

    print(f"\nGenerating {args.n} synthetic survey responses (LangChain version)...")
    print(f"Survey: E-commerce Customer Satisfaction\n")

    responses = generate_responses(args.n, verbose=True)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df = pd.DataFrame(responses)
    df = df.drop(columns=["persona"])
    df = df.rename(columns=COLUMN_LABELS)
    df.to_csv(OUTPUT_FILE, index=True, index_label="Response ID")

    print(f"\nDone! Saved to: {OUTPUT_FILE}")
    print("\n--- Summary Statistics ---")
    print(df["Q1: Overall Satisfaction (1-5)"].describe().round(2).to_string())
    print(f"\nDelivery on time: {(df['Q4: Delivery On Time'] == 'Yes').mean():.1%}")
    print(f"\nCategory distribution:\n{df['Q3: Category Purchased'].value_counts().to_string()}")


if __name__ == "__main__":
    main()
