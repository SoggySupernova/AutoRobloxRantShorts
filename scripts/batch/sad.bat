wsl -e bash -c "./scripts/text/align_subtitles.sh"
ffmpeg -i input.mkv -y -c copy temp/convoutput.mp4
ffmpeg -i temp/convoutput.mp4 -y -filter:v "crop=490:870:683:182" -c:a copy temp/normalspeed.mp4
ffmpeg -i temp/normalspeed.mp4 -y -filter:v "setpts=0.65*PTS" temp/input.mp4
python scripts\text\replacesrt.py
python scripts\audio\speedshift.py temp/audio.wav temp/replaced.srt temp/shifted.wav temp/shifted.srt 2000 0.6 0.8 1.75
python scripts\audio\trimsilence.py temp/shifted.wav temp/shifted.srt temp/trimmed.wav temp/trimmed.srt 300
python scripts\audio\vineboom.py
python scripts\video\add_images.py
ffmpeg -i temp/itdoesntlikewhenioverwritethevideo.mp4 -y temp/input.mp4
ffmpeg -i temp/FINALWAV.wav -i assets/bgm.mp3 -y -filter_complex "[0:a]volume=1.0[a1]; [1:a]volume=0.7[a2]; [a1][a2]amix=inputs=2:duration=longest:dropout_transition=0,volume=2[aout]" -map "[aout]" -ac 2 temp/ACTUALFINALWAV.wav
python scripts\text\rendertext.py temp/bracketed.json
python scripts\video\add_captions.py
python scripts\video\finaltrim.py

exit
