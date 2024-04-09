FROM python:3.10-bookworm

WORKDIR /app

COPY ./requirements.txt requirements.txt

RUN pip3 install -r requirements.txt 

COPY . .

CMD gunicorn --bind 0.0.0.0:$PORT app:app
