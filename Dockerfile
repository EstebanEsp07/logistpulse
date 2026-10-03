FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /srv/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ejecutar como usuario sin privilegios
RUN useradd --create-home appuser && chown -R appuser /srv/app
USER appuser

EXPOSE 8000

# 1 worker: la creación de tablas y el seed se ejecutan una sola vez al arrancar
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "1", "--threads", "4", "wsgi:app"]
