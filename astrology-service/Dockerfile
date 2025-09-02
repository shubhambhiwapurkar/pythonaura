FROM python:3.9-slim

WORKDIR /app/astrology-service

COPY astrology-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY astrology-service/ .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
