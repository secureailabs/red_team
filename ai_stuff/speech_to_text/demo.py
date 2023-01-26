import whisper

model = whisper.load_model("base")
result = model.transcribe("transcript_1.wav")
print(result["text"])
