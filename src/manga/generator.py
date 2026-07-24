import vertexai
from vertexai.preview.vision_models import ImageGenerationModel

def generate_manga_panel(project, location, sutta_summary, output_uri):
    vertexai.init(project=project, location=location)
    model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")

    # Tezuka Osamu style prompt
    prompt = f"""
    Manga panel in the classic style of Tezuka Osamu (Astro Boy, Buddha).
    Black and white ink drawing, clean lines, expressive characters.
    Scene: {sutta_summary}.
    Dramatic composition, 1950s manga aesthetic.
    """

    images = model.generate_images(
        prompt=prompt,
        number_of_images=1,
        language="en",
        aspect_ratio="1:1"
    )

    images[0].save(output_uri)
    return output_uri
