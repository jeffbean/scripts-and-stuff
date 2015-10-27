#!/usr/bin/env python
import argparse
import sys

import requests


parser = argparse.ArgumentParser()
parser.add_argument('jenkins_master')
parser.add_argument('slave_name')

jenkins_api = {'OK': 0,
               'WARNING': 1,
               'CRITICAL': 2,
               'UNKNOWN': 3}


def show_jenkins_slave_status(master_api_url, slave_name):
    jenkins_nodes_request = requests.get(master_api_url, )
    jenkins_nodes_request.raise_for_status()

    nodes_json = jenkins_nodes_request.json()
    for computer in nodes_json.get('computer', None):
        if str(computer.get('displayName').lower()) == str(slave_name.lower()):
            if computer.get('offline', False):
                print('Slave {} is OFFLINE! Reason: {}'.format(computer.get('displayName'),
                                                               computer.get('offlineCauseReason')))
                sys.exit(jenkins_api.get('CRITICAL'))
            else:
                print('Slave {} is online.'.format(computer.get('displayName')))
                sys.exit(jenkins_api.get('OK'))
    print('Node {} NOT FOUND! Case insensitive.'.format(slave_name))
    sys.exit(jenkins_api.get('UNKNOWN'))

if __name__ == '__main__':
    args = parser.parse_args()
    master_url = 'http://{}/computer/api/json'.format(args.jenkins_master)
    show_jenkins_slave_status(master_url, args.slave_name)
