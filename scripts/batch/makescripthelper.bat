python scripts/text/generate_script.py %1
python scripts/text/removebold.py
python scripts/text/extract_code_block.py
python scripts/text/create_brackets.py
python scripts/text/generate_plain_subtitles.py
python scripts/text/clean_text.py temp/subtitles.txt temp/finalsub.txt
taskkill /IM ollama.exe /F

exit
