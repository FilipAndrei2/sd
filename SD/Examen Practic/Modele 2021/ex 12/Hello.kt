package com.sd.laborator

import kotlinx.serialization.json.Json
import kotlinx.serialization.json.jsonArray
import kotlinx.serialization.json.jsonObject
import org.apache.spark.SparkConf
import org.apache.spark.streaming.Durations
import org.apache.spark.streaming.api.java.JavaStreamingContext
import java.io.File
import java.lang.Math.abs
import java.util.*

var positive_words= File("positive-words.txt").readLines()
var negative_words = File("negative-words.txt").readLines()

fun printData(jsonObj: List<String>){
    if(jsonObj.size != 0){
        val jsonData = Json.parseToJsonElement(jsonObj[0])
        val news = jsonData.jsonArray[0].jsonObject

        val summary=news.getValue("summary").toString()
        val words =summary.toLowerCase().split(" ")
        var tolerance = 0.05
        var pos_procentage=0
        var neg_procentage=0
        var pos=0
        var neg=0
        for (word in words) {
            if ((word + "\n") in positive_words) {
                pos += 1
            }
            if ((word + "\n") in negative_words) {
                neg += 1
            }
            pos_procentage = pos / words.size
            neg_procentage = neg / words.size
            print("Content:" + summary)
        }
        if (abs(pos_procentage - neg_procentage) < tolerance) {
            print("\nNeutral post")
        }
        else if( pos_procentage > neg_procentage) {
            print("\nPositive post")
        }
        else {
            print("\nNegative post")
        }
    }
}


fun main() {
    val conf = SparkConf().setMaster("local[2]").setAppName("News")
    val jssc = JavaStreamingContext(conf, Durations.seconds(1))

    val stream = jssc.socketTextStream("127.0.0.1", 65432)
    stream.foreachRDD { rdd-> printData(rdd.collect()) }

    jssc.start()
    jssc.awaitTermination()
}
