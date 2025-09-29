from pydub import AudioSegment
import pysrt

def insert_sound_effect(
    base_audio_path,
    srt_path,
    effect_audio_path,
    phrase,
    volume_db,
    output_path
):
    # Load base audio
    base_audio = AudioSegment.from_wav(base_audio_path)

    # Load sound effect and adjust volume
    effect_audio = AudioSegment.from_wav(effect_audio_path) + volume_db

    # Load subtitles
    subs = pysrt.open(srt_path)

    # Process each subtitle
    for sub in subs:
        # Check if subtitle text ends with the target phrase
        if phrase.lower() in sub.text.strip().lower():
            # Calculate insertion time in milliseconds
            end_time_ms = (
                sub.end.hours * 3600000
                + sub.end.minutes * 60000
                + sub.end.seconds * 1000
                + int(sub.end.milliseconds)
                - 380  # extra 10 ms
            )

            # Overlay the effect on the base audio
            base_audio = base_audio.overlay(effect_audio, position=end_time_ms)

    # Export result
    base_audio.export(output_path, format="wav")


if __name__ == "__main__":
    insert_sound_effect(
        base_audio_path="trimmed.wav",
        srt_path="trimmed.srt",
        effect_audio_path="assets/vineboom.wav",
        phrase="😭🙏",  # change to your phrase
        volume_db=-5,                # negative to lower volume, positive to increase
        output_path="FINALWAV.wav"
    )

