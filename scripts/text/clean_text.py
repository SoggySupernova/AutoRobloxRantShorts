import sys

def clean_text(text: str) -> str:
    # Map curly quotes to straight quotes
    replacements = {
        '“': '"',
        '”': '"',
        '‘': "'",
        '’': "'"
    }
    for curly, straight in replacements.items():
        text = text.replace(curly, straight)
    
    # Remove non-ASCII characters
    text = text.encode('ascii', 'ignore').decode('ascii')
    return text

def process_file(input_file: str, output_file: str) -> None:
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    cleaned = clean_text(content)
    
    with open(output_file, 'w', encoding='ascii') as f:
        f.write(cleaned)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python clean_text.py input.txt output.txt")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    process_file(input_path, output_path)
