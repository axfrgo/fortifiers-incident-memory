FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src
WORKDIR /app

COPY requirements-lock.txt /app/requirements-lock.txt
RUN python -m pip install --no-cache-dir -r requirements-lock.txt
COPY pyproject.toml /app/pyproject.toml
COPY src /app/src
RUN mkdir -p /app/artifacts/demo && \
    useradd --create-home --uid 10001 app && \
    chown -R app:app /app
USER 10001

EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s --start-period=20s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/health', timeout=2)"
CMD ["python", "-m", "uvicorn", "incident_memory.api:app", "--host", "0.0.0.0", "--port", "8080", "--proxy-headers"]
