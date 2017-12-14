# SI506 Final Project
# Option 1:Facebook & iTunes
# Sangho Eum, sanghoe@umich.edu

import json
import webbrowser
import csv
import requests
from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import facebook_compliance_fix
from your_app_data import APP_ID, APP_SECRET


#############FACEBOOK###########################
# Set the Global facebook_session varible for FB access below
facebook_session = False

# Creating Cache for facebook
CACHE_FNAME = "facebook_cache.json"

try:
    f = open(CACHE_FNAME, "r")
    fstr = f.read()
    CACHE_DICTION = json.loads(fstr)
    f.close()
except:
    CACHE_DICTION = {}

# Define a function for a API request to Facebook with caching.
def params_unique_combination_fb(baseurl, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        res.append("{}={}".format(k, params[k]))
    return baseurl +"?" + "&".join(res)

def getFacebookPost(baseURL, params = {}):
    unique_ident = params_unique_combination_fb(baseURL, params)
    if unique_ident in CACHE_DICTION:
        print("getting cached data...")
        return CACHE_DICTION[unique_ident]
    else:
        global facebook_session
        if not facebook_session:
            authorization_base_url =  'https://www.facebook.com/dialog/oauth'
            token_url = 'https://graph.facebook.com/oauth/access_token'
            redirect_uri = 'https://www.programsinformationpeople.org/runestone/oauth'

            scope = ['user_posts','pages_messaging','user_managed_groups','user_status','user_likes']
            facebook = OAuth2Session(APP_ID, redirect_uri=redirect_uri, scope=scope)
            facebook_session = facebook_compliance_fix(facebook)

            authorization_url, state = facebook_session.authorization_url(authorization_base_url)
            print('Opening browser to {} for authorization'.format(authorization_url))
            webbrowser.open(authorization_url)

            redirect_response = input('Paste the full redirect URL here: ')
            facebook_session.fetch_token(token_url, client_secret=APP_SECRET, authorization_response=redirect_response.strip())

        facebook_resp = facebook_session.get(baseURL, params=params)
        facebook_text = facebook_resp.text
        CACHE_DICTION[unique_ident] = json.loads(facebook_text)
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close()
        print(facebook_text)
        return CACHE_DICTION[unique_ident]

# Set the base url and parameters for 30 posts and store 30 posts data to variable thirty_post
baseurl = 'https://graph.facebook.com/me/feed'
url_params = {}
url_params["fields"] = "message, likes, comments"
url_params["limit"] = 30
thirty_post = getFacebookPost(baseurl, params = url_params)

# make a stopwords_list
s = open('stopwords_list.txt', 'r')
stopwords_list=[]
for i in s.readlines()[0:174]:
    stopwords_list.append(i[0:-1])
s.close()

# Define a class Post
class Post():
    def __init__(self, post_dict={}):
        if 'message' in post_dict:
            self.message = post_dict['message']
        else:
            self.message = ''
        if 'comments' in post_dict:
            self.comments = post_dict['comments']['data']
            self.comments_cnt = len(post_dict['comments']['data'])
        else:
            self.comments = []
        if 'likes' in post_dict:
            self.likes = post_dict['likes']['data']
            self.likes_cnt = len(post_dict['likes']['data'])
        else:
            self.likes = []

# __str__ method
    def __str__(self):
        return "This post has {} comments and {} likes".format(self.comments_cnt, self.likes_cnt)

# Method returning a list of all the words
    def words_list(self):
        n = []
        for i in self.message.split():
            if i not in stopwords_list:
                n.append(i)
        return n

# Method returning ratio of non-stopword to total-words
    def words_ratio(self):
        n = []
        n_num=0
        for i in self.message.split():
            if i not in stopwords_list:
                n_num += 1
        t = []
        t_num=0
        for i in self.message.split():
            t_num += 1
        return n_num/t_num

# Create a list of class 30 Post
post_list = []
for i in thirty_post["data"]:
    post_list.append(Post(i))

thirty_post_dict ={}
for i in post_list:
    n = i.words_list()
    for l in n:
        if l not in thirty_post_dict.keys():
            thirty_post_dict[l] = 1
        else:
            thirty_post_dict[l] += 1

# Define function for finding the most common words except stopwords
def common_word(dict):
    max_v = max(dict.values())
    k=list(dict.keys())
    max_l = []
    for i in k:
        if dict[i] == max_v:
            max_l.append(i)
    return max_l

most_common_word = common_word(thirty_post_dict)


############################ iTunes##############################

# Creating Cache for iTunes
CACHE_FNAME_itunes = "itunes_cache.json"

try:
    f1 = open(CACHE_FNAME_itunes, "r")
    fstr1 = f1.read()
    CACHE_DICTION1 = json.loads(fstr1)
    f1.close()
except:
    CACHE_DICTION1 = {}


def params_unique_combination(baseurl, params_d, private_keys=["api_key"]):
    alphabetized_keys = sorted(params_d.keys())
    res = []
    for k in alphabetized_keys:
        if k not in private_keys:
            res.append("{}-{}".format(k, params_d[k]))
    return baseurl + "_".join(res)

def get_from_itunes(name, mtype="song"):
    baseurl = "https://itunes.apple.com/search"
    parameters = {}
    parameters["term"] = name
    parameters["entity"] = mtype
    itunes_unique = params_unique_combination(baseurl, parameters)
    if itunes_unique in CACHE_DICTION1:
        print("Loading a cached iTune API data")
        itunes_data = CACHE_DICTION1[itunes_unique]
    else:
        print("Making a request to iTunes API")
        itunes_resp = requests.get(baseurl, params = parameters)
        itunes_resp_data = itunes_resp.text
        itunes_data = json.loads(itunes_resp_data)
        CACHE_DICTION1[itunes_unique] = itunes_data
        cache_diction_json = json.dumps(CACHE_DICTION1)
        itunes_file = open(CACHE_FNAME_itunes, 'w')
        itunes_file.write(cache_diction_json)
        itunes_file.close()
    return itunes_data

# Define Song class

class Song(object):
    def __init__(self, itunes_dict):
        self.title = itunes_dict["trackName"]
        self.artist = itunes_dict["artistName"]
        self.track_duration = itunes_dict["trackTimeMillis"]
        self.album = itunes_dict["collectionName"]
        self.genre = itunes_dict["primaryGenreName"]
        self.track_url = itunes_dict["trackViewUrl"]

# __str__ method
    def __str__(self):
        return "This song is {} by artist: {} in {} Album.(Duration: {})".format(self.title, self.artist, self.album, self.track_duration)

    def track_length(self):
        return self.track_duration


# Create a list of instances of class Song using most common_word

itunes_data = get_from_itunes(most_common_word)
itunes_list = []

for i in itunes_data["results"]:
    itunes_list.append(Song(i))

# Sorted itunes_list by track_length
sorted_itunes = sorted(itunes_list, key =lambda x: x.track_length(), reverse= True)

# Define function creating CSV files
def write_csv(songs, file_name ="songs_list.csv"):
    output = open(file_name, "w")
    col_name = ["song_title", "artist", "length", "album" ,"genre"]
    transfer = csv.DictWriter(output, fieldnames = col_name, delimiter=",")
    transfer.writeheader()
    for i in songs:
        transfer.writerow({"song_title":i.title, "artist": i.artist, "length": i.track_duration, "album": i.album, "genre":  i.genre})
    output.close()

print(write_csv(itunes_list, "sangho.csv"))
