from pydub import AudioSegment, silence
import pysrt
import sys

def shorten_silences(audio, max_silence_len=1000, silence_thresh=-40):
    """
    Shortens silences longer than max_silence_len to exactly max_silence_len.
    Returns:
      shortened_audio: AudioSegment with silences shortened
      time_map: list of tuples (original_start_ms, original_end_ms, new_start_ms)
    """
    silent_ranges = silence.detect_silence(audio, min_silence_len=100, silence_thresh=silence_thresh)
    # Filter only silences longer than max_silence_len
    long_silences = [(start, end) for start, end in silent_ranges if (end - start) > max_silence_len]

    if not long_silences:
        return audio, [(0, len(audio), 0)]

    shortened_chunks = []
    time_map = []
    prev_end = 0
    new_time = 0

    for start, end in long_silences:
        # Append audio chunk before the silence
        if prev_end < start:
            chunk = audio[prev_end:start]
            shortened_chunks.append(chunk)
            time_map.append((prev_end, start, new_time))
            new_time += len(chunk)

        # Append shortened silence
        silence_duration = end - start
        # Take only max_silence_len from the original silence
        shortened_silence = audio[start:start + max_silence_len]
        shortened_chunks.append(shortened_silence)
        time_map.append((start, end, new_time))
        new_time += max_silence_len

        prev_end = end

    # Append remaining audio after last silence
    if prev_end < len(audio):
        chunk = audio[prev_end:]
        shortened_chunks.append(chunk)
        time_map.append((prev_end, len(audio), new_time))

    shortened_audio = sum(shortened_chunks)
    return shortened_audio, time_map

def adjust_subtitle_times(subs, time_map):
    """
    Adjust subtitle times based on time_map.
    time_map: list of tuples (orig_start, orig_end, new_start) in ms
    """
    def map_time(orig_ms):
        for orig_start, orig_end, new_start in time_map:
            if orig_start <= orig_ms < orig_end:
                return new_start + (orig_ms - orig_start)
        # If beyond last chunk, clamp to end
        last_chunk = time_map[-1]
        if orig_ms >= last_chunk[1]:
            return last_chunk[2] + (last_chunk[1] - last_chunk[0])
        return 0

    for sub in subs:
        start_ms = sub.start.ordinal
        end_ms = sub.end.ordinal
        sub.start = pysrt.SubRipTime(milliseconds=map_time(start_ms))
        sub.end = pysrt.SubRipTime(milliseconds=map_time(end_ms))

def main(wav_path, srt_path, output_wav_path, output_srt_path, max_silence_len=1000, silence_thresh=-40):
    audio = AudioSegment.from_wav(wav_path)
    subs = pysrt.open(srt_path)

    shortened_audio, time_map = shorten_silences(audio, max_silence_len, silence_thresh)
    adjust_subtitle_times(subs, time_map)

    shortened_audio.export(output_wav_path, format="wav")
    subs.save(output_srt_path, encoding='utf-8')

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python shorten_silence_sync.py input.wav input.srt output.wav output.srt max_silence_len_ms")
        sys.exit(1)

    wav_path = sys.argv[1]
    srt_path = sys.argv[2]
    output_wav_path = sys.argv[3]
    output_srt_path = sys.argv[4]
    max_silence_len = int(sys.argv[5])
    silence_thresh = -40  # Can be parameterized if needed

    main(wav_path, srt_path, output_wav_path, output_srt_path, max_silence_len, silence_thresh)
