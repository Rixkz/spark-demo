# from pyspark.sql import SparkSession
import pika, sys, os
import time
from multiprocessing import Process, process

def spark_process(topic , statement):
    print("start process: {}".format(topic))
    # spark = SparkSession.builder\
    #     .config("spark.jars", "/Spark/postgresql-42.2.23.jar")\
    #     .config("spark.driver.extraClassPath", "/Spark/postgresql-42.2.23.jar")\
    #     .getOrCreate()

    # data = spark.read.format("jdbc") \
    #     .option("driver", "org.postgresql.Driver") \
    #     .option("url", "jdbc:postgresql://pgsql:5432/postgres") \
    #     .option("query", statement) \
    #     .option("user", "postgres") \
    #     .option("password", "") \
    #     .load()
    # print(data)


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

spark_process(
    "summary total cre",
    "select loan_id,sum(amount) from ntbx_datawarehouse.raw_cal_service_loan_payment_bucket_cre rcslpbc group by loan_id "
)


if __name__ == '__main__':
    try:
        topic = "summary total cre"
        statment = "select loan_id,sum(amount) from ntbx_datawarehouse.raw_cal_service_loan_payment_bucket_cre rcslpbc group by loan_id "
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
