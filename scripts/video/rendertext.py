import base64
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json
import re

# IMPORTANT: Ensure 'font.txt' and 'spritesheet.txt' are in the same directory
try:
    with open("assets/font.txt", "r") as file:
        CUSTOM_FONT_BASE64 = file.read().strip()
    with open("assets/spritesheet.txt", "r") as file2:
        EMOJI_SPRITE_BASE64 = file2.read().strip()
except FileNotFoundError:
    print("Error: Required files 'font.txt' or 'spritesheet.txt' not found.")
    exit()

def create_html(canvas_width=700, canvas_height=300):
    """
    Generates the HTML content for the page, including a hidden image tag for the
    emoji sprite sheet.
    """
    font_css = f"""
    @font-face {{
        font-family: 'CustomFont';
        src: url(data:font/ttf;base64,{CUSTOM_FONT_BASE64}) format('truetype');
        font-weight: 500;
        font-style: normal;
    }}
    body {{
        margin: 0;
        background: transparent;
        overflow: hidden;
    }}
    canvas {{
        display: block;
        background: transparent;
    }}
    """
    return f"""
    <html>
    <head>
        <style>
            {font_css}
        </style>
    </head>
    <body>
        <canvas id="textCanvas" width="{canvas_width}" height="{canvas_height}"></canvas>
        <img id="emoji-sprites" src="data:image/png;base64,{EMOJI_SPRITE_BASE64}" style="display: none;">
    </body>
    </html>
    """

def draw_text_js(line):
    """
    Generates the JavaScript to draw text and emojis.
    This version correctly handles kerning by drawing full words at a time.
    """
    # Using a JSON string for the emoji map to pass it to JavaScript
    emoji_map_js = json.dumps({
        "😐": {"x": 0, "width": 160},
        "🥀": {"x": 160, "width": 160},
        "🙏": {"x": 320, "width": 160},
        "😭": {"x": 480, "width": 160}
    })

    # This part is now handled in Python before creating the JavaScript string
    emoji_keys = list(json.loads(emoji_map_js).keys())
    escaped_emoji_keys = [re.escape(key) for key in emoji_keys]
    regex_emoji_part = "|".join(escaped_emoji_keys)

    return f"""
    const canvas = document.getElementById('textCanvas');
    const ctx = canvas.getContext('2d');
    const emojiSprites = document.getElementById('emoji-sprites');
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.font = "55px CustomFont";
    ctx.fillStyle = "white";
    ctx.strokeStyle = "black";
    ctx.lineWidth = 7;
    ctx.miterLimit = 2;
    ctx.textBaseline = "top";

    const maxWidth = 450;
    const lineHeight = 60;
    const emojiSize = 55; // Adjust to match font size

    const emojiMap = {emoji_map_js};

    // Create a regex to split the line by emojis and spaces, keeping them as tokens
    const emojiRegex = new RegExp(`({regex_emoji_part}|\\s+)`, 'g');

    // Measures the width of a line with mixed text and emojis
    function measureTextAndEmoji(text) {{
        let width = 0;
        const tokens = text.split(emojiRegex).filter(token => token.length > 0);

        for (const token of tokens) {{
            if (emojiMap[token]) {{
                width += emojiSize;
            }} else if (token === ' ') {{
                width += ctx.measureText(' ').width;
            }} else {{
                width += ctx.measureText(token).width;
            }}
        }}
        return width;
    }}

    // Wraps text and emojis to fit within the max width
    function wrapText(text, x, y, maxWidth, lineHeight) {{
        const words = text.split(' ');
        let line = '';
        let yOffset = y;
        
        for (let i = 0; i < words.length; i++) {{
            const word = words[i];
            const testLine = line + (line ? ' ' : '') + word;
            const testWidth = measureTextAndEmoji(testLine);

            if (testWidth > maxWidth) {{
                if (line) {{
                    renderLine(line, x, yOffset);
                    yOffset += lineHeight;
                    line = word;
                }} else {{
                    renderLine(word, x, yOffset);
                    yOffset += lineHeight;
                    line = '';
                }}
            }} else {{
                line = testLine;
            }}
        }}
        if (line) {{
            renderLine(line, x, yOffset);
        }}
    }}
    
    // Renders a single line by drawing words and emojis separately
    // Renders a single line by drawing words and emojis separately
// Renders a single line by drawing words and emojis separately
function renderLine(line, x, yOffset) {{
    const tokens = line.split(emojiRegex).filter(token => token.length > 0);
    let currentX = x - measureTextAndEmoji(line) / 2; // Center the line

    // The vertical alignment is the key. Let's align both to the top.
    const textVerticalOffset = 0; // Since textBaseline is "top"

    for (const token of tokens) {{
        if (emojiMap[token]) {{
            const sprite = emojiMap[token];
            ctx.drawImage(
                emojiSprites,
                sprite.x, 0, sprite.width, 160, // Source x, y, width, height
                currentX, yOffset - 4, emojiSize, emojiSize // Destination x, y, width, height
            );
            currentX += emojiSize;
        }} else if (token === ' ') {{
            currentX += ctx.measureText(' ').width;
        }} else {{
            const textWidth = ctx.measureText(token).width;
            ctx.strokeText(token, currentX, yOffset + textVerticalOffset);
            ctx.fillText(token, currentX, yOffset + textVerticalOffset);
            currentX += textWidth;
        }}
    }}
}}
    wrapText({line!r}, canvas.width / 2, 10, maxWidth, lineHeight);

    return canvas.toDataURL('image/png');
    """

def save_canvas_image(driver, line, filename):
    """
    Draws the text and emojis on the canvas and saves the result as a PNG file.
    """
    data_url = driver.execute_script(draw_text_js(line))
    header, encoded = data_url.split(',', 1)
    with open(filename, 'wb') as f:
        f.write(base64.b64decode(encoded))

def main(input_file):
    """
    Main function to process the input file and save images.
    """
    options = Options()
    options.headless = True

    try:
        driver = webdriver.Firefox(options=options)
    except Exception as e:
        print(f"Error starting WebDriver: {e}")
        print("Please ensure you have Firefox and geckodriver installed and in your PATH.")
        return

    with open(input_file, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            html = create_html()
            driver.get("data:text/html;charset=utf-8," + html)
            save_canvas_image(driver, line, f"temp/line_number_{i}.png")

    driver.quit()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python script.py input.txt")
    else:
        main(sys.argv[1])

