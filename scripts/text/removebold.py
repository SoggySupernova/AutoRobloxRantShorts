import re

def uppercase_and_remove_bold(markdown_text: str) -> str:
    # Matches Markdown bold syntax: **text** or __text__
    pattern = r'(\*\*|__)(.*?)\1'

    def replace_bold(match):
        return match.group(2).upper()

    return re.sub(pattern, replace_bold, markdown_text, flags=re.DOTALL)

if __name__ == "__main__":
    input_file = "temp/llamaresult.json"
    output_file = "temp/output.md"
    # Read Markdown content
    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Process content
    processed_content = uppercase_and_remove_bold(content)

    # Save result
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(processed_content)

    print(f"Processed file saved as {output_file}")

