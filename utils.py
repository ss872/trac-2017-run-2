import requests
import datetime
from peewee import *

db = MySQLDatabase("trac", host="localhost", port=3306, user="root", passwd="root")


class PushProfiles(Model):
    profile = CharField()
    tweet = CharField()
    score = CharField()
    text = CharField()
    time = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db  # This model uses the "people.db" database.


def push_tweet(profile_id, tweet_id, client_id, tweet_score, tweet_text):
    url = 'http://scspc654.cs.uwaterloo.ca/tweet/{0}/{1}/{2}'.format(profile_id, tweet_id, client_id)
    print "url is ", url
    headers = {'Content-type': 'application/json'}
    response = requests.post(url, headers=headers)

    if response.status_code == 204:
        PushProfiles.create(profile=profile_id, tweet=tweet_id, score=tweet_score, text=tweet_text)
        print profile_id + " posted"
    else:
        print "Tweet was unable to push as we get response code :", response.status_code


if __name__ == '__main__':
    # push_tweet('MB226', '738418531520352258', 'Eqnn7Hu7bSyd')
    db.connect()
    db.create_tables([PushProfiles])
    pass
