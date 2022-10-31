FROM python:3.8.5-slim-buster

ENV FLASK_ENV=development

RUN mkdir -p /usr/share/man/man1
RUN apt-get update && apt-get -y install \
    gcc \
    default-jre \
    graphviz \
    libgraphviz-dev \
    graphviz-dev \
    pkg-config \
    build-essential \
    unixodbc-dev \
    unixodbc \
    libpq-dev \
    curl \
    git

RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list

RUN apt-get update && ACCEPT_EULA=Y apt-get install msodbcsql17  mssql-tools

RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc

RUN chmod +rwx /etc/ssl/openssl.cnf
RUN sed -i 's/TLSv1.2/TLSv1/g' /etc/ssl/openssl.cnf
RUN sed -i 's/SECLEVEL=2/SECLEVEL=1/g' /etc/ssl/openssl.cnf

WORKDIR /app

ADD requirements/ requirements/
RUN pip install cython && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements/requirements.txt && \
    pip install --no-cache-dir -r requirements/requirements_dev.txt && \
    pip install --no-cache-dir -r requirements/requirements_test.txt

COPY . .

EXPOSE 5000 8050

COPY . .

RUN chmod u+x /app/docker/services/api/entrypoint.sh
ENTRYPOINT ["/app/docker/services/api/entrypoint.sh"]
