from random import shuffle
from collections import OrderedDict

from pyspark import SparkContext
import re
import matplotlib.pyplot as plt


class SparkClient:
    def run(self):
        # Create context
        ctx = SparkContext(appName="WordCount", master="local[*]")
        lines = ctx.textFile("content/Elliot-Forbes-Learning-Concurren.txt")

        # Division in words
        words = lines \
            .flatMap(lambda line: re.split(r'\W+', line.lower())) \
            .filter(lambda word: len(word) > 4)

        # Count words
        sorted_frequencies = sorted(words.countByValue().items(), key=lambda x: x[1])[-10:]
        word_counts = dict(sorted_frequencies)

        # Random shuffle
        keys = list(word_counts.keys())
        shuffle(keys)
        shuffled_words = OrderedDict(zip(keys, word_counts.values()))

        # Plot values
        fig = plt.figure(figsize=(50, 100))
        plt.bar(shuffled_words.keys(), shuffled_words.values(), color="blue", width=0.5)
        plt.xlabel("Words")
        plt.ylabel("Frequency")
        plt.title("Histogram of words from Elliot-Forbes-Learning-Concurrency ebook")
        plt.show()


if __name__ == '__main__':
    spark_client = SparkClient()
    spark_client.run()
