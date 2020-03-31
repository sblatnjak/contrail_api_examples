#!/usr/bin/env python
import argparse
import pika

#python del_qs.py --ip 10.1.0.46 --port 5673 --queues "new_channel" "new_channel.12" "new_channel.123"

def get_args():
    parser = argparse.ArgumentParser(description='Process some integers.')

    parser.add_argument('-ip', '--ip', type=str, help='ip address of the rabbit host', required=True)
    parser.add_argument('-p', '--port', type=int, help='rabbit port (default is 5673)', required=False)
    parser.add_argument('-q', '--queues', type=str, nargs='+', help='Q names to delete', required=True)

    args = parser.parse_args()

    host_ip = args.ip
    port = args.port
    queues = args.queues

    return host_ip, port, queues

host_ip, port, queues = get_args()

channel = pika.BlockingConnection(pika.ConnectionParameters(host_ip, port, "/", credentials=pika.PlainCredentials("guest","guest"))).channel()
for q in queues:
    print("List of Qs to delete: {}".format(q))
    channel.queue_delete(queue=q)


channel.close()
