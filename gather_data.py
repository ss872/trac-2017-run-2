from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import logging
import logging.handlers
import json
import schedule
import data_cleaning_filtering as dcf
from utils import push_tweet
import Ranking_Algo as ra

CLIENT_ID = "DCIRfK2Kxel3"

class TweetListener(StreamListener):
    def __init__(self, api=None):
        super(TweetListener, self).__init__(api)

        self.logger = logging.getLogger('tweetlogger')

        statusHandler = logging.handlers.TimedRotatingFileHandler('status.log', when='H', encoding='bz2', utc=True)
        statusHandler.setLevel(logging.INFO)
        self.logger.addHandler(statusHandler)

        warningHandler = logging.handlers.TimedRotatingFileHandler('warning.log', when='H', encoding='bz2', utc=True)
        warningHandler.setLevel(logging.WARN)
        self.logger.addHandler(warningHandler)
        logging.captureWarnings(True)

        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel(logging.WARN)
        self.logger.addHandler(consoleHandler)

        self.logger.setLevel(logging.INFO)

        # variables to use
        self.profiles_text = ""

        profile_file = "expand.txt"
        self.set_profile_text(profile_file)

        self.pushed_tweets_count = {}

    def set_profile_text(self, profile_file):
        with open(profile_file, 'r') as fin:
            self.profiles_text = fin.read()

    def on_error(self, exception):
        self.logger.warn(str(exception))

    def on_data(self, data):
        # print data
        clean_tweet = dcf.filter_tweet(data)
        # print clean_tweet

        # if clean_tweet and not self.text_in_profile(clean_tweet['text']):
        #     return True
        if not clean_tweet:
            return True
        # ra.Ranking_algo(clean_tweet)
        results = ra.Ranking_algo(clean_tweet)

        ########## Algo #########
        #	result = algoxyz(clean_tweet)
        # output of algoxyz should be like below
        # result = [{
        #     'push_tweet': True,
        #     'tweet_id': 123456789,
        #     'profile_id': "MB101",
        #     'tweet_score': 5,
        #     'text': "this is tweet text",
        # },
        # {
        #     'push_tweet': True,
        #     'tweet_id': 123456789,
        #     'profile_id': "MB101",
        # }
        # ]
        ######### End Algo ##########

        print "results is ", results

        for result in results:
                push_tweet(result["profile_id"], result["tweet_id"], CLIENT_ID, result["tweet_score"], result["text"])

        return True

    # def can_push(self, profile_id):
    #     push_count = self.pushed_tweets_count.get(profile_id)
    #     if push_count:
    #         print 'push count is ', push_count, "profile id is", profile_id
    #         if push_count <= 10:
    #             return True
    #         else:
    #             return False
    #     else:
    #         self.pushed_tweets_count[profile_id] = 1
    #         return True

    def text_in_profile(self, text):
        for word in text.split():
            if word in self.profiles_text:
                return True
        return False

    def reset_count(self):
        self.pushed_tweets_count = {}
