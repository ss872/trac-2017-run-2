from gather_data import *
import multiprocessing
import time
# access_token = "1456511107-LSRlg2Cemxq5pxtip1ZqXEjGVztC7qbGtbLgXe9"
# access_token_secret = "sstwXdOd3ErHyQPsIvd1Ek0JsLvPOtCZOLQXSWP8FLNBv"
# consumer_key = "cSX57JqiOvEh6m8RpaeI4fpbW"
# consumer_secret = "zutTaUvx4KbLESEInyNX8vC6tydPV58joq1WIGGgWxYzHHChgw"

# consumer_key = "ZN3oupo3WzZmIcvNSGXdK4yea"
# consumer_secret = "wZwscKyJc60xizrSSWNKRhRrllRLYyv7RpKWKVsCiPHfuGghAp"
# access_token = "873881805119672322-MyeCpCteUIUzjKmHGBB5ZPcbp8mMVqZ"
# access_token_secret = "PatrEqAWDPDe53PnLJEuvMsqQ7fycI76SppkKnJQcuajM"


access_token = "873881805119672322-kwWJeoffxEAiWNbwMnqOpP9uODLCr6T"
access_token_secret = "mw7O66clhLADSgWfJeud22rBSYLN5tfcSfXrpivJcfkCq"
consumer_key = "as1VRfqFjInsrx6uSuweettWy"
consumer_secret = "UK60ZYwV89zoP9ajknnhGrN7eYhOWPzGS2NeGXUP9SJNPt7r46"


def start_tweets_api():
    listener = TweetListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, listener)
    print stream
    while True:
        try:
            p = multiprocessing.Process(target=multi,name="multi")
            p.start()
            p.join(120)
            if p.is_alive():
                print "lets terminate"
                p.terminate()
                p.join()
            #stream.sample(languages=['en'])

        except Exception as ex:
            print str(ex)
def multi():
    stream.sample(languages=['en'])

if __name__ == "__main__":
    listener = TweetListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, listener)
    start_tweets_api()
