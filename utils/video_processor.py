import os
import yt_dlp
from pydub import AudioSegment

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def download_youtube_audio(url: str) -> str:

    # Equivalent to:
    # downloads/<video_title>.<extension>
    output_path = os.path.join(
        DOWNLOAD_DIR,
        "%(title)s.%(ext)s"
    )

    # Settings (similar to command-line options)
    ydl_opts = {

        # Command:
        # yt-dlp -f bestaudio/best <url>
        "format": "bestaudio/best",

        # Command:
        # -o "downloads/%(title)s.%(ext)s"
        "outtmpl": output_path,

        # After downloading, run FFmpeg
        "postprocessors": [
            {
                # Command:
                # ffmpeg -i input.webm output.wav
                "key": "FFmpegExtractAudio",

                # Convert to WAV
                "preferredcodec": "wav",

                # Audio bitrate
                "preferredquality": "192",
            }
        ],

        # Hide download logs
        "quiet": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

        # Same as:
        # yt-dlp <url>
        info = ydl.extract_info(
            url,
            download=True
        )

        # Get downloaded file name
        filename = ydl.prepare_filename(info)

        # If FFmpeg converted it to wav,
        # change extension in returned filename
        filename = filename.replace(".webm", ".wav").replace(".mp3", ".wav")

    return filename

print(download_youtube_audio("https://youtu.be/wGAH8PSk-rg?si=rj-m11dRk9aHSMNK"))