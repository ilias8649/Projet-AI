import yt_dlp
import os

def download_video_from_url(url, output_path="temp_video.mp4"):
    try:
        # Temporary file without extension
        temp_path = os.path.splitext(output_path)[0]

        ydl_opts = {
            'outtmpl': f"{temp_path}.%(ext)s",  # Keep dynamic extension
            'format': 'bestvideo+bestaudio/best',  # Download the best quality
            'merge_output_format': 'mp4',  # Force output to be in .mp4 format
            'quiet': False,  # Optional: show the download progress
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # Ensure the final output file is named correctly
        final_output = f"{temp_path}.mp4"
        if not os.path.exists(final_output):
            print("Warning: Downloaded file was not merged correctly. Checking for alternative extensions.")
            # Look for alternative extensions (e.g., .webm, .mkv)
            for ext in ['.webm', '.mkv']:
                alternative_path = f"{temp_path}{ext}"
                if os.path.exists(alternative_path):
                    os.rename(alternative_path, final_output)
                    print(f"Renamed {alternative_path} to {final_output}")
                    break

        print(f"Video downloaded successfully: {final_output}")
        return final_output
    except Exception as e:
        print(f"Error downloading video: {e}")
        return None

