FROM python:3.10-slim-buster

COPY prometheus_esmr5 /app
WORKDIR /app

RUN python3 -m pip install --no-cache --upgrade -r ./requirements.txt

EXPOSE 8000
CMD ["/usr/local/bin/python3", "-u", "./main.py"]