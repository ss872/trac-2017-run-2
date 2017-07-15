import requests
import json
import os


def push_tweet(profile_id, tweet_id, client_id):
    # url = 'http://54.164.151.19/tweet/{}/{}/{}'.format(profile_id, tweet_id, client_id)
    # headers = {'Content-type': 'application/json'}
    # response = requests.post(url, headers=headers)
    response = None

    if response.status_code == 204:
        print
        profile_id + " posted"
        return True
    else:
        return False


if __name__ == '__main__':
    push_tweet('MB226', '738418531520352258', 'Eqnn7Hu7bSyd')
