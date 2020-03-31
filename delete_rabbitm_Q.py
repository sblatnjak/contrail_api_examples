#!/usr/bin/env python
import argparse
import pika

#python delete_rabbitm_Q.py --ip 10.1.0.46 --port 5673 --queues "new_channel", "new_channel.1"

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

#host_ip = "10.1.0.38"
channel = pika.BlockingConnection(pika.ConnectionParameters(host_ip, port, "/", credentials=pika.PlainCredentials("guest","guest"))).channel()
for queue in queues:
    print("List of Qs to delete: {}".format(queue))
    channel.queue_delete(queue=queue)


channel.close()
