import re
import json
import argparse

def normalize_text(text):
    # Basic normalization: word numbers to digits and point variations to dot
    replacements = {
        'point': '.', 'poin': '.', 'dot': '.', 'full stop': '.'
    }
    for word, replacement in replacements.items():
        text = text.replace(word, replacement)

    # Simple word-to-digit for common small numbers
    word_to_num = {'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5'}
    for word, num in word_to_num.items():
        text = re.sub(rf'\b{word}\b', num, text, flags=re.IGNORECASE)

    return text

def split_suttas(text, book_id):
    # Regex for x.y.z where x is the book_id
    pattern = rf'({book_id}\.\d+\.\d+)'

    # Find all matches with their positions
    matches = list(re.finditer(pattern, text))

    suttas = []
    for i, match in enumerate(matches):
        start_idx = match.start()
        # Find the split point: look back for the last full stop or timestamp before this ID
        # For simplicity in boilerplate, we split right before the ID

        end_idx = matches[i+1].start() if i+1 < len(matches) else len(text)
        sutta_content = text[start_idx:end_idx].strip()

        suttas.append({
            "sutta_id": match.group(1),
            "content": sutta_content
        })

    return suttas

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", required=True)
    parser.add_argument("--book_id", required=True)
    args = parser.parse_args()

    with open(args.input_file, 'r', encoding='utf-8') as f:
        raw_text = f.read()

    clean_text = normalize_text(raw_text)
    sutta_list = split_suttas(clean_text, args.book_id)

    for sutta in sutta_list:
        filename = f"sutta_{sutta['sutta_id']}.json"
        with open(filename, 'w') as f:
            json.dump(sutta, f, indent=2)
        print(f"Generated {filename}")
