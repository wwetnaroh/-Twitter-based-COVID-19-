import socket
import sys
import os
import requests
import requests_oauthlib
import json

# Replace the values below with yours
# ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN'
# ACCESS_SECRET = 'YOUR_ACCESS_SECRET'
# CONSUMER_KEY = 'YOUR_CONSUMER_KEY'
# CONSUMER_SECRET = 'YOUR_CONSUMER_SECRET'
# my_auth = requests_oauthlib.OAuth1(CONSUMER_KEY, CONSUMER_SECRET,ACCESS_TOKEN, ACCESS_SECRET)
bearer_token = os.environ.get("BEARER_TOKEN")

def send_tweets_to_spark(http_resp, tcp_connection):
    for line in http_resp.iter_lines():
        try:
            full_tweet = json.loads(line)
            tweet_text = full_tweet['data']['text']# pyspark can't accept stream, add '\n'
            print("Tweet Text: " + tweet_text)
            print ("------------------------------------------")
            tcp_connection.send(bytes(tweet_text + '\n','utf-8'))
        except:
            e = sys.exc_info()[0]
            #print("Error: %s" % e)
            print("Error: is here" )

def get_tweets():
    # url = 'https://stream.twitter.com/1.1/statuses/filter.json'
    #query_data = [('language', 'en'), ('locations', '-130,-20,100,50'),('track','#')]
    # query_data = [('locations', '-122.75,36.8,-121.75,37.8,-74,40,-73,41'), ('track', '#')] #this location value is San Francisco & NYC
    # query_url = url + '?' + '&'.join([str(t[0]) + '=' + str(t[1]) for t in query_data])
    # response = requests.get(query_url, auth=my_auth, stream=True)
    # print(query_url, response)
    

    rules = get_rules()
    delete = delete_all_rules(rules)
    set = set_rules(delete)
    response=get_stream(set)
    return response




# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'



def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer AAAAAAAAAAAAAAAAAAAAACE%2FbgEAAAAAN1L%2BY1kZ8BiVVr392iitgBVpkWM%3DeJO2PBFACse5wDS3X7l341BHay3z2408YISmAQy1XkMRMxJ4pb"
    r.headers["User-Agent"] = "v2FilteredStreamPython"
    return r


def get_rules():
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", auth=bearer_oauth
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    #print(json.dumps(response.json()))
    return response.json()


def delete_all_rules(rules):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    #print(json.dumps(response.json()))


def set_rules(delete):
    # You can adjust the rules if needed
    sample_rules = [
        {"value": "COVID-19"},
    ]
    payload = {"add": sample_rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    #print(json.dumps(response.json()))


def get_stream(set):
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream?tweet.fields=geo", auth=bearer_oauth, stream=True,
    )
    #print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    # for response_line in response.iter_lines():
    #     if response_line:
    #         json_response = json.loads(response_line)
    #         #print(json.dumps(json_response, indent=4, sort_keys=True))
    print("I am ready to return response")
    return response



TCP_IP = "localhost"
TCP_PORT = 9009
conn = None
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
print("Waiting for TCP connection...")
conn, addr = s.accept()
print("Connected... Starting getting tweets.")
resp = get_tweets()
send_tweets_to_spark(resp,conn)



