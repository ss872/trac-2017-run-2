import data_cleaning_filtering as dc
import json
import requests
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup

profile_path = "expand.txt"
bhav_path = 'expand_bhavya.txt'

bhav_file = open(bhav_path, 'r')
bhav_profiles = []
for line in bhav_file:
    line=line.strip()
    line = dc.clean_tweet_data(line)
    line = dc.do_lemmatize(line)
    bhav_profiles.append(line)
#print bhav_profiles

profile_id_path = "tid.txt"
profile_ids = open(profile_id_path, 'r')
l = []
for line in profile_ids:
    id = line.strip().split()
    l += id
# print l

threshold_path = "Threshold.txt"
all_threshold = open(threshold_path, 'r')
threshold = []
for line in all_threshold:
    y = line.strip().split()
    threshold += y


# print threshold

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
        url_cont = Url_Crawler(url)
        url_cont = dc.clean_tweet_data(url_cont)
        url_cont = dc.do_lemmatize(url_cont)
        url_cont = word_tokenize(url_cont)
        url_cont = [w for w in url_cont if not w in stop_words]
        url_cont = no_repeat(url_cont)
        #print url_cont
    profile_file = open(profile_path, "r")
    #i = 1
    j = 0
    for line in profile_file:
        line = dc.clean_tweet_data(line)
        line = dc.do_lemmatize(line)
        #file_name = "/home/sandip/PycharmProjects/Profile_Rank/" + str(i) + "_Profile_Rank.txt"
        rank1 = 3*(ranking(text, line))
        #print "expand txt      :"+ str(rank1)
        rank1 += ranking(text,bhav_profiles[j])
        print "bhav_profile txt:"+ str(rank1)
        rank2 = ranking(url_cont, line)
        #print "expand url      :" + str(rank2)
        rank2 += ranking(url_cont, bhav_profiles[j])
        print "bhav_profile url:" + str(rank2)
        rank = rank1 + rank2
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
            # final_file_writer(temp, l[j])
        j += 1
        # file_writer(temp, l[j])
        # file = open(file_name, "a")
        # file.write("\n")
        # file.write(json.dumps(temp))
        # file.close()
        #i += 1
        # print "total rank", rank
        # print "Url rank", rank2
        # print rank + rank2
        # print "======================"
        # print profile_file
    return result

def ranking(text, profile):
    rank = 0
    profile_words = profile.split()
    for tword in text:
        # print word
        for pword in profile_words:
            if tword == pword:
                rank += 1
                # print tword + pword
                # print rank
                # print word
    return rank


def Url_Crawler(url):
    abc = ""
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


def no_repeat(tweet):
    dict_data = set(tweet)
    list_data = list(dict_data)
    return list_data


def file_writer(tweets, l):
    path = "code_files/" + str(l) + ".txt"
    z = open(path, 'a')
    z.write(str(l) + " ")
    z.write(str(tweets['id']) + " ")
    z.write(str(tweets['rank']) + " ")
    z.write(str(tweets['text']) + "\n")
    z.close()


def final_file_writer(tweets, l):
    #print "i was here"
    path = "filtered_tweets/" + str(l) + ".txt"
    z = open(path, 'a')
    z.write(str(l) + " ")
    z.write(str(tweets['id']) + " ")
    z.write(str(tweets['rank']) + " ")
    z.write(str(tweets['text']) + "\n")
    z.close()


def threshold_check(temp, threshold):
    rank = temp['rank']
    if rank >= int(threshold):
        return True
    else:
        return False
