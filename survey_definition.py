"""
Survey schema definition.
Each question has: id, text, type, and options (if applicable).
Types: 'rating', 'nps', 'single_choice', 'open_text'
"""

SURVEY = {
    "title": "E-commerce Customer Satisfaction",
    "questions": [
        {
            "id": "q1_satisfaction",
            "text": "Overall satisfaction?",
            "type": "rating",
            "min": 1,
            "max": 5,
        },
        {
            "id": "q2_nps",
            "text": "Likelihood to recommend?",
            "type": "nps",
            "min": 0,
            "max": 10,
        },
        {
            "id": "q3_category",
            "text": "Category purchased?",
            "type": "single_choice",
            "options": ["Electronics", "Clothing", "Home", "Other"],
        },
        {
            "id": "q4_delivery",
            "text": "Was delivery on time?",
            "type": "single_choice",
            "options": ["Yes", "No"],
        },
        {
            "id": "q5_improve",
            "text": "What could we improve?",
            "type": "open_text",
        },
    ],
}
