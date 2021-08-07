FROM ubuntu:20.04

RUN apt-get update
RUN apt -y upgrade
RUN apt install curl mlocate default-jdk -y
RUN apt install python3 -y
RUN apt install python3-pip -y
RUN apt show postgresql
RUN apt-get install postgresql postgresql-contrib -y

WORKDIR /sparkDir

RUN curl -O https://archive.apache.org/dist/spark/spark-3.1.1/spark-3.1.1-bin-hadoop3.2.tgz
RUN tar xvf spark-3.1.1-bin-hadoop3.2.tgz
RUN mv spark-3.1.1-bin-hadoop3.2/ /opt/spark

WORKDIR /Spark
RUN curl https://jdbc.postgresql.org/download/postgresql-42.2.23.jar --output postgresql-42.2.23.jar

# WORKDIR /sparklib
# COPY pyspark-3.1.2.tar.gz .
# RUN tar xvf pyspark-3.1.2.tar.gz
# RUN pip3 install setup.py

WORKDIR /app

COPY . /app

RUN pip3 install --no-cache-dir -r requirements.txt
RUN pyspark --packages org.postgresql:postgresql