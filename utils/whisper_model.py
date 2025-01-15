import whisper
import os

def get_whisper_model(model_size="medium"):
    # Set the cache directory to save/load the model
    model_cache_path = os.path.expanduser("~/.cache/whisper")

    # Load the model
    model = whisper.load_model(model_size, download_root=model_cache_path)

    return model
