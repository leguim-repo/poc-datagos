FROM python:3.9-alpine
RUN mkdir /app
ADD . /app
WORKDIR /app
COPY app /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 9999/udp
CMD ["python", "datagos_server.py"]
