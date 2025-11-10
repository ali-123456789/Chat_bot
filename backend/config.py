"""
Configuration file for model selection - GROQ (100% FREE!)
"""

# Available FREE models on Groq (all are free and fast!):
AVAILABLE_MODELS = {
    "llama-3.3": "llama-3.3-70b-versatile",  # Best quality, FREE
    "llama-3.1": "llama-3.1-70b-versatile",  # Great quality, FREE
    "llama-3.1-8b": "llama-3.1-8b-instant",  # Fastest, FREE
    "mixtral": "mixtral-8x7b-32768",         # Good for long context, FREE
    "gemma": "gemma2-9b-it",                 # Fast and efficient, FREE
}

# Change this to switch models (ALL ARE FREE on Groq!):
MODEL_NAME = "llama-3.1-8b"  # Fastest model - RECOMMENDED

# Get the selected model
SELECTED_MODEL = AVAILABLE_MODELS[MODEL_NAME]

print(f"[CONFIG] Using model: {SELECTED_MODEL}")

