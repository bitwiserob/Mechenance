FROM python:3.10-bookworm

WORKDIR /app

COPY ./requirements.txt requirements.txt

RUN pip3 install -r requirements.txt 

RUN mkdir -p /root/.postgresql && chmod 700 /root/.postgresql

COPY root.crt /root/.postgresql/root.crt

ENV DATABASE_URL = ""

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
#CMD gunicorn --bind 0.0.0.0:$PORT app:app
