import torch
from transformers import LayoutLMv3Processor, LayoutLMv3ForTokenClassification

processor = LayoutLMv3Processor.from_pretrained("microsoft/layoutlmv3-base", apply_ocr=False)
model = LayoutLMv3ForTokenClassification.from_pretrained(
    "microsoft/layoutlmv3-base",
    num_labels=6
)

labels = ["O", "NAME", "SKILL", "EXPERIENCE", "EDUCATION", "ORG"]

def normalize_box(box, width, height):
    return [
        int(1000 * box[0] / width),
        int(1000 * box[1] / height),
        int(1000 * box[2] / width),
        int(1000 * box[3] / height),
    ]

def extract_entities(words, boxes, image_size):
    width, height = image_size
    boxes = [normalize_box(b, width, height) for b in boxes]

    encoding = processor(
        words,
        boxes=boxes,
        return_tensors="pt",
        truncation=True,
        padding="max_length"
    )

    outputs = model(**encoding)
    predictions = torch.argmax(outputs.logits, dim=-1)

    return predictions


def structure_output(words, predictions):
    extracted = {
        "skills": [],
        "experience": [],
        "education": []
    }

    for word, pred in zip(words, predictions[0]):
        label = labels[pred]
        if label == "SKILL":
            extracted["skills"].append(word)
        elif label == "EXPERIENCE":
            extracted["experience"].append(word)
        elif label == "EDUCATION":
            extracted["education"].append(word)

    return extracted