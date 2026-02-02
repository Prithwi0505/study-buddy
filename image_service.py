import pytesseract
from PIL import Image

def extract_text_from_image(file):
    """
    Extract text from image using Pillow + Tesseract
    Railway-safe (no OpenCV, no Windows paths)
    """

    image = Image.open(file).convert("L")  # grayscale
    text = pytesseract.image_to_string(
        image,
        config="--psm 6"
    )

    return text.strip()