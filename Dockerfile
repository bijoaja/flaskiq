FROM python:3.12-slim

# Buat direktori kerja
WORKDIR /app

# Copy file proyek
COPY . /app

# Install dependensi
RUN pip install -r requirements.txt

# Expose port Flask
EXPOSE 8080

# Jalankan aplikasi
CMD ["flask", "run", "--host=0.0.0.0"]

