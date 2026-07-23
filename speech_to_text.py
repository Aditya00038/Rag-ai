import whisper
import json

model = whisper.load_model("large-v2")
result = model.transcribe(audio="audios/react_045.mp3",
                          language="hi",
                          task="translate")

chunks = []
for segment in result["segments"]:
    chunks.append({"start": segment["start"],
                   "end": segment["end"],
                   "text": segment["text"]})

print(chunks)

with open("output.json", "w") as f:
    json.dump(chunks, f)