from transformers import AutoModelForSequenceClassification, AutoTokenizer

model_name = "j-hartmann/emotion-english-distilroberta-base"
save_path = "../models/emotion-model"  # Relative to your script location

# Download and save the model and tokenizer locally
model = AutoModelForSequenceClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

model.save_pretrained(save_path)
tokenizer.save_pretrained(save_path)

print("Model saved locally at:", save_path)
