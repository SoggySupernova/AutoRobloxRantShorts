import os
import re
import sys
from pathlib import Path

import pysrt
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip
import moviepy.video.fx.all as vfx

# ---- CONFIG ----
VIDEO_PATH = "input.mp4"                # your video
SRT_PATH = "trimmed.srt"                # original SRT (will not be modified)
ORIG_TEXT_PATH = "origbracketed.json"   # text file with replacement subtitle lines (one per subtitle)
OUTPUT_SRT = "replaced_subs.srt"        # new SRT produced (original SRT kept)
OUTPUT_VIDEO = "input.mp4"              # overwrite file so I don't have to change all my scripts again
IMAGE_FOLDER = "assets"                 # where <word>.png files live (relative or absolute)
IMAGE_HEIGHT = 320                      # px height for overlaid image (auto-resize)
OVERLAY_DURATION = 1.15                 # seconds: how long the image stays (fade will happen during this)
FADE_DURATION = 1                       # seconds: length of fade-out (<= OVERLAY_DURATION)
TIME_OFFSET_SEC = 0.38                  # mimic original script's small back-offset (380ms)
# ----------------

BRACKET_RE = re.compile(r"\{([^}]+)\}")

def load_replacement_lines(path):
    with open(path, "r", encoding="utf-8") as f:
        # Keep newline semantics consistent; strip trailing newlines
        lines = [l.rstrip("\n\r") for l in f.readlines()]
    return lines

def is_numeric_bracket(s):
    # Return True if the bracketed content is a pure integer (e.g. "2" or "123")
    return re.fullmatch(r"\d+", s) is not None

def main():
    # sanity checks
    for p in (VIDEO_PATH, SRT_PATH, ORIG_TEXT_PATH):
        if not os.path.exists(p):
            print(f"ERROR: required file not found: {p}", file=sys.stderr)
            return

    # load SRT
    subs = pysrt.open(SRT_PATH, encoding='utf-8')
    # load replacement lines
    repl_lines = load_replacement_lines(ORIG_TEXT_PATH)

    if len(repl_lines) < len(subs):
        print(
            f"WARNING: {ORIG_TEXT_PATH} has fewer lines ({len(repl_lines)}) than subtitles ({len(subs)}).\n"
            "Only the first N subtitles will be replaced accordingly.",
            file=sys.stderr
        )

    # create a copy of subtitles with replaced text (do not modify original SRT file)
    new_subs = pysrt.SubRipFile()
    for i, sub in enumerate(subs):
        new_text = repl_lines[i] if i < len(repl_lines) else sub.text
        # preserve the original timing
        new_item = pysrt.SubRipItem(index=sub.index, start=sub.start, end=sub.end, text=new_text)
        new_subs.append(new_item)

    # save new SRT
    new_subs.save(OUTPUT_SRT, encoding='utf-8')

    # load video
    video = VideoFileClip(VIDEO_PATH)
    overlays = []

    # for each subtitle, detect bracketed words in the replacement text
    for i, sub in enumerate(new_subs):
        text = sub.text
        matches = BRACKET_RE.findall(text)
        if not matches:
            continue

        # compute insertion time: just before subtitle end, matching the original audio logic
        end_seconds = sub.end.hours * 3600 + sub.end.minutes * 60 + sub.end.seconds + (sub.end.milliseconds / 1000.0)
        start_time = max(0, end_seconds - TIME_OFFSET_SEC)  # seconds

        for br in matches:
            br_stripped = br.strip()
            if is_numeric_bracket(br_stripped):
                # ignore bracketed numbers like {2}
                continue

            # image filename for this bracketed word
            # sanitize file name minimally: remove spaces and keep common safe chars
            filename_safe = "".join(c for c in br_stripped if c.isalnum() or c in ("-", "_"))
            img_path = Path(IMAGE_FOLDER) / f"{filename_safe}.png"

            if not img_path.exists():
                # If image is missing, skip but log to stderr
                print(f"WARNING: image for {{{br}}} not found: {img_path}", file=sys.stderr)
                continue

            # create ImageClip with specified duration and fade-out
            img_clip = ImageClip(str(img_path)).set_duration(OVERLAY_DURATION)
            # resize if needed
            try:
                img_clip = img_clip.resize(height=IMAGE_HEIGHT)
            except Exception:
                pass

            # set start time and position (center)
            img_clip = img_clip.set_start(start_time).set_pos(("center", "center"))

            # apply fadeout over FADE_DURATION seconds (moviepy fadeout expects seconds)
            if FADE_DURATION > 0 and FADE_DURATION <= OVERLAY_DURATION:
                img_clip = img_clip.crossfadeout(FADE_DURATION)

            overlays.append(img_clip)

    if overlays:
        # ensure composite uses the same frame size as the source
        composite = CompositeVideoClip([video, *overlays], size=video.size)
        # compute the desired duration: at least the video duration;
        # also handle the (unlikely) case where an overlay extends past the video
        overlay_ends = [oc.start + oc.duration for oc in overlays]
        max_overlay_end = max(overlay_ends) if overlay_ends else 0
        composite_duration = max(video.duration, max_overlay_end)

        # explicitly set duration
        final = composite.set_duration(composite_duration)
    else:
        final = video

    export_fps = getattr(video, "fps", None) or 24

    # export (preserve audio from original video)
    final.write_videofile(
        OUTPUT_VIDEO,
        codec="libx264",
        audio_codec="aac",
        threads=4,
        preset="medium",
        fps=export_fps,
        audio=True
    )


    # cleanup
    final.close()
    video.close()

    print(f"Done. New SRT: {OUTPUT_SRT}   Video: {OUTPUT_VIDEO}")

if __name__ == "__main__":
    main()
