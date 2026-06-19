import json
from datetime import datetime

from pyspark import SparkContext
from pyspark.streaming import StreamingContext


def print_info(json_obj):
    if len(json_obj) != 0:
        print("Received " + str(json_obj))
        print("First element " + str(json_obj[0]))

        # corect ca e un array
        json_file = json.loads(json_obj[0])

        # if pentru filtrarea news

        # aparent ghilimelee sunt trimise ok aici

        # primesc informatia, dar nu ma lasa sa o tratez ca un obiect json ca sa ii accesez membrii :))

        date_ = datetime.fromtimestamp(json_file['datetime']).strftime("%A, %B %d, %Y %I:%M:%S")
        print()

        print("==========================================")
        print(json_file['headline'])
        print(str(date_))
        print(json_file['url'])
        print("==========================================")

        print()


if __name__ == "__main__":
    # Deci in primul rand am nevoie de un Spark context
    # context
    # setMaster("local[2]").setName("News")
    spark_context = SparkContext("local[2]", "News")

    # nu stiu ce reprezinta 1 ala
    streaming_context = StreamingContext(spark_context, 1)

    # imi creez streamul de date
    lines = streaming_context.socketTextStream("127.0.0.1", 8910)

    # imi fac flow-ul de rdd
    # conditia era ca sa fie de tip jpg si sa aiba dimensiunea imagina mai mica de 150
    # Lasa asa :))
    lines.foreachRDD(lambda rdd: print_info(rdd.collect()))

    streaming_context.start()
    streaming_context.awaitTermination()
