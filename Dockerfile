FROM python:3.8.5-slim-buster

ENV FLASK_ENV=development

RUN mkdir -p /usr/share/man/man1
RUN apt-get update
RUN apt-get -y install gcc default-jre graphviz libgraphviz-dev graphviz-dev pkg-config

WORKDIR /app

COPY . .

RUN pip install cython && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 5000 8050

ENTRYPOINT [ "python" ]

CMD [ "climatemind.py" ]

