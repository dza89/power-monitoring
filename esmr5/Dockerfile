FROM python:3.8-slim-buster

RUN pip3 install --upgrade --no-cache\
        prometheus_client \
        smeterd

WORKDIR /prometheus_esmr5
EXPOSE 8000/tcp
EXPOSE 8000/udp
COPY  prometheus_esmr5 /prometheus_esmr5
CMD ["/usr/local/bin/python3", "-u", "/prometheus_esmr5/main.py"]