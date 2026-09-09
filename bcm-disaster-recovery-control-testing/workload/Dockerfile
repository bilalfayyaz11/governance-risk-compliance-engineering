FROM python:3.12-slim

WORKDIR /app

COPY app.py /app/app.py

RUN useradd -r -u 10001 appuser \
    && mkdir -p /data \
    && chown -R appuser:appuser /app /data

USER appuser

EXPOSE 8080

CMD ["python", "/app/app.py"]
