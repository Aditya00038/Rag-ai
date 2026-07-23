import whisper
import json
import os
import re

# Load Whisper's large-v2 model (most accurate, but slowest/heaviest)
# model = whisper.load_model("large-v2")
model = whisper.load_model("medium")

# Create "jsons" folder if it doesn't already exist
# exist_ok=True means: no error if it's already there, and it won't wipe existing files
os.makedirs("jsons", exist_ok=True)

# Get list of all filenames inside the "audios" folder
audios = os.listdir("audios")

# Regex pattern to match filenames like "react_005.mp3"
# Group 1 = everything before the last underscore (title, e.g. "react")
# Group 2 = the number after the underscore (e.g. "005")
pattern = re.compile(r"^(.+)_(\d+)\.mp3$", re.IGNORECASE)

# Loop through every file in the audios folder
for audio in audios:

    # Skip anything that isn't an mp3 file (e.g. folders, .txt, etc.)
    if not audio.lower().endswith(".mp3"):
        continue

    # Try to match the "title_number.mp3" pattern (e.g. react_005.mp3)
    match = pattern.match(audio)

    if match:
        # Matched the pattern -> it's a sample chunk file
        title = match.group(1)   # e.g. "react"
        number = match.group(2)  # e.g. "005"
    else:
        # Didn't match -> it's a main/full-length file
        # (e.g. "React Full Course.mp3", "JavaScript Crash Course_...mp3")
        title = os.path.splitext(audio)[0]  # filename without extension
        number = "main"                     # label it as "main" since no number exists

    # Print which file is currently being processed (for tracking progress)
    print(number, title)

    # Run Whisper transcription + translation on this audio file
    result = model.transcribe(
        audio=f"audios/{audio}",   # path to the audio file
        language="hi",              # source language spoken in audio (Hindi)
        task="translate",           # translate speech into English text
        word_timestamps=False       # don't need word-level timestamps, just segment-level
    )

    # Build a list of chunks, one per transcribed segment
    chunks = []
    for segment in result["segments"]:
        chunks.append({
            "number": number,           # chunk number (or "main")
            "title": title,              # video/audio title
            "start": segment["start"],   # start time of this segment (seconds)
            "end": segment["end"],       # end time of this segment (seconds)
            "text": segment["text"]      # transcribed/translated text for this segment
        })

    # Wrap chunks + full text together into one dictionary
    chunks_with_metadata = {"chunks": chunks, "text": result["text"]}

    # Save this file's transcription as a JSON file inside "jsons" folder
    # Filename matches the original audio name, e.g. "react_005.mp3.json"
    with open(f"jsons/{audio}.json", "w") as f:
        json.dump(chunks_with_metadata, f)