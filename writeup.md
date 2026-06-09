# Write-up: Synthetic Survey Response Generator

## Approach

Instead of asking an LLM to generate all responses at once (which produces incoherent data — e.g., a satisfaction score of 1 with a glowing open-text answer), I built a persona-first pipeline:

1. **Pick a persona** — one of 5 customer archetypes (e.g., `happy_loyal`, `frustrated_late_delivery`), selected with weighted probability
2. **Sample numeric answers** — Q1–Q4 are drawn from that persona's probability distributions; NPS is clamped to stay consistent with the satisfaction score
3. **Generate open text** — the LLM only handles Q5, and by then it already knows the satisfaction score, NPS, category, and delivery status — so it never contradicts the numbers

## Why LangChain

LangChain's pipe operator chains the prompt, LLM, and output parser into one clean line:

```
chain = prompt | llm | parser
```

- `PromptTemplate` keeps all variables (satisfaction, NPS, category, delivery, sentiment) declared upfront — no scattered string formatting
- `StrOutputParser` handles stripping raw LLM output automatically
- The chain is built once and reused for every call

The underlying model is Groq's `llama-3.1-8b-instant` (free tier, 14,400 requests/day).

## Measuring Output Quality

- **Pearson correlation (Q1 vs Q2):** Should land around 0.7–0.85. Too low means the scores feel random; too high means they look artificially perfect.
- **Sentiment alignment:** Running VADER on Q5 open-text and comparing against Q1 — negative sentiment should match low satisfaction scores. If they diverge, the prompt is not grounding the LLM properly.
- **Score distribution:** The average satisfaction score should sit around 3.8/5, matching real e-commerce benchmarks. A heavy skew toward extremes signals the persona weights need adjustment.
- **Delivery coherence:** Every response where Q4 is "No" should have a Q5 that mentions delivery or timing. This is easy to check programmatically and directly tests whether the prompt template is working.
- **Manual review:** Reading ~20 random responses by hand is the most reliable check — if they feel like something a real person would write in a post-purchase survey, the system is working.

## What I'd Improve With More Time

- **Fit distributions on real data** — current persona score distributions are hand-tuned. Even 30–50 real survey rows would give empirically grounded numbers and catch non-obvious correlations (e.g., does product category predict NPS?)
- **Add LangSmith tracing** — free at low usage; auto-logs every chain call with inputs, outputs, and latency, making it easy to spot where the LLM drifts without reading every CSV row manually
