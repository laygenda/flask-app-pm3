# syntax=docker/dockerfile:1
FROM python:3.10-alpine
WORKDIR /flask

# Instal dependencies build untuk SQLite (gcc, musl-dev, linux-headers)
RUN apk add --no-cache gcc musl-dev linux-headers

# Salin dan instal dependencies Python
COPY requirement.txt requirement.txt
RUN pip install -r requirement.txt

# (Pengecekan Opsional)
RUN pwd
RUN ls -a

# Expose port (port aplikasi di dalam container)
EXPOSE 5000

# Salin seluruh kode aplikasi (termasuk folder 'board' dan file .env)
COPY . .

# Jalankan inisialisasi database sebelum server mulai
# Ini akan membuat file board.sqlite
RUN bash -c "python -m dotenv load && python -m flask --app board init-db"

# Perintah utama untuk menjalankan server Flask
CMD ['python', '-m', 'flask', '--app', 'board', 'run', '--host=0.0.0.0', '--debug']
