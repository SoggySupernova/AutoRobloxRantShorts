import requests
import json
import sys
systemp = """
Create a funny, relatable Youtube Short script with the same formatting and similar style as the attached script. Make it a similar length as the original file. Put intense or funny moments in bold. Put the script in a txt code block.

Here is the attached script:

"""
with open("assets/nah script.txt", "r", encoding="utf-8") as f:
    question = f.read()
print("Generating script...")
data = {
    "model": "mistral",
    "messages": [{"role":"system","content":systemp+question},{"role": "user", "content": "The new script's topic and hook should be: '"+sys.argv[1]+"'"}],
    "stream": True,
    "options": {"num_gpu": 20, "num_ctx": 65536, "num_batch": 512, "num_thread": 8},
    "keep_alive": 100000000000
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
with open("temp/llamaresult.json", "w", encoding="utf-8") as f:
    f.write(result)
