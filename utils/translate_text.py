from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import os

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import os

# Mapping of target languages to Opus-MT models
OPUS_MT_MODELS = {
    "fr": "Helsinki-NLP/opus-mt-en-fr",  # English to French
    "es": "Helsinki-NLP/opus-mt-en-es",  # English to Spanish
    "de": "Helsinki-NLP/opus-mt-en-de",  # English to German
    "it": "Helsinki-NLP/opus-mt-en-it",  # English to Italian
    "pt": "Helsinki-NLP/opus-mt-en-pt",  # English to Portuguese
    "ar": "Helsinki-NLP/opus-mt-en-ar",  # English to Arabic
    "hi": "Helsinki-NLP/opus-mt-en-hi",  # English to Hindi
    "zh": "Helsinki-NLP/opus-mt-en-zh",  # English to Chinese
    "ru": "Helsinki-NLP/opus-mt-en-ru",  # English to Russian
}

# Function to dynamically load and cache the Opus-MT model
def get_model(model_name):
    # Set the cache directory to save/load the model
    model_cache_path = os.path.join(os.path.expanduser("~"), ".cache", model_name.replace('/', '_'))

    try:
        # Check if the model is already cached
        if not os.path.exists(model_cache_path):
            # Load the tokenizer and model to cache them
            tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=model_cache_path)
            model = AutoModelForSeq2SeqLM.from_pretrained(model_name, cache_dir=model_cache_path)
            print(f"Model {model_name} downloaded and cached successfully.")
        else:
            # Load the tokenizer and model from the cache
            tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=model_cache_path)
            model = AutoModelForSeq2SeqLM.from_pretrained(model_name, cache_dir=model_cache_path)
            print(f"Model {model_name} loaded from cache.")
        return tokenizer, model
    except Exception as e:
        print(f"Error loading model {model_name}: {e}")
        return None, None



# Function to translate text
def translate_text(text, tgt_lang="fr"):
    try:
        # Get the model name based on the target language
        model_name = OPUS_MT_MODELS.get(tgt_lang)
        if not model_name:
            print(f"Target language '{tgt_lang}' is not supported.")
            return None

        # Load the tokenizer and model
        tokenizer, model = get_model(model_name)
        if tokenizer is None or model is None:
            return None

        # Prepare the input text
        inputs = tokenizer(text, return_tensors="pt")

        # Generate translation
        outputs = model.generate(**inputs)
        translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        return translated_text
    except Exception as e:
        print(f"Error translating text: {e}")
        return None

# Example usage
if __name__ == "__main__":
    # Translate a sample text
    sample_text = "Hello, how are you?"
    translated = translate_text(sample_text, tgt_lang="es")
    print("Translated Text:", translated)
