start cmd /K scripts\batch\ollamaautoclose.bat
python scripts/text/create_brackets.py
taskkill /IM ollama.exe /F
exit