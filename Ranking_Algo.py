import data_cleaning_filtering as dc
import json
import requests
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
import multiprocessing

profile_path = "expand.txt"

profile_id_path = "tid.txt"
profile_ids = open(profile_id_path, 'r')
l = []
for line in profile_ids:
    id = line.strip().split()
    l += id

threshold_path = "Threshold.txt"
all_threshold = open(threshold_path, 'r')
threshold = []
for line in all_threshold:
    y = line.strip().split()
    threshold += y


def Ranking_algo(tweet_demo):

    result = []
    stop_words = set(stopwords.words('english'))
    text = tweet_demo['text']
    text = text.split()
    text = no_repeat(text)
    url = tweet_demo['expanded_url']
    if url == "NULL":
        url_cont = ""
    else:
        print "point A"
        t = multiprocessing.Process(target=Url_Crawler, args=(url,))
        t.start()
        t.join(15)
        if t.is_alive():
            print "process is terminated"
            t.terminate()
            t.join()
        print "point B"
        url_cont = temp_reader()
        url_cont = dc.clean_tweet_data(url_cont)
        url_cont = dc.do_lemmatize(url_cont)
        url_cont = word_tokenize(url_cont)
        url_cont = [w for w in url_cont if not w in stop_words]
        url_cont = no_repeat(url_cont)
    profile_file = open(profile_path, "r")
    j = 0
    for line in profile_file:
        line = dc.clean_tweet_data(line)
        line = dc.do_lemmatize(line)
        rank1 = 3*(ranking(text, line))
        rank2 = 2*(ranking(url_cont, line))
        rank = rank1 + rank2 + 1
        temp = tweet_demo
        temp['rank'] = rank
        flag = threshold_check(temp, threshold[j])
        if flag:
            result_profile = {}
            result_profile['push_tweet'] = True
            result_profile['tweet_id'] = temp['id']
            result_profile['profile_id'] = l[j]
            result_profile['tweet_score'] = temp['rank']
            result_profile['text'] = temp['text']
            result.append(result_profile)
        j += 1
    return result

def ranking(text, profile):
    rank = 0
    profile_words = profile.split()
    for tword in text:
        for pword in profile_words:
            if tword == pword:
                rank += 1
    return rank


def Url_Crawler(url):
    abc = " "
    source_code = requests.get(url)
    plain_source = source_code.text
    soup = BeautifulSoup(plain_source, "html.parser")
    title = soup.find('title')
    try:
        abc = title.text
    except:
        pass
    paragraph = soup.find_all('p')
    for tag in paragraph:
        try:
            abc += tag.text
        except:
            pass
    temp_writer(abc)


def no_repeat(tweet):
    dict_data = set(tweet)
    list_data = list(dict_data)
    return list_data


def temp_writer(cont):
    path = "temp.text"
    z = open(path, 'w')
    z.write(json.dumps(cont))
    z.close()

def temp_reader():
    path = "temp.text"
    cont = ""
    z = open(path, 'r')
    for line in z:
        cont += line
    z.close()
    return cont


def threshold_check(temp, threshold):
    rank = temp['rank']
    if rank >= int(threshold):
        return True
    else:
        return False
