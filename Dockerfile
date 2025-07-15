FROM bijoaja/flaskiq:latest

# Buat direktori kerja
WORKDIR /app

# Copy file proyek
COPY . /app

# Install dependensi
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y curl

# Expose port Flask
EXPOSE 8080