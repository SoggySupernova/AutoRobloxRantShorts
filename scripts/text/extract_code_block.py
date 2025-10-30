import re

def extract_code_blocks(markdown_text):
    """
    Extracts text inside Markdown code blocks (```...```) and returns them as a list of strings,
    excluding the code fence lines and any language identifiers.
    """
    # Regex captures content between triple backticks, ignoring the language tag
    pattern = r"```(?:[a-zA-Z0-9_+-]*)\n(.*?)```"
    matches = re.findall(pattern, markdown_text, re.DOTALL)
    return [match.strip() for match in matches]

if __name__ == "__main__":
    # Example usage
    with open("temp/output.md", "r", encoding="utf-8") as file:
        markdown_content = file.read()
    
    code_blocks = extract_code_blocks(markdown_content)
    print(code_blocks)
    # Save or print extracted code
    with open("temp/enter.txt", "w", encoding="utf-8") as file:
        # Also remove empty lines, replace emojis, add subscribe to the end
        filtered = '\n'.join([line for line in code_blocks[-1].split('\n') if line.strip()])
        file.write(filtered)
        print('Writing: ' + filtered)

