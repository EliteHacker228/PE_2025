FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1=1.6.0-1 \
    libglib2.0-0=2.74.6-2+deb12u6 \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]