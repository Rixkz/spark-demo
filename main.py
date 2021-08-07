from pyspark.sql import SparkSession

spark = SparkSession.builder\
    .config("spark.jars", "/Spark/postgresql-42.2.23.jar")\
    .config("spark.driver.extraClassPath", "/Spark/postgresql-42.2.23.jar")\
    .getOrCreate()

data = spark.read.format("jdbc") \
    .option("driver", "org.postgresql.Driver") \
    .option("url", "jdbc:postgresql://pgsql:5432/postgres") \
    .option("query", "select sum(salary) from public.employee") \
    .option("user", "postgres") \
    .option("password", "") \
    .load()

print(data)


    
