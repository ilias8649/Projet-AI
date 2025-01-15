import ffmpeg

def extract_audio(video_file_path, audio_output_path="audio.mp3"):
    try:
        ffmpeg.input(video_file_path).output(audio_output_path).run()
        print(f"Audio extracted successfully: {audio_output_path}")
        return audio_output_path
    except ffmpeg.Error as e:
        print(f"Error extracting audio: {e}")
        return None
