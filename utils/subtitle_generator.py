import whisper
import torch

def create_srt(segments, output_srt_path):
    with open(output_srt_path, "w", encoding="utf-8") as srt_file:
        for idx, segment in enumerate(segments):
            start_time = format_time(segment["start"])
            end_time = format_time(segment["end"])
            text = segment["text"]

            srt_file.write(f"{idx + 1}\n")
            srt_file.write(f"{start_time} --> {end_time}\n")
            srt_file.write(f"{text}\n\n")

def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    milliseconds = int((seconds % 1) * 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"
