FROM ubuntu:14.04
MAINTAINER Alex Perez "alex@percosys.com"
ENV DEBIAN_FRONTEND noninteractive

RUN sed 's/main$/main universe/' -i /etc/apt/sources.list && \
        apt-get update && \
        apt-get -y install \
            python \
            python-requests
        pip install dnsimple
        pip install pythondns

ADD ./dnsimple_update.py /dnsimple_update.py

ENTRYPOINT ["/usr/bin/python", "/dnsimple_update.py"]
