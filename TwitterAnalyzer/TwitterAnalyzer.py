# TwitterAnalyzer.py
# Grzegorz Krug
import twitter
import json
from time import time
from LibOverrider import overrider
import os
import pandas as pd
# from TwitterApi import TwitterApi

overrider()  # Override and show what was overrided


class TwitterAnalyzer:
    def __init__(self, autologin=True):
        self._loged_in = False
        self.api = None
        self.following = None
        self._data_dir = 'tweets'
        os.makedirs(self._data_dir, exist_ok=True)  # Create folder for files

        if autologin:
            self._loged_in, self.api = self._login_from_file()

            if self._loged_in:
                user_data = self.api.VerifyCredentials()
                print('Logged in as {}'.format(user_data['screen_name']))

                self.following = self._get_following()

        # for user in self.following:
        #     print("Currently following: {}".format(user['screen_name']))

    def _get_following(self):
        print(self.api.base_url)
        return self.api.GetFollowersPaged()[2]  # index 0,1 are empty

    def _login_from_file(self):
        with open('secret_token.txt', 'rt') as token_file:
        
            try:
                data = json.load(token_file)
                consumer_key = data['consumer_key'] 
                consumer_secret = data['consumer_secret']
                access_token_key = data['access_token_key']
                access_token_secret = data['access_token_secret']

                api = twitter.Api(consumer_key=consumer_key,
                              consumer_secret=consumer_secret,
                              access_token_key=access_token_key,
                              access_token_secret=access_token_secret)
                api.VerifyCredentials()
                
            except json.decoder.JSONDecodeError as e:
                print("secret_token.txt is not in json format!")
                return False
            
            except KeyError as e:
                print("secret_token.txt is missing some keys!")
                return False
            
            except FileNotFoundError:
                print("secret_token.txt is missing!")
                return False
            
            except twitter.error.TwitterError:
                print("Invalid or expired token!")
                return False

        return True, api

    def CollectHome(self, count=200):
        home = self.api.GetHomeTimeline(count=count)
        return home

    def export_tweet_to_database(self, tweet, filename='last_data'):
        head = ['id', 'timestamp', 'contributors', 'coordinates', 'created_at',
                'current_user_retweet', 'favorite_count', 'favorited', 'full_text', 'geo',
                'hashtags', 'id_str', 'in_reply_to_screen_name', 'in_reply_to_status_id',
                'in_reply_to_user_id', 'lang', 'location', 'media', 'place', 'possibly_sensitive',
                'quoted_status', 'quoted_status_id', 'quoted_status_id_str', 'retweet_count',
                'retweeted', 'retweeted_status', 'scopes', 'source', 'text', 'truncated', 'urls',
                'user', 'user_mentions', 'withheld_copyright', 'withheld_in_countries',
                'withheld_scope', 'tweet_mode']

        # df = pd.DataFrame.from_dict(tweet)

        with open(self._data_dir + '\\' + filename + '.csv', 'at') as file:
            for key in head:
                file.write(str(tweet.get(key, 'n/a')))
                file.write(';')
            file.write('\n')

    def add_timestamp(self, tweet):
        try:
            setattr(tweet, 'timestamp', round(time()))

        except AttributeError:
            tweet['timestamp'] = round(time())

    @staticmethod
    def tweet_strip(tweet):
        def add_data(query, new_query=None):
            if new_query == None:
                new_query = query

            out[new_query] = tweet[query]

        out = {}

        add_data('text')
        add_data('lang')
        add_data('created_at')

        add_data('id')
        add_data('user')
        add_data('urls')

        add_data('user_mentions')
        add_data('hashtags')
        add_data('media')

        add_data('retweet_count')
        add_data('favorite_count')
        # add_data comments  # <-- ??

        add_data('in_reply_to_screen_name')
        add_data('in_reply_to_status_id')
        add_data('in_reply_to_user_id')
        add_data('quoted_status')
        add_data('quoted_status_id', 'quoted_status_id')

        return out


if __name__ == "__main__":
    app = TwitterAnalyzer()
    home_twetts = app.CollectHome(10)
    for i, tweet in enumerate(home_twetts):
        stripped_tweet = app.tweet_strip(tweet)
        # print(tweet)
        app.add_timestamp(stripped_tweet)
        app.export_tweet_to_database(stripped_tweet)


        # for s in tweet.items():
        #     if s[0] == 'param_defaults' or s[0] == '_json':
        #         continue
        #     print('\t', s)







