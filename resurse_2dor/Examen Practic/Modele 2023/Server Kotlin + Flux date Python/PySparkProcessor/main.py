import json
import os

from pyspark import SparkContext
from pyspark.streaming.context import StreamingContext
from pyspark.storagelevel import StorageLevel
from datetime import datetime


def print_data(j_data):
    # Afisare formatata a datelor procesate
    for item in j_data:
        date = datetime.utcfromtimestamp(int(item["datetime"])).strftime('%Y-%m-%d')
        print(f'URL: {item["url"]},\tData: {date},\tTitle: {item["headline"]}')


class SparkClient:
    PARAMETERS = {
        "host": "localhost",
        "port": 5678
    }

    def __init__(self):
        os.environ["PYSPARK_PYTHON"] = "python3"
        os.environ["PYSPARK_DRIVER_PYTHON"] = "python3"

    def run(self):
        ctx = SparkContext(appName="streaming", master="local[*]")
        ctx.setLogLevel("ERROR")

        # Creare context spark si conectare la socket TCP
        spark_context = StreamingContext(ctx, 3)
        data = spark_context.socketTextStream(self.PARAMETERS["host"], self.PARAMETERS["port"])

        # Adaugare nivel de persistenta
        data.persist(StorageLevel.MEMORY_AND_DISK)

        # Procesare date
        json_data = data \
            .map(lambda x: json.loads(x)) \
            .filter(lambda j_data: len(j_data["url"]) <= 280) \
            # .filter(lambda j_data: j_data["image"][-3:] != "jpg")

        # Colectare date si trimitere spre afisare
        json_data.foreachRDD(lambda rdd: print_data(rdd.collect()))

        spark_context.start()
        spark_context.awaitTermination()
        spark_context.stop()


if __name__ == '__main__':
    # Creare client spark
    sparkClient = SparkClient()
    sparkClient.run()
