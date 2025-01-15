import os
from utils.audio_extractor import extract_audio
from utils.subtitle_generator import create_srt
from utils.video_subtitle_merger import add_subtitles_to_video
from utils.whisper_model import get_whisper_model
from utils.video_downloader import download_video_from_url
from utils.translate_text import translate_text
from utils.embeding import generate_and_store_embedding

def process_video(video_input,target_language):
    model = get_whisper_model()
    # File paths
    video_file_path = video_input if os.path.isfile(video_input) else "temp_video.mp4"
    audio_file_path = "audio.mp3"
    subtitle_file_path = "subtitles.srt"
    output_video_path = "output/video_with_subtitles.mp4"
    translated_text_file = "translated_text.txt"

    # Create output directory if it doesn't exist
    output_directory = "output"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # If input is a URL, download the video
    if video_input.startswith("http://") or video_input.startswith("https://"):
        video_file_path = download_video_from_url(video_input, output_path=video_file_path)
        if not video_file_path:
            print("Failed to download the video. Exiting.")
            return

    # Extract audio from video
    audio_file_path = extract_audio(video_file_path, audio_output_path=audio_file_path)

    if audio_file_path:
        # Transcribe audio to generate subtitles
        result = model.transcribe(audio_file_path, task="translate")

        # Generate and store embedding for the original text
        generate_and_store_embedding(result["text"])

        # Translate the segments to the target language
        translated_segments = []
        all_translated_text = []
        
        for segment in result["segments"]:
            if target_language != "en":
                # Perform translation
                translated_text = translate_text(segment["text"], tgt_lang=target_language)
            else:
                # Use the original text if target language is English
                translated_text = segment["text"]

            # Append translated or original text to the segments
            translated_segments.append({
                "start": segment["start"],
                "end": segment["end"],
                "text": translated_text
            })



        # Create SRT file with translated segments
        if translated_segments:
            create_srt(translated_segments, output_srt_path=subtitle_file_path)
        else:
            print("No translated segments available for SRT creation. Exiting.")
            return

        # Add subtitles to the video
        add_subtitles_to_video(video_file_path, subtitle_file_path, output_video_path)

        # Clean up temporary files
        cleanup_files = [audio_file_path, subtitle_file_path]
        if video_input.startswith("http://") or video_input.startswith("https://"):
            cleanup_files.append(video_file_path)

        for file_path in cleanup_files:
            if os.path.exists(file_path):
                os.remove(file_path)
