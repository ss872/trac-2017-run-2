import json
import re
from nltk.stem import WordNetLemmatizer


def clean_tweet_data(text):
    ree = re.sub(r'#', " ", text)
    ree = re.sub(r' us ', "", ree)
    ree = ree.lower()
    ree = re.sub(r'@', " ", ree)
    ree = re.sub(r'-', " ", ree)
    ree = re.sub(r"(?:\@|https?\://)\S+", "", ree)
    # ree = re.sub(r'https\S+',' ', ree)
    ree = re.sub(r'[^a-zA-Z]', ' ', ree)
    ree = re.sub(r' +', ' ', ree)
    return ree


#	print ree.encode('utf-8')

def do_lemmatize(sentence):
    wnl = WordNetLemmatizer()
    line = sentence.split()
    w = []
    for word in line:
        w.append(wnl.lemmatize(word))

    s = ' '.join(w)
    return s


def filter_tweet(tweet):
    data = json.loads(tweet)

    t_id = data['id']
    text = data['text']
    text = clean_tweet_data(text)
    text = do_lemmatize(text)
    timestamp = data['timestamp_ms']
    expanded_url = clean_url(data["entities"]["urls"], data)
    if data.get('retweeted_status'):
        retweeted = True
    else:
        retweeted = False
    fav_count = data['favorite_count']
    user_followers = data['user']['followers_count']
    if retweeted == True:
        return None
    else:
        text_2_word = text.split()

        if len(text_2_word) > 4:
            response = {'id': t_id, 'text': text, 'timestamp_ms': timestamp, 'retweeted': retweeted,
                        'fav_count': fav_count, 'user_followers': user_followers, 'expanded_url': expanded_url}
            return response
        else:
            return None


def clean_url(url, data):
    string = "NULL"
    if url == []:
        return string
    else:
        return data["entities"]["urls"][0]["expanded_url"]