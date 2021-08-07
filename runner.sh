docker rm test-spark
docker build -t spark-app .
docker run --name test-spark spark-app