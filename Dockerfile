FROM bijoaja/template_flask:latest

# Buat direktori kerja
WORKDIR /app

# Copy file proyek
COPY . /app

# Install dependensi
RUN pip install --no-cache-dir -r requirements.txt

# Expose port Flask
EXPOSE 8080