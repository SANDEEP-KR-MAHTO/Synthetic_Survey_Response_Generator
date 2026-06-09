"""
Persona archetypes that drive coherent, internally consistent responses.
Each persona defines probability weights for numeric/choice answers.
"""

import random

PERSONAS = [
    {
        "name": "happy_loyal",
        "description": "Frequent buyer, very satisfied, always gets timely delivery",
        "weight": 0.25,
        "satisfaction_weights": [0.02, 0.03, 0.10, 0.35, 0.50],
        "nps_weights":          [0.01, 0.01, 0.01, 0.01, 0.01,
                                  0.02, 0.05, 0.14, 0.24, 0.25, 0.25],
        "delivery_on_time_prob": 0.95,
        "category_weights": [0.30, 0.30, 0.25, 0.15],
    },
    {
        "name": "satisfied_casual",
        "description": "Occasional buyer, mostly satisfied, delivery usually fine",
        "weight": 0.30,
        "satisfaction_weights": [0.02, 0.05, 0.18, 0.45, 0.30],
        "nps_weights":          [0.01, 0.01, 0.02, 0.03, 0.05,
                                  0.08, 0.15, 0.25, 0.20, 0.12, 0.08],
        "delivery_on_time_prob": 0.80,
        "category_weights": [0.25, 0.35, 0.25, 0.15],
    },
    {
        "name": "neutral_indifferent",
        "description": "Indifferent shopper, mixed experience, average scores",
        "weight": 0.20,
        "satisfaction_weights": [0.05, 0.15, 0.50, 0.20, 0.10],
        "nps_weights":          [0.02, 0.03, 0.05, 0.08, 0.10,
                                  0.20, 0.20, 0.15, 0.10, 0.05, 0.02],
        "delivery_on_time_prob": 0.65,
        "category_weights": [0.20, 0.30, 0.30, 0.20],
    },
    {
        "name": "frustrated_late_delivery",
        "description": "Had a bad delivery experience, low satisfaction",
        "weight": 0.15,
        "satisfaction_weights": [0.40, 0.35, 0.15, 0.07, 0.03],
        "nps_weights":          [0.20, 0.20, 0.18, 0.15, 0.10,
                                  0.07, 0.05, 0.03, 0.01, 0.01, 0.00],
        "delivery_on_time_prob": 0.10,
        "category_weights": [0.35, 0.25, 0.25, 0.15],
    },
    {
        "name": "disappointed_quality",
        "description": "Product quality issue, moderately unhappy",
        "weight": 0.10,
        "satisfaction_weights": [0.25, 0.40, 0.25, 0.07, 0.03],
        "nps_weights":          [0.10, 0.15, 0.18, 0.20, 0.15,
                                  0.10, 0.07, 0.03, 0.01, 0.01, 0.00],
        "delivery_on_time_prob": 0.60,
        "category_weights": [0.40, 0.30, 0.20, 0.10],
    },
]

# NPS clamp: prevents impossible Q1/Q2 combinations
NPS_CLAMP = {
    1: (0, 3),
    2: (0, 5),
    3: (3, 7),
    4: (5, 9),
    5: (7, 10),
}


def pick_persona() -> dict:
    weights = [p["weight"] for p in PERSONAS]
    return random.choices(PERSONAS, weights=weights, k=1)[0]


def sample_rating(weights: list, min_val: int) -> int:
    indices = list(range(len(weights)))
    chosen = random.choices(indices, weights=weights, k=1)[0]
    return min_val + chosen


def sample_category(options: list, weights: list) -> str:
    return random.choices(options, weights=weights, k=1)[0]


def clamp_nps(nps: int, satisfaction: int) -> int:
    lo, hi = NPS_CLAMP[satisfaction]
    return max(lo, min(hi, nps))
