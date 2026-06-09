# Survey Sensum Chain

A synthetic e-commerce survey response generator that uses persona archetypes and an LLM (via Groq) to produce realistic, coherent customer satisfaction survey data.

## What It Does

Generates `N` survey responses where each response is driven by a customer persona — ensuring answers across all questions are logically consistent with each other.

Each response contains:
| Field | Description |
|---|---|
| Q1 | Overall Satisfaction (1–5) |
| Q2 | Likelihood to Recommend / NPS (0–10) |
| Q3 | Product Category (Electronics, Clothing, Home, Other) |
| Q4 | Delivery On Time (Yes / No) |
| Q5 | Open-text feedback (LLM-generated) |

Output is saved to `output/responses.csv`.

## How It Works

1. **Pick a Persona** — one of 5 archetypes is selected (e.g., `happy_loyal`, `frustrated_late_delivery`) with weighted probability
2. **Sample Numeric Answers** — Q1–Q4 are sampled from that persona's probability distributions; NPS is clamped to stay consistent with the satisfaction score
3. **Generate Open Text (Q5)** — a LangChain chain sends context (satisfaction, NPS, category, delivery, sentiment) to Groq's `llama-3.1-8b-instant` and returns a short feedback comment
4. **Export** — all responses are written to CSV with summary stats printed to console

## Project Structure

```
survey_sensum_chain/
├── main.py               # Entry point, CLI args, CSV export
├── generator.py          # Core response generation loop
├── persona.py            # Persona archetypes and sampling logic
├── llm_chain.py          # LangChain + Groq chain for open-text Q5
├── survey_definition.py  # Survey schema (question types and options)
├── requirements.txt
└── .env                  # Your Groq API key (not committed)
```

## Setup

**1. Clone the repo and install dependencies**
```bash
git clone <repo-url>
cd survey_sensum_chain
pip install -r requirements.txt
```

**2. Add your Groq API key**

Create a `.env` file in the project root:
```
GROQ_API_KEY=your_groq_api_key_here
```

Get a free key at [console.groq.com](https://console.groq.com).

**3. Run**
```bash
python main.py              # Generate 200 responses (default)
python main.py --n 50       # Generate 50 responses
python main.py --no-llm     # Skip LLM, use fallback text
```

## Personas

| Persona | Weight | Behavior |
|---|---|---|
| `happy_loyal` | 25% | High satisfaction, high NPS, 95% on-time delivery |
| `satisfied_casual` | 30% | Mostly satisfied, moderate NPS |
| `neutral_indifferent` | 20% | Mixed experience, centered around 3/5 |
| `frustrated_late_delivery` | 15% | Low scores, only 10% on-time delivery |
| `disappointed_quality` | 10% | Quality complaints, low satisfaction |

## Dependencies

- [LangChain](https://github.com/langchain-ai/langchain) — LLM chain pipeline
- [langchain-groq](https://github.com/langchain-ai/langchain/tree/master/libs/partners/groq) — Groq integration
- [pandas](https://pandas.pydata.org/) — DataFrame and CSV export
- [python-dotenv](https://github.com/theskumar/python-dotenv) — Environment variable loading
