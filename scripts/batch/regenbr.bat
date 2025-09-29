start cmd /K scripts\batch\ollamaautoclose.bat
python scripts/generating/create_brackets.py
taskkill /IM ollama.exe /F
exit