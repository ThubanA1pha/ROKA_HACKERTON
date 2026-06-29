import re
from functools import lru_cache

import cv2
import easyocr

# 총번은 5~8자리 숫자(예: 2231140, 100742, 04412) — 그 외 문자는 노이즈로 간주
_DIGIT_PATTERN = re.compile(r"\d{4,8}")


@lru_cache(maxsize=1)
def _get_reader():
    """EasyOCR Reader 초기화는 비용이 커서 프로세스당 한 번만 생성해 재사용한다."""
    return easyocr.Reader(["en"], gpu=False)


def _crop_with_margin(image, box, margin_ratio: float = 0.08):
    h, w = image.shape[:2]
    x1, y1, x2, y2 = box
    mx, my = (x2 - x1) * margin_ratio, (y2 - y1) * margin_ratio
    x1, y1 = max(0, int(x1 - mx)), max(0, int(y1 - my))
    x2, y2 = min(w, int(x2 + mx)), min(h, int(y2 + my))
    return image[y1:y2, x1:x2]


def recognize_serial(image, box, upscale: int = 3) -> dict:
    """탐지된 총기 bbox 영역에서 각인된 총번(숫자열)을 OCR로 읽는다.

    image: BGR numpy 배열 (원본 이미지)
    box: (x1, y1, x2, y2) 픽셀 좌표
    반환: {"text": "2231140" | None, "confidence": 0.0~1.0}
    """
    crop = _crop_with_margin(image, box)
    if crop.size == 0:
        return {"text": None, "confidence": 0.0}

    # 각인 숫자는 총기 전체 사진에서 매우 작게 나오므로 확대 후 OCR
    crop = cv2.resize(crop, None, fx=upscale, fy=upscale, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

    reader = _get_reader()
    results = reader.readtext(gray, allowlist="0123456789")

    candidates = [
        (match.group(), conf)
        for _, text, conf in results
        for match in [_DIGIT_PATTERN.search(text)]
        if match
    ]
    if not candidates:
        return {"text": None, "confidence": 0.0}

    text, conf = max(candidates, key=lambda c: c[1])
    return {"text": text, "confidence": round(float(conf), 4)}


def recognize_serials_for_result(result) -> list[dict]:
    """YOLO Results 객체 하나에 대해 박스별 총번 OCR 결과 리스트를 반환한다."""
    image = result.orig_img
    return [recognize_serial(image, box) for box in result.boxes.xyxy.tolist()]
