FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY server.py ./server.py
COPY web ./web
COPY admin ./admin

EXPOSE 8000

CMD ["python", "server.py"]