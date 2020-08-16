FROM python:3.8-alpine

EXPOSE 5000

#RUN apt-get install graphviz
WORKDIR ./

#COPY requirements.txt .
COPY knowledge_graph/ .

RUN pip freeze > requirements.txt

RUN pip install -r requirements.txt

RUN ls

RUN export FLASK_ENV=development


ENTRYPOINT [ "python" ]

CMD [ "__init__.py" ]

