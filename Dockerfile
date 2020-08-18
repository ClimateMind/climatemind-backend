FROM python:3.8.5-slim-buster

ENV FLASK_ENV=development
RUN apt-get update
RUN apt-get -y install gcc graphviz-dev

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install cython && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENTRYPOINT [ "python" ]

CMD [ "climatemind.py" ]
