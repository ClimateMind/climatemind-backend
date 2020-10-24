FROM python:3.8.5-slim-buster

ENV FLASK_ENV=development

RUN mkdir -p /usr/share/man/man1
RUN apt-get update
RUN apt-get -y install gcc default-jre graphviz libgraphviz-dev graphviz-dev pkg-config
RUN apt-get install --reinstall build-essential -y
RUN apt-get update && apt-get install -y --no-install-recommends \
    unixodbc-dev \
    unixodbc \
    libpq-dev 
RUN apt-get -y install curl

RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -

RUN curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install msodbcsql17
RUN ACCEPT_EULA=Y apt-get install mssql-tools
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc

WORKDIR /app

COPY . .

RUN pip install cython && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 5000 8050

ENTRYPOINT [ "python" ]

RUN chmod u+x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
