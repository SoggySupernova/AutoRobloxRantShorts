ffmpeg -i input.mkv -c copy convoutput.mp4
ffmpeg -i convoutput.mp4 -filter:v "crop=490:870:683:182" -c:a copy normalspeed.mp4
ffmpeg -i normalspeed.mp4 -filter:v "setpts=0.65*PTS" input.mp4
python scripts\text\replacesrt.py
python scripts\audio\speedshift.py audio.wav replaced.srt shifted.wav shifted.srt 2000 0.6 0.8 1.75
python scripts\audio\trimsilence.py shifted.wav shifted.srt trimmed.wav trimmed.srt 300
python scripts\audio\vineboom.py
ffmpeg -i FINALWAV.wav -i assets/bgm.mp3 -filter_complex "[0:a]volume=1.0[a1]; [1:a]volume=0.7[a2]; [a1][a2]amix=inputs=2:duration=longest:dropout_transition=0,volume=2[aout]" -map "[aout]" -ac 2 ACTUALFINALWAV.wav
python scripts\video\rendertext.py bracketed.json
python scripts\video\add_captions.py
python scripts\video\finaltrim.py