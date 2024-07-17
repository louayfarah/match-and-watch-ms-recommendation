FROM python:3.11-bullseye
RUN apt-get update && apt-get install -y python3-pip
RUN pip install --upgrade pip
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY . /app
EXPOSE 8000
RUN chmod +x run_server.sh
CMD ["/bin/sh", "./run_server.sh"]