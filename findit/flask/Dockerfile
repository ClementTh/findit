FROM python:3.8

RUN apt-get update && apt-get install -y \
    build-essential \
    wget 

ADD ./app /app
ADD requirements.txt .

RUN pip install --no-cache-dir --upgrade pip
RUN pip3 install -r requirements.txt

WORKDIR /app


