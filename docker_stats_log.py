import json
import time
from datetime import datetime, timedelta

import docker
from hurry.filesize import size


def resource_report(container_name: str = 'postgres', config: dict = {}, filename: str = "resource_result.csv"):
    """ generate resource report as csv file. 

    Args:
        container_name (str, optional): container name. Defaults to 'postgres'.
        
        config (dict, optional): dict of env (environment) and action. Defaults to {}. 
        e.g. {'env':'zeta' ,'action': 'recal'}
        
        filename (str, optional): filename. Defaults to "resource_result.csv".
    """
    client = docker.from_env()

    for container in client.containers.list():
        if container.name == container_name:

            with open(filename, mode="w") as head_f:
                head_f.write(
                    "ENV,Action,Memory_limit (MiB),Date,Time,CPU_percentage,Memory_usage (MiB),Memory_percentage\n")

            while True:
                docker_resource = container.stats(stream=False)

                if process_finish(docker_resource):
                    return

                cpu_percent = json.dumps(
                    calculate_cpu_percent(docker_resource))
                cpu_percent = round(float(cpu_percent), 2)

                memory_stats = docker_resource["memory_stats"]
                memory_usage = memory_stats["usage"]
                memory_limit = memory_stats["limit"]
                
                memory_percent = memory_usage / memory_limit * 100
                memory_percent = round(float(memory_percent), 2)

                memory_usage_megabyte_no_suffix = size(
                    memory_usage, system=[(1024 ** 2, '')])
                memory_limit_megabyte_no_suffix = size(
                    memory_limit, system=[(1024 ** 2, '')])

                time_now = datetime.now() - timedelta(hours=7)

                with open(filename, mode="a") as f:
                    f.write("{:>6},{:>6},{:>10},{},{},{:10.2f},{:>10},{:10.2f}\n".format(
                        config.get('env', '-'),
                        config.get('action', '-'),
                        memory_limit_megabyte_no_suffix,
                        time_now.strftime("%Y-%m-%d"),
                        time_now.strftime("%H:%M:%S"),
                        cpu_percent,
                        memory_usage_megabyte_no_suffix,
                        memory_percent))

                time.sleep(1)


def process_finish(docker_resource: dict) -> bool:
    try:
        return not (docker_resource["cpu_stats"]["cpu_usage"]["percpu_usage"] or
                    docker_resource["cpu_stats"]["system_cpu_usage"] or
                    docker_resource["precpu_stats"]["system_cpu_usage"])
    except Exception:
        return True


def calculate_cpu_percent(docker_resource: dict) -> float:
    cpu_count = len(docker_resource["cpu_stats"]["cpu_usage"]["percpu_usage"])
    cpu_percent = 0.0
    cpu_delta = float(docker_resource["cpu_stats"]["cpu_usage"]["total_usage"]) - \
        float(docker_resource["precpu_stats"]["cpu_usage"]["total_usage"])
    system_delta = float(docker_resource["cpu_stats"]["system_cpu_usage"]) - \
        float(docker_resource["precpu_stats"]["system_cpu_usage"])
    if system_delta > 0.0:
        cpu_percent = cpu_delta / system_delta * 100.0 * cpu_count
    return cpu_percent


if __name__ == '__main__':
    config = {
        'env': "zeta",
        'action': "recal"
    }
    resource_report(container_name='dailka', config=config)
