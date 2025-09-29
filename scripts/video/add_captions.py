from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, ImageClip
from moviepy.video.tools.subtitles import SubtitlesClip
import codecs
import re
import moviepy.config as mpyconf
mpyconf.change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"})

# Helper function to parse SRT file into a list of (start, end, text) tuples
def parse_srt_utf8(srt_path):
    with codecs.open(srt_path, 'r', encoding='utf-8') as f:
        content = f.read()
    pattern = re.compile(r'(\d+)\s+([\d:,]+)\s+-->\s+([\d:,]+)\s+([\s\S]*?)(?=\n\d+\s|\Z)', re.MULTILINE)
    def srt_time_to_seconds(t):
        h, m, s_ms = t.split(':')
        s, ms = s_ms.split(',')
        return int(h)*3600 + int(m)*60 + int(s) + int(ms)/1000
    subtitles = []
    for match in pattern.finditer(content):
        start = srt_time_to_seconds(match.group(2))
        end = srt_time_to_seconds(match.group(3))
        text = match.group(4).replace('\n', ' ').strip()
        subtitles.append(((start, end), text))
    return subtitles

def generate_subtitle(txt, line_number):
    """Loads a pre-rendered image for the subtitle line as an ImageClip."""
    img_path = f"line_number_{line_number}.png"
    img_clip = ImageClip(img_path).set_duration(0.1)  # Duration will be set later
    return img_clip

def add_subtitles_and_audio(video_path, audio_path, srt_path, output_path):
    """Adds image-based subtitles a little lower and smaller, and replaces its audio."""
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)
    subtitles_list = parse_srt_utf8(srt_path)

    subtitle_clips = []
    for i, ((start, end), text) in enumerate(subtitles_list):
        img_clip = generate_subtitle(text, i+1)  # line numbers start at 1
        img_clip = img_clip.resize(0.83)  # Make the caption a little smaller
        img_clip = img_clip.set_start(start).set_end(end).set_position(("center", 120))  # 30px from the top
        subtitle_clips.append(img_clip)

    final_video = CompositeVideoClip([video] + subtitle_clips)
    final_video = final_video.set_audio(audio)
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")

# Example usage
add_subtitles_and_audio("input.mp4", "ACTUALFINALWAV.wav", "trimmed.srt", "output_video.mp4")
