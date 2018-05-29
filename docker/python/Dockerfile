FROM python:3.6.5-stretch

ENV PYTHONUNBUFFERED=0

# install required libs
RUN apt-get update && apt-get install -y \
    python-psycopg2 libpq-dev sqlite3 \
    telnet lsof vim

# add requirements.txt
ADD ./files/requirements.txt /files/requirements.txt

# start installing py packages
RUN pip install -r /files/requirements.txt -q

# start adding files
ADD ./files /files

# set the root dir
WORKDIR /web
