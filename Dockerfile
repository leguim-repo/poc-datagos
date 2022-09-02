FROM python:3.9-alpine
RUN apk add --update --no-cache --virtual .tmp-build-deps gcc libc-dev linux-headers zlib zlib-dev libffi-dev rust cargo openssl-dev
COPY requirements.txt requirements.txt
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt
# Mein App
RUN mkdir /app
ADD . /app
WORKDIR /app
COPY server /app
EXPOSE 9999/udp
CMD ["python", "/app/datagos_server.py"]
