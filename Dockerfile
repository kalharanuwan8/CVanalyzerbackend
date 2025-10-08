# -----------------------------
# 1️⃣ Base image
# -----------------------------
FROM python:3.11-slim

# Set environment vars
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# -----------------------------
# 2️⃣ Set working directory
# -----------------------------
WORKDIR /app

# -----------------------------
# 3️⃣ Copy project files
# -----------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

# -----------------------------
# 4️⃣ Expose port and start app
# -----------------------------
EXPOSE 8000

# -----------------------------
# 5️⃣ Command to run FastAPI
# -----------------------------
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
