from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import os
from datetime import timedelta
import ast
import threading
from threading import Lock,Thread
from os import access
from pyspark import SparkConf,SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import Row,SQLContext
import sys
import requests

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
CORS(app, supports_credentials=True)

labels = []
values = []

def aggregate_tags_count(new_values, total_sum):
    return sum(new_values) + (total_sum or 0)


def get_sql_context_instance(spark_context):
    if ('sqlContextSingletonInstance' not in globals()):
        globals()['sqlContextSingletonInstance'] = SQLContext(spark_context)
    return globals()['sqlContextSingletonInstance']


def send_df_to_dashboard(df):
    global labels,values
    # extract the hashtags from dataframe and convert them into array
    top_tags = [str(t.hashtag) for t in df.select("hashtag").collect()]
    # extract the counts from dataframe and convert them into array
    tags_count = [p.hashtag_count for p in df.select("hashtag_count").collect()]

    labels = top_tags
    values = tags_count

def process_rdd(time, rdd):
    print("----------- %s -----------" % str(time))
    try:
        # Get spark sql singleton context from the current context
        sql_context = get_sql_context_instance(rdd.context)
        # convert the RDD to Row RDD
        row_rdd = rdd.map(lambda w: Row(hashtag=w[0][1:], hashtag_count=w[1]))
        # create a DF from the Row RDD
        hashtags_df = sql_context.createDataFrame(row_rdd)
        # Register the dataframe as table
        hashtags_df.registerTempTable("hashtags")
        # get the top 10 hashtags from the table using SQL and print them
        hashtag_counts_df = sql_context.sql("select hashtag, hashtag_count from hashtags order by hashtag_count desc limit 20")
        hashtag_counts_df.show()
        # call this method to prepare top 10 hashtags DF and send them
        send_df_to_dashboard(hashtag_counts_df)
    except:
        e = sys.exc_info()[0]
        print("Error: %s" % e)

def start_job():
    # create spark configuration
    conf = SparkConf()
    conf.setAppName("TwitterStreamApp")
    # create spark instance with the above configuration
    sc = SparkContext(conf=conf)
    sc.setLogLevel("ERROR")
    # creat the Streaming Context from the above spark context with window size 2 seconds
    ssc = StreamingContext(sc, 30)
    # setting a checkpoint to allow RDD recovery
    ssc.checkpoint("checkpoint_TwitterApp")
    # read data from port 9009
    dataStream = ssc.socketTextStream("localhost",9009)
    #print('dataStream is', dataStream.pprint())
    winLogs = dataStream.window(300, 30)
    #winCounts = winLogs.countByKey()
    # split each tweet into words
    #words = dataStream.flatMap(lambda line: line.split(" "))
    words = winLogs.flatMap(lambda line: line.split(" "))
    #print('words is, ', words.pprint())
    # filter the words to get only hashtags, then map each hashtag to be a pair of (hashtag,1)
    #hashtags = words.map(lambda x: (x, 1))
    hashtags = words.filter(lambda w: '#' in w).map(lambda x: (x, 1))
    #print('hashtag is : ', hashtags.pprint())
    # adding the count of each hashtag to its last count
    #tags_totals = hashtags.updateStateByKey(aggregate_tags_count)
    tags_totals = hashtags.reduceByKey(lambda a, b : a+b)
    tags_totals.pprint()
    # do processing for each RDD generated in each interval
    tags_totals.foreachRDD(process_rdd)

    # start the streaming computation
    ssc.start()
    # wait for the streaming to finish
    ssc.awaitTermination()


@app.route("/")
def chart():
    global labels,values
    labels = []
    values = []
    return render_template('chart.html', values=values, labels=labels)


@app.route('/refreshData')
def refresh_graph_data():
    global labels, values
    print("labels now: " + str(labels))
    print("data now: " + str(values))
    return jsonify(sLabel=labels, sData=values)

def start_server():
    app.run(port=5001)

if __name__ == '__main__':
    t1 = threading.Thread(target=start_job)
    t2 = threading.Thread(target=start_server)
    t1.start()
    t2.start()


   
