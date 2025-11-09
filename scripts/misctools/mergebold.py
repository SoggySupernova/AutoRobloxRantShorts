import re

# Read input file
with open("output.md", "r", encoding="utf-8") as f:
    text = f.read()

# Merge consecutive bold words: **word1** **word2** -> **word1 word2**
pattern = re.compile(r"\*\*([^\*]+?)\*\*\s+\*\*([^\*]+?)\*\*")
while True:
    new_text = pattern.sub(r"**\1 \2**", text)
    if new_text == text:
        break
    text = new_text

# Write output file
with open("realoutput.md", "w", encoding="utf-8") as f:
    f.write(text)
