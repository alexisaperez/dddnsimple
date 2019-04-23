FROM python:3.7
MAINTAINER Alex Perez "alex@percosys.com"
ENV DEBIAN_FRONTEND noninteractive

RUN pip install dnsimple
RUN pip install dnspython
RUN pip install requests
ADD ./src/ /
RUN ls
ENTRYPOINT ["/usr/bin/python", "/dnsimple_update.py"]
