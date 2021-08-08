import pika
import time
import json
import docker
from hurry.filesize import size

def producer():
    conn_param = pika.ConnectionParameters(host='localhost')
    connection = pika.BlockingConnection(conn_param)
    channel = connection.channel()

    channel.queue_declare(queue='cpu_percent_usage')
    channel.queue_declare(queue='memory_mb_usage')

    docker_client = docker.from_env()
    for x in range(0, 100):
        for container_object in docker_client.containers.list():
            if container_object.name == 'spark':
                docker_information = container_object.stats(stream=False)
                cpu_stats = json.dumps(calculate_cpu_percent(docker_information))
                memory_stats = docker_information["memory_stats"]
                channel.basic_publish(exchange='', routing_key='cpu_percent_usage', body=cpu_stats)
                channel.basic_publish(exchange='', routing_key='memory_mb_usage', body=size(memory_stats["usage"]))
                print(" [x] Sent container usage.")   
        time.sleep(1)
    connection.close()

def calculate_cpu_percent(d):
    cpu_count = len(d["cpu_stats"]["cpu_usage"]["percpu_usage"])
    cpu_percent = 0.0
    cpu_delta = float(d["cpu_stats"]["cpu_usage"]["total_usage"]) - \
                float(d["precpu_stats"]["cpu_usage"]["total_usage"])
    system_delta = float(d["cpu_stats"]["system_cpu_usage"]) - \
                   float(d["precpu_stats"]["system_cpu_usage"])
    if system_delta > 0.0:
        cpu_percent = cpu_delta / system_delta * 100.0 * cpu_count
    return cpu_percent

if __name__ == '__main__':
    producer()