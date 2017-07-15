import data_cleaning_filtering as dc
import json
import requests
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup

tweet_demo = {'expanded_url': u'https://plato.stanford.edu/entries/reasons-agent/', 'user_followers': 1976,
              'text': u'reason hershey for action agent neutral v agent relative philosophyjournals book review article entry feedly',
              'retweeted': False, 'timestamp_ms': u'1499846738663', 'id': 885047485818974208, 'fav_count': 0}
profile_path = "/home/shyamal/PycharmProjects/Trac 2017/expand.txt"

profile_id_path = "/home/shyamal/PycharmProjects/Trac 2017/tid.txt"
profile_ids = open(profile_id_path, 'r')
l = []
for line in profile_ids:
    id = line.strip().split()
    l += id

threshold_path = "/home/shyamal/PycharmProjects/Trac 2017/Threshold.txt"
all_threshold = open(threshold_path, 'r')
threshold = []
for line in all_threshold:
    y = line.strip().split()
    threshold += y
print
threshold


def Ranking_algo(tweet_demo):
    stop_words = set(stopwords.words('english'))
    text = tweet_demo['text']
    text = text.split()
    url = tweet_demo['expanded_url']
    if url == "NULL":
        tot_data = no_repeat(text, [])
    else:
        url_cont = Url_Crawler(url)
        url_cont = dc.clean_tweet_data(url_cont)
        url_cont = dc.do_lemmatize(url_cont)
        url_cont = word_tokenize(url_cont)
        url_cont = [w for w in url_cont if not w in stop_words]
        tot_data = no_repeat(text, url_cont)
        print
        url_cont
    profile_file = open(profile_path, "r")
    i = 1
    j = 0
    for line in profile_file:
        line = dc.clean_tweet_data(line)
        line = dc.do_lemmatize(line)
        file_name = "/home/shyamal/PycharmProjects/Profile_Rank/" + str(i) + "_Profile_Rank.txt"
        rank = ranking(tot_data, line)
        # rank2 = ranking(url_cont, line)
        temp = tweet_demo
        temp['rank'] = rank
        flag = threshold_check(temp, threshold[j])
        if flag:
            final_file_writer(temp, l[j])
        file_writer(temp, l[j])
        file = open(file_name, "a")
        file.write("\n")
        file.write(json.dumps(temp))
        file.close()
        i += 1
        j += 1
        print
        "total rank", rank
        # print "Url rank", rank2
        # print rank + rank2
        print
        "======================"
        # print profile_file


def ranking(text, profile):
    rank = 0
    profile_words = profile.split()
    for tword in text:
        # print word
        for pword in profile_words:
            if tword == pword:
                rank += 1
                print
                tword + pword
                # print rank
                # print word
    return rank


def Url_Crawler(url):
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
    return abc


def no_repeat(tweet, url):
    tot_data = tweet + url
    dict_data = set(tot_data)
    list_data = list(dict_data)
    return list_data


def file_writer(tweets, l):
    path = "/home/shyamal/PycharmProjects/Trac 2017/code_files/" + str(l) + ".txt"
    z = open(path, 'a')
    z.write(str(l) + " ")
    z.write(str(tweets['id']) + " ")
    z.write(str(tweets['rank']) + " ")
    z.write(str(tweets['text']) + "\n")
    z.close()


def final_file_writer(tweets, l):
    path = "/home/shyamal/PycharmProjects/Trac 2017/filtered_tweets/" + str(l) + ".txt"
    z = open(path, 'a')
    z.write(str(l) + " ")
    z.write(str(tweets['id']) + " ")
    z.write(str(tweets['rank']) + " ")
    z.write(str(tweets['text']) + "\n")
    z.close()


def threshold_check(temp, threshold):
    rank = temp['rank']
    if rank >= threshold:
        return True
    else:
        return False
