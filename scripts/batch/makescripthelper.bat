python scripts/generating/generate_script.py %1
python scripts/text/removebold.py
python scripts/text/extract_code_block.py
python scripts/generating/create_brackets.py
python scripts/generating/generate_plain_subtitles.py
python scripts/text/clean_text.py subtitles.txt finalsub.txt
taskkill /IM ollama.exe /F
exit