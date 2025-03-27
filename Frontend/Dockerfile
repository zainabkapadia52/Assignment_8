FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir requests fastapi[standard] uvicorn gunicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9567"]