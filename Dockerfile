FROM python:3.11-slim

WORKDIR /app

# OpenCV가 필요로 하는 시스템 라이브러리
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements-server.txt .
RUN pip install --no-cache-dir -r requirements-server.txt

COPY src/ ./src/
COPY models/firearms_yolo_no_m16/best.pt ./models/firearms_yolo_no_m16/best.pt

ENV PORT=8080
EXPOSE 8080

CMD ["python", "-m", "uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8080"]