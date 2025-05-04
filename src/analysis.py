import os
from transformers import pipeline
from typing import List, Dict, Union
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EmotionAnalyzer:
    def __init__(self):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.model_path = os.path.join(os.path.dirname(current_dir), "models", "emotion-model")
            
            if not os.path.exists(self.model_path):
                raise FileNotFoundError(
                    f"Model not found at {self.model_path}. "
                    "Please run download_model.py first to download the model."
                )
            
            logger.info(f"Loading model from {self.model_path}")
            self.classifier = pipeline(
                task="text-classification",
                model=self.model_path,
                tokenizer=self.model_path,
                top_k=None
            )
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to initialize EmotionAnalyzer: {str(e)}")
            raise
    
    def analyze_text(self, text: str) -> List[List[Dict[str, Union[str, float]]]]:
        """Analyze text and return emotion scores in [[{label, score}, ...]] format."""
        try:
            if not text or not isinstance(text, str) or not text.strip():
                logger.warning("Empty or invalid text provided")
                return [[]]
            
            logger.debug(f"Analyzing text: {text[:50]}...")
            results = self.classifier(text)
            formatted_results = [[
                {
                    'label': result['label'],
                    'score': round(float(result['score']), 4)
                }
                for result in results[0]
            ]]
            logger.debug(f"Classifier output: {formatted_results}")
            return formatted_results
        except Exception as e:
            logger.error(f"Error analyzing text: {str(e)}")
            return [[]]

# Create the classifier instance
classifier = EmotionAnalyzer().analyze_text