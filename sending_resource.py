import pika
import time
import json
import docker

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='cpu_resource')
channel.queue_declare(queue='memory_resource')

client = docker.from_env()
for x in range(0, 100):
    for i in client.containers.list():
        docker_information = i.stats(stream=False)
        cpu_stats = docker_information["cpu_stats"]
        memory_stats = docker_information["memory_stats"]

        channel.basic_publish(exchange='', routing_key='cpu_resource', body=json.dumps(cpu_stats))
        channel.basic_publish(exchange='', routing_key='memory_resource', body=json.dumps(memory_stats))
        print(" [x] Sent 'Hello World!'")
        time.sleep(1)
    time.sleep(1)
connection.close()