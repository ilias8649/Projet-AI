import ffmpeg

def add_subtitles_to_video(video_file_path, subtitle_file_path, output_video_path="output_video_with_subtitles.mp4"):
    try:
        ffmpeg.input(video_file_path).output(output_video_path, vf=f"subtitles={subtitle_file_path}").run()
        print(f"Subtitles added successfully: {output_video_path}")
    except ffmpeg.Error as e:
        print(f"Error adding subtitles: {e}")
