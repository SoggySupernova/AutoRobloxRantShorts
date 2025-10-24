import re
import subprocess
from fractions import Fraction

# --- Configuration ---
srt_path = "trimmed.srt"
mp4_path = "output_video.mp4"
output_path = "FINALVIDEO.mp4"

# --- Step 1: Detect framerate from MP4 ---
def get_framerate(video_path):
    result = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=r_frame_rate",
            "-of", "default=noprint_wrappers=1:nokey=1",
            video_path
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True
    )
    return Fraction(result.stdout.strip())

frame_rate = get_framerate(mp4_path)
print(f"Detected framerate: {frame_rate} fps")

# --- Step 2: Extract last end time from SRT ---
with open(srt_path, "r", encoding="utf-8") as f:
    content = f.read().strip()

timestamps = re.findall(
    r"(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})",
    content
)

if not timestamps:
    raise ValueError("No valid timestamps found in the SRT file.")

last_end_time_str = timestamps[-1][1]

def srt_time_to_seconds(t):
    h, m, s_ms = t.split(":")
    s, ms = s_ms.split(",")
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000

last_end_seconds = srt_time_to_seconds(last_end_time_str)

# --- Step 3: Calculate exact trim points ---
one_frame = 1 / float(frame_rate)
trim_end = last_end_seconds - one_frame
trim_start = 5 / float(frame_rate)

# --- Step 4: Trim with re-encoding ---
cmd = [
    "ffmpeg",
    "-ss", f"{trim_start:.6f}",
    "-i", mp4_path,
    "-y",
    "-to", f"{trim_end - trim_start:.6f}",  # duration, not absolute end
    "-c:v", "libx264", "-crf", "18", "-preset", "veryfast",
    "-c:a", "aac", "-b:a", "192k",
    output_path
]

subprocess.run(cmd, check=True)
print(f"Frame-accurate trimmed video saved to: {output_path}")
