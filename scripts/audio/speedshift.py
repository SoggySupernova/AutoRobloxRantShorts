import sys
import random
from pydub import AudioSegment
import pysrt
import math

def time_to_ms(t):
    return (t.hours * 3600 + t.minutes * 60 + t.seconds) * 1000 + t.milliseconds

def ms_to_time(ms):
    hours = ms // 3600000
    ms %= 3600000
    minutes = ms // 60000
    ms %= 60000
    seconds = ms // 1000
    milliseconds = ms % 1000
    return pysrt.SubRipTime(hours, minutes, seconds, milliseconds)

def linear_speed_change_segment(audio, start_ms, end_ms, start_speed, end_speed):
    segment = AudioSegment.empty()
    chunk_ms = 50
    length = end_ms - start_ms
    num_chunks = math.ceil(length / chunk_ms)

    for i in range(num_chunks):
        chunk_start = start_ms + i * chunk_ms
        chunk_end = min(start_ms + (i + 1) * chunk_ms, end_ms)
        chunk = audio[chunk_start:chunk_end]

        frac = (chunk_start - start_ms) / length if length > 0 else 0
        speed = start_speed + frac * (end_speed - start_speed)

        new_frame_rate = int(chunk.frame_rate * speed)
        chunk = chunk._spawn(chunk.raw_data, overrides={'frame_rate': new_frame_rate})
        chunk = chunk.set_frame_rate(audio.frame_rate)

        segment += chunk
    return segment

def change_speed_fixed(audio, speed):
    new_frame_rate = int(audio.frame_rate * speed)
    changed = audio._spawn(audio.raw_data, overrides={'frame_rate': new_frame_rate})
    return changed.set_frame_rate(audio.frame_rate)

def merge_intervals(intervals):
    if not intervals:
        return []
    for interval in intervals:
        if 'emoji_starts' not in interval:
            interval['emoji_starts'] = [interval['emoji_start']]
    intervals.sort(key=lambda x: x['slow_start'])
    merged = [intervals[0]]
    for current in intervals[1:]:
        last = merged[-1]
        if current['slow_start'] <= last['emoji_end']:
            merged[-1] = {
                'slow_start': min(last['slow_start'], current['slow_start']),
                'emoji_starts': sorted(list(set(last['emoji_starts'] + current['emoji_starts']))),
                'emoji_end': max(last['emoji_end'], current['emoji_end']),
                'end_speed': last['end_speed']  # keep same for merged
            }
        else:
            merged.append(current)
    return merged

def process_audio_and_srt(audio_path, srt_path, output_audio_path, output_srt_path,
                          slowdown_ms, min_end_speed, max_end_speed, start_speed):
    audio = AudioSegment.from_file(audio_path)
    duration_ms = len(audio)
    subs = pysrt.open(srt_path)

    slowdown_regions = []
    for sub in subs:
        if sub.text.strip().endswith("😭🙏"):
            end_ms = time_to_ms(sub.end)
            emoji_start_ms = end_ms - 100  # 0.1s before end
            slow_start_ms = max(0, emoji_start_ms - slowdown_ms)
            slowdown_regions.append({
                'slow_start': slow_start_ms,
                'emoji_start': emoji_start_ms,
                'emoji_end': end_ms,
                'end_speed': round(random.uniform(min_end_speed, max_end_speed), 3)
            })

    if not slowdown_regions:
        print("No lines ending with '😭🙏' found.")
        return

    merged_intervals = merge_intervals(slowdown_regions)

    boundaries = set([0, duration_ms])
    for interval in merged_intervals:
        boundaries.add(interval['slow_start'])
        boundaries.add(interval['emoji_end'])
        for es in interval['emoji_starts']:
            boundaries.add(es)
    boundaries = sorted(boundaries)

    def get_speed(orig_ms):
        for interval in merged_intervals:
            s = interval['slow_start']
            e = interval['emoji_end']
            if s <= orig_ms < e:
                earliest_emoji_start = interval['emoji_starts'][0]
                end_speed = interval['end_speed']
                if s <= orig_ms < earliest_emoji_start:
                    frac = (orig_ms - s) / (earliest_emoji_start - s) if (earliest_emoji_start - s) != 0 else 0
                    return start_speed + frac * (end_speed - start_speed)
                else:
                    return end_speed
        return start_speed

    output_audio = AudioSegment.empty()
    timing_map = []
    out_cursor = 0

    for i in range(len(boundaries) - 1):
        seg_start = boundaries[i]
        seg_end = boundaries[i + 1]
        segment_orig = audio[seg_start:seg_end]

        speed_start = get_speed(seg_start)
        speed_end = get_speed(seg_end)

        if abs(speed_start - speed_end) > 0.01:
            segment_changed = linear_speed_change_segment(segment_orig, 0, len(segment_orig), speed_start, speed_end)
        else:
            segment_changed = change_speed_fixed(segment_orig, speed_start)

        output_audio += segment_changed
        timing_map.append((seg_start, seg_end, out_cursor, out_cursor + len(segment_changed)))
        out_cursor += len(segment_changed)

    def map_time(orig_ms):
        for o_start, o_end, out_start, out_end in timing_map:
            if o_start <= orig_ms <= o_end:
                ratio = (orig_ms - o_start) / (o_end - o_start) if (o_end - o_start) != 0 else 0
                mapped = out_start + ratio * (out_end - out_start)
                return int(mapped)
        return orig_ms

    new_subs = pysrt.SubRipFile()
    for sub in subs:
        new_start = map_time(time_to_ms(sub.start))
        new_end = map_time(time_to_ms(sub.end))
        new_sub = pysrt.SubRipItem(
            index=sub.index,
            start=ms_to_time(new_start),
            end=ms_to_time(new_end),
            text=sub.text
        )
        new_subs.append(new_sub)

    output_audio.export(output_audio_path, format="wav")
    new_subs.save(output_srt_path, encoding='utf-8')

if __name__ == "__main__":
    if len(sys.argv) != 9:
        print("Usage: python script.py input_audio input_srt output_audio output_srt slowdown_ms min_end_speed max_end_speed start_speed")
        sys.exit(1)

    audio_path = sys.argv[1]
    srt_path = sys.argv[2]
    output_audio_path = sys.argv[3]
    output_srt_path = sys.argv[4]
    slowdown_ms = int(sys.argv[5])
    min_end_speed = float(sys.argv[6])
    max_end_speed = float(sys.argv[7])
    start_speed = float(sys.argv[8])

    process_audio_and_srt(audio_path, srt_path, output_audio_path, output_srt_path,
                          slowdown_ms, min_end_speed, max_end_speed, start_speed)
