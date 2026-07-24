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
    # e.g., 1.2.3
    pattern = rf'({book_id}\.\d+\.\d+)'

    # Split text into sentences using simple regex (can be improved with nltk/spacy)
    sentences = re.split(r'(?<=[.!?])\s+', text)

    suttas = []
    current_sutta_sentences = []
    current_sutta_id = None

    for sentence in sentences:
        match = re.search(pattern, sentence)
        if match:
            # If we found a new x.y.z, it becomes the first sentence of the new sutta
            if current_sutta_id is not None:
                # Save the previous sutta
                content = " ".join(current_sutta_sentences)
                # Heuristic tagging: For now just wrapping everything
                # This will be replaced by the ML model's tags
                tagged_content = f"*buddha* {content} *buddha*"
                suttas.append({
                    "sutta_id": current_sutta_id,
                    "processed_text": tagged_content
                })

            # Start a new sutta
            current_sutta_id = match.group(1)
            current_sutta_sentences = [sentence]
        else:
            current_sutta_sentences.append(sentence)

    # Add the last sutta
    if current_sutta_id is not None:
        content = " ".join(current_sutta_sentences)
        tagged_content = f"*buddha* {content} *buddha*"
        suttas.append({
            "sutta_id": current_sutta_id,
            "processed_text": tagged_content
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
