# 1. Base Python image (Lightweight)
FROM python:3.11-slim

# 2. Install all required OS-level libraries for OpenCV & DeepFace
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libxcb1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 3. Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. THE MASTER STROKE: Uninstall GUI OpenCV & force Headless version during BUILD time
RUN pip uninstall -y opencv-python opencv-contrib-python && \
    pip install --no-cache-dir opencv-python-headless

# 5. Copy your actual code
COPY . .

# 6. Run Gunicorn with a longer timeout to allow Facenet to load properly
CMD gunicorn --timeout 120 --workers 1 --bind 0.0.0.0:$PORT face_api:app