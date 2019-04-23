#!/usr/bin/env python

import json
import os
import time
import dnsimple
import requests
import dns.resolver
import socket

config_file = './dnsimple.json'


def get_config():
    config = {}
    config['noop'] = False
    try:
        with open(config_file) as d:
            config = json.load(d)
    except:
        pass
    config['noop'] = False
    return config


def __log(msg):
    print('{0} {1}'.format(time.strftime("%Y-%m-%dT%H:%M:%S"), msg))

def to_sec(u, v):
    if u == 's':
        return int(v)
    elif u == 'm':
        return int(v) * 60
    elif u == 'h':
        return int(v) * 3600
    else:
        return int(v)


def get_ext_ip():
    res = dns.resolver.Resolver()
    res.nameservers = [socket.gethostbyname('resolver1.opendns.com')]
    try:
        for ip in res.query('myip.opendns.com'):
            return ip
    except Exception as e:
        __log(e)


def create_record(host, record_type, content):
    try:
        __log('Creating "{0}" record for {1} using IP {2}'.format(record_type, host, content))
        if not config['noop']:
            data = {'name': host, 'record_type': record_type, 'content': str(content)}
            dsim.add_record(id_or_domain_name=config['domain'], data=data)
    except Exception as e:
        __log('ERR: Problem creating "{0}" record for {1} using IP {2}'.format(record_type, host, content))


def update_record(record, content):
    if str(record['content']) == str(content):
        __log('"{0}" record content is already set to {1} for {2}... Skipping update'.format(record['type'], content, record['name']))
        return
    else:
        try:
            __log('Updating record {0} for {1} using IP {2}'.format(record['id'], record['name'], content))
            if not config['noop']:
                dsim.update_record(id_or_domain_name=record['zone_id'], record_id=record['id'], data={'content': str(content)})
        except Exception as e:
            __log(e)
            __log('Problem updating record {0} for {1} using IP {2}'.format(record['id'], record['name'], content))


def main():
    unit = config['update'][-1].lower()
    if unit.isalpha():
        interval = config['update'][0:-1]
    else:
        interval = config['update']

    try:
        sec = to_sec(unit, interval)
    except ValueError:
        __log('ERR: Update interval is set to: {0}'.format(config['update']))
        __log('ERR: Problem trying to convert {0} to seconds...exiting'.format(interval))
        exit(1)

    while True:
        for host in config['hosts']:
            config['ipv4'] = get_ext_ip()
            ipv4_record = None
            if config['ipv4'] is None:
                have_ip = False
            else:
                have_ip = True
            try:
                domain_records = dsim.getrecords(id_or_domain_name=config['domain'])
            except:
                domain_records = None

            if not domain_records is None and have_ip:
                __log('About to update:')
                __log('{0}FQDN: {1}.{2} IPV4: {3}'.format(
                    '\t',
                    host,
                    config['domain'],
                    config['ipv4']
                    ))
                drnames = list(filter(None, [r['record']['name'] for r in domain_records]))
                if host in drnames:
                    for r in domain_records:
                        if str(r['record']['name']) == str(host):
                            cname_found = True if r['record']['type'] == 'CNAME' else False
                            ipv4_record = r['record'] if r['record']['type'] == 'A' else ipv4_record
                            if cname_found:
                                __log('WARN: {0} has a CNAME record, please delete before trying to update... Skipping update'.format(config['host']))
                                __log('Will sleep for {0} sec'.format(sec))
                                time.sleep(sec)
                                continue
                            if str(r['record']['content']) != str(config['ipv4']):
                                update_record(ipv4_record, config['ipv4'])
                            else:
                                __log('INFO: Record already up to date')
                else:
                    if not config['ipv4'] is None:
                        create_record(host, 'A', config['ipv4'])

            else:
                __log('WARN: Did not get any domain records for {0} or could not find external address for IPv4 and IPv6... skipping update this time'.format(config['domain']))
        __log('Will sleep for {0} sec'.format(sec))
        time.sleep(sec)

if __name__ == '__main__':
    config = get_config()
    dsim = dnsimple.DNSimple(api_token=config['api_token'])
    main()
