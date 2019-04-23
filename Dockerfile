FROM python:latest
MAINTAINER Alex Perez "alex@percosys.com"
WORKDIR /
COPY requirements.txt ./
COPY dnsimple.json ./
RUN pip install --no-cache-dir -r requirements.txt
ADD ./dnsimple_updater.py /dnsimple_updater.py
CMD ["python", "/dnsimple_updater.py"]
