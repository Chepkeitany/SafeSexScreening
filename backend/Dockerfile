# build with Python 3.7.5 Debian Buster image
FROM python:3.7.5-buster

# install NGINX
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
        nginx \
        sqlite3

# create and set working directory
RUN mkdir -p /backend/app
WORKDIR /backend

# copy application files and install requirements
COPY requirements.txt requirements.txt
COPY app app
COPY tests tests
COPY boot.sh ./
COPY *.py ./
COPY files/post-install/ /

RUN pip install -r requirements.txt
RUN chmod 755 boot.sh
RUN rm -rf /etc/nginx/sites-enabled/default /tmp/* /var/lib/apt/lists/*

# set environment variables
ENV FLASK_APP backend.py
ENV FLASK_CONFIG /backend/config.py

# expose ports and start server
EXPOSE 80
ENTRYPOINT ["./boot.sh"]
