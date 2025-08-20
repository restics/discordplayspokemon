FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./src/
COPY roms/ ./roms/
COPY saves/ ./saves/
RUN mkdir -p /app/temp /app/data && chmod 755 /app/temp /app/data

CMD ["python", "src/bot.py"]