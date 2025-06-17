FROM python:3.11-slim

WORKDIR /telegram_bot

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "bot.py"]