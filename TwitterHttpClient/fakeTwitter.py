import socket
import sys
import os
import jsonlines
import time

path = './oldtweet/json'
files = os.listdir(path)
file1 = files[0]

def get_tweets(tcp_connection):
    content = []
    for file in files:
        with open(path + '/' + file, 'r+', encoding='utf8') as f:
            cnt = 0
            for item in jsonlines.Reader(f):
                cnt += 1
                # print(item)
                content.append(item['full_text'])
                if cnt == 5:
                    cnt = 0
                    for twt in content:
                        try:
                            print("Tweet Text: " + twt)
                            print ("------------------------------------------")
                            tcp_connection.send(bytes(twt + '\n','utf-8'))
                        except:
                            e = sys.exc_info()[0]
                            print("Error: ", e)
                    content = []
                    time.sleep(1)
    

TCP_IP = "localhost"
TCP_PORT = 9009
conn = None
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
print("Waiting for TCP connection...")
conn, addr = s.accept()
print("Connected... Starting getting tweets.")
resp = get_tweets(conn)



# def send_tweets_to_spark(http_resp, tcp_connection):
#     # for line in http_resp.iter_lines():
    # try:
    #     # full_tweet = json.loads(line)
    #     # tweet_text = full_tweet['data']['text']# pyspark can't accept stream, add '\n'
    #     print("Tweet Text: " + tweet_text)
    #     print ("------------------------------------------")
    #     tcp_connection.send(bytes(tweet_text + '\n','utf-8'))
    # except:
    #     e = sys.exc_info()[0]
    #     #print("Error: %s" % e)
    #     print("Error: is here" )