FROM python:3.7
MAINTAINER Alex Perez "alex@percosys.com"
ENV DEBIAN_FRONTEND noninteractive

RUN pip install dnsimple
RUN pip install pythondns
RUN pip install requests
ADD ./dnsimple_update.py /dnsimple_update.py

ENTRYPOINT ["/usr/bin/python", "/dnsimple_update.py"]
