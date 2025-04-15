FROM python:3.13-alpine

RUN mkdir /app

WORKDIR /app

EXPOSE 3000

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY *.json .
COPY *.py .

CMD ["python", "bot.py"]