start cmd /K scripts\batch\ollamaautoclose.bat
python scripts/text/generate_plain_subtitles.py
python scripts/text/clean_text.py subtitles.txt finalsub.txt
taskkill /IM ollama.exe /F
exit