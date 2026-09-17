def clean_text(text):
    text=text.replace("\n", " ")
    return text
def clean_text(text):
    # Remove excessive spaces while preserving paragraph breaks
    lines = text.splitlines()

    cleaned_lines = []

    for line in lines:
        line = line.strip()

        if line:
            cleaned_lines.append(line)

    return "\n".join(cleaned_lines)