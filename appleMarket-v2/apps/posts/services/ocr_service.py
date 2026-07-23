import re

from paddleocr import PaddleOCR


ocr = PaddleOCR(
    lang="korean",
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
)


def find_number(patterns, text):
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return float(match.group(1))

    return None


def extract_nutrition(image_path):
    results = ocr.predict(image_path)

    recognized_texts = []

    for result in results:
        result_data = result.json

        # PaddleOCR 결과가 {"res": {...}} 형태인 경우 처리
        if "res" in result_data:
            result_data = result_data["res"]

        texts = result_data.get("rec_texts", [])

        for text in texts:
            if text:
                recognized_texts.append(str(text))

    full_text = " ".join(recognized_texts)

    print("OCR 인식 결과:", full_text)

    nutrition = {
        "calories": find_number(
            [
                r"(\d+(?:\.\d+)?)\s*kcal",
                r"(\d+(?:\.\d+)?)\s*칼로리",
                r"열량\s*(\d+(?:\.\d+)?)",
            ],
            full_text,
        ),
        "carbohydrates": find_number(
            [
                r"탄수화물\s*(\d+(?:\.\d+)?)\s*g?",
                r"탄수화물.*?(\d+(?:\.\d+)?)\s*g",
            ],
            full_text,
        ),
        "protein": find_number(
            [
                r"단백질\s*(\d+(?:\.\d+)?)\s*g?",
                r"단백질.*?(\d+(?:\.\d+)?)\s*g",
            ],
            full_text,
        ),
        "fat": find_number(
            [
                r"(?<!트랜스)(?<!포화)지방\s*(\d+(?:\.\d+)?)\s*g?",
                r"(?<!트랜스)(?<!포화)지방.*?(\d+(?:\.\d+)?)\s*g",
            ],
            full_text,
        ),
        "ocr_text": full_text,
    }

    return nutrition