FROM python:3.11-alpine AS base

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	JWT_EXPIRATION_DAYS=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN addgroup -S app && adduser -S app -G app
COPY --chown=app:app . .

EXPOSE 2013

FROM base AS dev
ENV FLASK_ENV=development
CMD ["python", "main.py"]

FROM base AS production
ENV FLASK_ENV=production
USER app
CMD ["gunicorn", "-w", "2", "-k", "gthread", "--threads", "4", "-b", "0.0.0.0:2013", "main:app"]