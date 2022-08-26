FROM python:3.9-alpine
RUN mkdir /server
ADD . /server
WORKDIR /server
COPY server /server
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 9999/udp
CMD ["python", "/server/app/datagos_server.py"]
