FROM python:3.6.15-slim-buster
WORKDIR /
COPY ./requirements.txt /snmp-collector/reqiurements.txt
COPY ./snmp-collector /snmp-collector/snmp-collector
COPY ./monitor /snmp-collector/monitor
COPY ./superserver.py /snmp-collector/superserver.py
COPY ./start.py /snmp-collector/start.py
COPY ./start.sh /start.sh
RUN  sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
RUN apt-get update
RUN apt-get install snmp snmpd -y
RUN apt-get install erlang -y
RUN apt-get install rabbitmq-server -y
RUN pip install --no-cache-dir -r /snmp-collector/reqiurements.txt
ENTRYPOINT ["sh", "./start.sh"]