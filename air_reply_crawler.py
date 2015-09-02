import json

import requests


__author__ = 'taisho6339'

from twitter import *

from config import *


def open_connect_twitter_stream():
    auth = OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    twitter_stream = TwitterStream(auth=auth, domain="userstream.twitter.com")
    return twitter_stream


def has_define_words_in_tweet(tweet):
    for word in EXTRACT_WORDS:
        if word in tweet:
            return True
    return False


def post_to_slack(user, tweet):
    name = user['name']
    scree_name = user['screen_name']

    headers = {'content-type': 'application/json'}

    title = "[" + name + '(@' + scree_name + ') さんからエアリプが飛んでいます' + "]"
    message = "発信時刻:" + tweet['created_at'] + '\n' + "```" + tweet['text'] + "```"
    data = {"text": title + "\n\n" + message + "\n\n"}

    requests.post(POST_SLACK_URL, data=json.dumps(data), headers=headers)


def stream_timeline():
    user_stream = open_connect_twitter_stream()
    for tweet in user_stream.user():
        if 'text' not in tweet or 'user' not in tweet:
            continue

        if not has_define_words_in_tweet(tweet['text']):
            continue

        user = tweet['user']
        post_to_slack(user, tweet)


if __name__ == "__main__":
    stream_timeline()
