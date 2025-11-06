import requests
import json
import sys
import re
systemp = """
Add EXACTLY ONE tag at the END of EVERY line: a word/number in curly brackets, with ONE SPACE before it. Keep all words and line breaks unchanged. Use ONLY ONE tag per line.
Remember to keep ALL the line breaks of the original text. Do not add any new line breaks either.

# Tag rules:

- Last line of a sentence: {positive}, {confusing}, {shocking}, or {depressing} depending on the tone of the sentence.
- Other lines: {1}, {2}, {3}, or {4} depending on the emotional or humourous intensity of that line.

# Example:


HOW does SLANG {1}
go from being THE {1}
COOLEST thing ever {3}
to COMPLETELY EMBARRASSING {4}
in like TWO WEEKS? {confusing}
One day, EVERYBODY's saying it {2}

...and so on. Notice how EVERY line has a tag at the end, the last line of each sentence has a word in a bracket, and other lines have a number in the bracket.

Respond with ONLY the updated text—no explanations, no extra output. The user will now provide the text.
"""
with open("temp/enter.txt", "r", encoding="utf-8") as f:
    question = '\n'.join([line.rstrip() for line in f.read().splitlines()]) # remove extra whitespace from each line
    print(question)
print("Generating script...")
data = {
    "model": "mistral",
    "messages": [{"role":"system","content":systemp},{"role": "user", "content": question}],
    "stream": True,
    "options": {"num_gpu": -1,"num_ctx": 16384},
    "keep_alive": 0
}
url = "http://localhost:11434/api/chat"
response = requests.post(url, json=data, stream=True)
result = ""
for line in response.iter_lines():
    if line:
        try:
            resp = json.loads(line.decode('utf-8'))
            content = resp.get("message", {}).get("content", "")
            if content:
                print(content, end='', flush=True)
                result += content
        except Exception:
            continue
with open("temp/bracketed.json", "w", encoding="utf-8") as f:
    f.write((result + '\nSubscribe. {neutral}').replace('{1}','😐').replace('{2}','🥀').replace('{3}','🙏').replace('{4}','😭'))
with open("temp/origbracketed.json", "w", encoding="utf-8") as f:
    f.write(result + '\nSubscribe. 😭🙏')
