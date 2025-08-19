FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./src/
COPY roms/ ./roms/
COPY saves/ ./saves/
RUN chmod 755 /app/temp

CMD ["python", "src/bot.py"]