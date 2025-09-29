import requests
import json
systemp = """
You are to convert the user’s text to sentence case with the following rules:

1. **Preserve line breaks exactly as in the input.**
   - Do not remove, merge, shift, or add line breaks.
   - The output must contain the same number of lines in the same positions as the input.

2. Apply sentence case only:
   - Capitalize the first word of each sentence.
   - Capitalize proper nouns, acronyms, “I,” and days of the week correctly.

3. Do not alter wording, punctuation, or spacing other than capitalization adjustments required by sentence case.

Here is an example with this as the original text:

HOW does SLANG
go from being THE
COOLEST thing ever
to COMPLETELY EMBARRASSING
in like TWO WEEKS?
One day, EVERYBODY's saying it

...and so on.

And here's the example of how you should respond:

How does slang
go from being the
coolest thing ever
to completely embarrassing
in like two weeks?
One day, everybody's saying it

...and so on.

Notice how no words are changed, all line breaks are kept and unchanged, and the text is in proper sentence case.
# **Also notice how each sentence (e.g., “in like two weeks? / One day…”) remain split across lines without being collapsed into a single line.**

Respond only with the corrected text.

The user will now provide the text.
"""
with open("enter.txt", "r", encoding="utf-8") as f:
    question = f.read().lower()
print("Generating script...")
data = {
    "model": "mistral",
    "messages": [{"role":"system","content":systemp},{"role": "user", "content": "Here's my existing script:\n" + question+"\nSubscribe."}],
    "stream": True,
    "options": {"num_gpu": -1,"num_ctx": 2048},
    "keep_alive": -1
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
with open("subtitles.txt", "w", encoding="utf-8") as f:
    f.write(result.replace('\n','\n\n').replace('🙏','').replace('😭','').replace('😐','').replace('🥀',''))