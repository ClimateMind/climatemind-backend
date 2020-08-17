FROM python:3.8.5-slim-buster

ENV FLASK_ENV=development
RUN apt-get update
RUN apt-get -y install gcc

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

RUN ls

COPY . .

EXPOSE 5000
CMD [ "python", "./climatemind.py" ]
