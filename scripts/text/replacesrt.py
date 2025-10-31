def replace_srt_captions(srt_path, txt_path, output_path):
    with open(srt_path, 'r', encoding='utf-8') as srt_file:
        srt_lines = srt_file.readlines()

    with open(txt_path, 'r', encoding='utf-8') as txt_file:
        new_captions = [line.strip() for line in txt_file.readlines()]

    output_lines = []
    caption_index = 0
    i = 0
    n = len(srt_lines)

    while i < n:
        # Subtitle number
        output_lines.append(srt_lines[i])
        i += 1

        # Timecode line
        output_lines.append(srt_lines[i])
        i += 1

        # Replace the caption text lines
        caption_text_lines = []
        while i < n and srt_lines[i].strip() != '':
            caption_text_lines.append(srt_lines[i])
            i += 1

        # Replace original caption text with new caption(s)
        if caption_index < len(new_captions):
            new_caption = new_captions[caption_index]
            caption_index += 1
            # If the new caption contains multiple lines separated by \n, split them
            for line in new_caption.split('\\n'):
                output_lines.append(line + '\n')
        else:
            # If no new captions left, keep original caption
            output_lines.extend(caption_text_lines)

        # Append the blank line separating captions
        if i < n:
            output_lines.append(srt_lines[i])
            i += 1

    with open(output_path, 'w', encoding='utf-8') as out_file:
        out_file.writelines(output_lines)


# Example usage:
replace_srt_captions('temp/output.srt', 'temp/bracketed.json', 'temp/replaced.srt')

