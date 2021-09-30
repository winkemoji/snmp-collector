#!/bin/bash
service rabbitmq-server start
cd /snmp-collector
python start.py "$@"