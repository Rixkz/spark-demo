from pyspark.sql import SparkSession
import pika, sys, os
import time
from multiprocessing import Process

def spark_process(topic , statement):
    for x in range(0, 100):
        print("start process: {}".format(topic))
        spark = SparkSession.builder\
            .config("spark.jars", "/Spark/postgresql-42.2.23.jar")\
            .config("spark.driver.extraClassPath", "/Spark/postgresql-42.2.23.jar")\
            .getOrCreate()

        data = spark.read.format("jdbc") \
            .option("driver", "org.postgresql.Driver") \
            .option("url", "jdbc:postgresql://pgsql:5432/postgres") \
            .option("query", statement) \
            .option("user", "postgres") \
            .option("password", "") \
            .load()
        print(data)
        time.sleep(1)

def main():
    conn_param = pika.ConnectionParameters(host='localhost')
    connection = pika.BlockingConnection(conn_param)
    channel = connection.channel()

    channel.queue_declare(queue='cpu_percent_usage')
    channel.queue_declare(queue='memory_mb_usage')

    def callback(ch, method, properties, body):
        routing_key = method.routing_key
        print(" [x] Received {0}: {1}".format(routing_key, body.decode("utf-8") ))

    channel.basic_consume(queue='cpu_percent_usage', on_message_callback=callback, auto_ack=True)
    channel.basic_consume(queue='memory_mb_usage', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        topic = "summary total cre"
        statment = "select employee_id , sum(salary) from public.employee group by employee_id"
        p1 = Process(target=main)
        p2 = Process(target=spark_process, args=(topic, statment))
        p1.start()
        p2.start()
        
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
