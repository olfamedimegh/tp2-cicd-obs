FROM python:3.12-slim

WORKDIR /app
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ /app/
ENV PORT=8000 \
    PYTHONUNBUFFERED=1 \
    SERVICE_NAME=tp2-flask-app \
    OTLP_ENDPOINT=http://otel-collector:4318

EXPOSE 8000
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "main:app"]