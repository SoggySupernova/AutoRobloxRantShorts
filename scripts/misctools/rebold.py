import re

def bold_and_lower_capitalized_words(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()

    # Replace uppercase words with lowercase bolded versions
    bolded_text = re.sub(r'\b([A-Z]{2,})\b', lambda m: f"**{m.group(1).lower()}**", text)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(bolded_text)

# Example usage
bold_and_lower_capitalized_words('input.txt', 'output.md')
