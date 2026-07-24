import vertexai
from vertexai.generative_models import GenerativeModel, Part

def extract_doctrinal_chain(project, location, sutta_text, book_number):
    vertexai.init(project=project, location=location)
    model = GenerativeModel("gemini-1.5-flash")

    prompt = f"""
    You are a Buddhist scholar. From the teacher's commentary below,
    extract exactly {book_number} sequential points that form the 'Doctrinal Chain'.

    Commentary:
    {sutta_text}

    Output exactly {book_number} numbered points.
    """

    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    # Placeholder
    pass
