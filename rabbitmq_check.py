import argparse
import subprocess
import os
import json
import requests
from requests.auth import HTTPBasicAuth

#auth=HTTPBasicAuth(self.SECRET_USERNAME, self.SECRET_PASSWORD)

def get_args():
    parser = argparse.ArgumentParser(description='Process args')

    parser.add_argument('-p', '--port', type=int, help='rabbit port (default is 15673)', required=False)
    parser.add_argument('-ips', '--ips', type=str, nargs='+', help='IPs of the rabbit hosts/contrail control nodes', required=True)
    args = parser.parse_args()
    
    port = args.port
    ips = args.ips
    
    return port, ips

port = '15673'
port, ips = get_args()



for ip in ips:
    print 'IP: '+ip
    request = requests.get('http://'+ip+':'+str(port)+'/api/queues/', auth=HTTPBasicAuth('guest','guest'))
    resp=json.loads(request.text)
    for r in resp:      
        print 'Q name: ' + r['name']
        print 'number of messages: ' + str(r['messages'])
        if (int(r['messages'])>10):
            print "ALARM"
            #TODO email notification

#TODO cluster healthcheck (/api/nodes/, )
