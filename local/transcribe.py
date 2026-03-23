import config
import models

def transcribe_raw(audio_path: str) -> str:
    if audio_path is None: return ""
    result = models.stt_model.transcribe(audio_path, fp16=True)
    return result["text"]

def transcribe_with_timestamps(audio_path: str) -> str:
    if audio_path is None: return ""
    result = models.stt_model.transcribe(audio_path, fp16=True, word_timestamps=True)
    output = ""
    for segment in result["segments"]:
        start = int(segment["start"])
        mins, secs = divmod(start, 60)
        output += f"[{mins:02d}:{secs:02d}] {segment['text'].strip()}\n"
    return output


# Uncomment when pyannote is installed Python 3.10/3.11:
# def transcribe_with_speakers(audio_path: str) -> str:
#     """Transcript with speaker identification via pyannote."""
#     if audio_path is None:
#         return ""
#     diarization = models.diarization_pipeline(audio_path) # <--- Добавлено models.
#     whisper_result = models.stt_model.transcribe(audio_path, fp16=True, word_timestamps=True) # <--- Добавлено models.
#     output_lines = []
#     for segment in whisper_result["segments"]:
#         seg_start = segment["start"]
#         seg_end   = segment["end"]
#         seg_text  = segment["text"].strip()
#         speaker = "Speaker ?"
#         max_overlap = 0.0
#         for turn, _, spk in diarization.itertracks(yield_label=True):
#             overlap = min(turn.end, seg_end) - max(turn.start, seg_start)
#             if overlap > max_overlap:
#                 max_overlap = overlap
#                 num = int(spk.split("_")[-1]) + 1
#                 speaker = f"Speaker {num}"
#         mins = int(seg_start) // 60
#         secs = int(seg_start) % 60
#         timestamp = f"[{mins:02d}:{secs:02d}]"
#         output_lines.append(f"**{speaker}** {timestamp}: {seg_text}")
#     return "\n\n".join(output_lines)

def transcribe_auto(audio_path: str, mode: str) -> str:
    """Router — selects transcription mode by switch."""
    if audio_path is None:
        return ""
    if mode == "👥 Identify speakers":
        # When you're ready to run locally, comment out the line return ниже...
        return "⚠️ Speaker Diarization is temporarily unavailable (requires Python 3.10/3.11)."
        # ...and uncomment this:
        # return transcribe_with_speakers(audio_path)
    elif mode == "🕐 With timecodes":
        return transcribe_with_timestamps(audio_path)
    else:
        return transcribe_raw(audio_path)