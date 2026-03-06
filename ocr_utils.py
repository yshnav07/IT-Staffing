import pytesseract
from PIL import Image

def extract_text_and_boxes(image_path):
    image = Image.open(image_path)
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

    words = []
    boxes = []

    for i in range(len(data["text"])):
        word = data["text"][i].strip()
        if word:
            words.append(word)
            x, y, w, h = (
                data["left"][i],
                data["top"][i],
                data["width"][i],
                data["height"][i],
            )
            boxes.append([x, y, x+w, y+h])

    return words, boxes, image.size