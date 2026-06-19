from pyspark import SparkContext
import re
import matplotlib.pyplot as plt


class SparkClient:
    def run(self):
        # Create context
        ctx = SparkContext(appName="WordCount", master="local[*]")
        lines = ctx.textFile("content/ebook.txt")

        # Division in words
        words = lines \
            .flatMap(lambda line: re.split(r'\W+', line.lower())) \
            .filter(lambda word: len(word) > 3)

        # Count words
        word_counts = words.countByValue()
        fig = plt.figure(figsize=(10, 10))
        plt.bar(word_counts.keys(), word_counts.values(), color="green", width=0.5)
        plt.xlabel("Words")
        plt.ylabel("Frequency")
        plt.title("Histogram of words from file")
        plt.show()


if __name__ == '__main__':
    spark_client = SparkClient()
    spark_client.run()
