from gather_data import *

access_token = "1456511107-LSRlg2Cemxq5pxtip1ZqXEjGVztC7qbGtbLgXe9"
access_token_secret = "sstwXdOd3ErHyQPsIvd1Ek0JsLvPOtCZOLQXSWP8FLNBv"
consumer_key = "cSX57JqiOvEh6m8RpaeI4fpbW"
consumer_secret = "zutTaUvx4KbLESEInyNX8vC6tydPV58joq1WIGGgWxYzHHChgw"


def start_tweets_api():
    listener = TweetListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, listener)
    print stream
    while True:
        try:
            stream.sample(languages=['en'])

        except Exception as ex:
            print str(ex)


if __name__ == "__main__":
    start_tweets_api()