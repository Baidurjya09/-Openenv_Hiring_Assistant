FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Environment variables (override at runtime)
ENV API_BASE_URL=https://router.huggingface.co/v1
ENV MODEL_NAME=gpt-4o-mini
ENV API_KEY=""
ENV HF_TOKEN=""

# Run web server (keeps container alive)
CMD ["python", "app.py"]
