import os
from transformers import pipeline

# Get absolute path to the model directory
current_dir = os.path.dirname(os.path.abspath(__file__))
local_model_path = os.path.join(os.path.dirname(current_dir), "models", "emotion-model")

# Make sure model path exists
if not os.path.exists(local_model_path):
    raise FileNotFoundError(
        f"Model not found at {local_model_path}. "
        "Please run download_model.py first to download the model."
    )

# Initialize the pipeline without local_files_only parameter
classifier = pipeline(
    task="text-classification",
    model=local_model_path,
    tokenizer=local_model_path,
    top_k=None  # replaces deprecated return_all_scores=True
)
