from utils.process_video import process_video

from utils.LLM import process_prompt
"""
def main():
    # Input: URL or local file path
    video_input = input("Enter the video file path or URL: ")

    # Process the video
    target_language = input("Enter the target language (e.g., 'fr', 'es', 'ar'): ").lower()
    process_video(video_input, target_language)
"""
if __name__ == "__main__":
    prompt = "what do you know about mercury metal"
    response = process_prompt(prompt)
    print("\nFinal Response:")
    print(response)
