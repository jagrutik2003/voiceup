import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification

def download_model():
    print("Downloading emotion classification model...")
    
    # Model ID from Hugging Face
    model_id = "j-hartmann/emotion-english-distilroberta-base"
    
    # Set up local path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    local_model_path = os.path.join(os.path.dirname(current_dir), "models", "emotion-model")
    
    # Create directory if it doesn't exist
    os.makedirs(local_model_path, exist_ok=True)
    
    try:
        # Download model and tokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = AutoModelForSequenceClassification.from_pretrained(model_id)
        
        # Save locally
        tokenizer.save_pretrained(local_model_path)
        model.save_pretrained(local_model_path)
        
        print(f"Model downloaded successfully to {local_model_path}")
    except Exception as e:
        print(f"Error downloading model: {e}")
        raise

if __name__ == "__main__":
    download_model()
