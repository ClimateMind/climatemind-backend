FROM python:3.8.5-slim-buster

ENV FLASK_ENV=development

RUN mkdir -p /usr/share/man/man1
RUN apt-get update
RUN apt-get -y install gcc default-jre graphviz libgraphviz-dev graphviz-dev pkg-config
RUN apt-get install --reinstall build-essential -y

#install sqlcmd and odbc and others
RUN apt-get update && apt-get install -y --no-install-recommends \
    unixodbc-dev \
    unixodbc \
    libpq-dev 


#RUN apt-get install mssql-server-polybase
#RUN apt-get install mssql-server-polybase-hadoop
#RUN systemctl restart mssql-launchpadd

RUN apt-get -y install curl
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -

RUN curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update
RUN apt install -y git

RUN ACCEPT_EULA=Y apt-get install msodbcsql17
RUN ACCEPT_EULA=Y apt-get install mssql-tools

RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc

RUN chmod +rwx /etc/ssl/openssl.cnf
RUN sed -i 's/TLSv1.2/TLSv1/g' /etc/ssl/openssl.cnf
RUN sed -i 's/SECLEVEL=2/SECLEVEL=1/g' /etc/ssl/openssl.cnf

# RUN sed -i "s/SSH_PORT/$SSH_PORT/g" /etc/ssh/sshd_config

#RUN sed -i -E 's/(CipherString\s*=\s*DEFAULT@SECLEVEL=)2/\11/' /etc/ssl/openssl.cnf
#RUN ACCEPT_EULA=Y apt-get install msodbcsql17=17.3.1.1-1 mssql-tools=17.3.0.1-1 -y
#RUN wget http://security.debian.org/debian-security/pool/updates/main/o/openssl1.0/libssl1.0.2_1.0.2s-1~deb9u1_amd64.deb \
#    && dpkg -i libssl1.0.2_1.0.2s-1~deb9u1_amd64.deb

WORKDIR /app

COPY . .

RUN pip install cython && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 5000 8050

RUN ["chmod", "+x", "db-init.sh"]

ENTRYPOINT [ "python" ]

RUN chmod u+x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]

#CMD [ "climatemind.py" ] #old entrypoint script.
