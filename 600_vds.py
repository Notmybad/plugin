#!/usr/bin/python
# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE
import json
import os
import time


def fetch_vds_info_state():

    balance, version, blocks = 0, 0, 0

    try:
        raw_data = Popen(['vds-cli', 'getinfo'], stdout=PIPE, stderr=PIPE).communicate()[0]
        vds_info = json.loads(raw_data)
        balance = vds_info["balance"]
        version = vds_info["version"]
        blocks = vds_info["blocks"]
    except OSError:
        pass

    create_record('vds.info.balance', balance)
    create_record('vds.info.version', version)
    create_record('vds.info.blocks',  blocks)

def fetch_vds_mininginfo_state():

    genproclimit, localsolps, generate, pooledtx = 0, 0, False, 0

    try:
        raw_data = Popen(['vds-cli', 'getmininginfo'], stdout=PIPE, stderr=PIPE).communicate()[0]
        vds_info = json.loads(raw_data)
        genproclimit = vds_info["genproclimit"]
        localsolps = vds_info["localsolps"]
        generate = vds_info["generate"]
        pooledtx = vds_info["pooledtx"]
    except OSError:
        pass

    create_record('vds.mininginfo.genproclimit', genproclimit)
    create_record('vds.mininginfo.localsolps', localsolps)
    create_record('vds.mininginfo.generate',  generate)
    create_record('vds.mininginfo.pooledtx', pooledtx)

def fetch_vds_mempoolinfo_state():

    mempoolsize = 0

    try:
        raw_data = Popen(['vds-cli', 'getmempoolinfo'], stdout=PIPE, stderr=PIPE).communicate()[0]
        vds_info = json.loads(raw_data)
        mempoolsize = vds_info["size"]
    except OSError:
        pass

    create_record('vds.mempoolinfo.size', mempoolsize)

def create_record(metric, value):
    record = {}
    record['Metric']      = metric
    record['Endpoint']    = os.uname()[1]
    record['Timestamp']   = int(time.time())
    record['Step']        = 600
    record['Value']       = value
    record['CounterType'] = 'GAUGE'
    record['TAGS']        = 'vds'
    data.append(record)

if __name__ == '__main__':

    data = []
    fetch_vds_info_state()
    fetch_vds_mempoolinfo_state()
    fetch_vds_mininginfo_state()
    print json.dumps(data)
