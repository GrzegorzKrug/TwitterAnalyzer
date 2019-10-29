# TwitterApi.py
# Grzegorz Krug
import requests
from requests_oauthlib import OAuth1
import json
import os


class TwitterApi:
    def __init__(self, autologin=True):
        # self._overrider(False)
        self.apiUrl = r'https://api.twitter.com/1.1/'
        self.logged_in = False
        self.auth = None

        self.following = None
        self.me = None

        if autologin:
            valid, text = self._login_procedure()
            print(text)

    def _login_procedure(self):
        valid, self.me, message = self._verifyOAuth()
        if valid:
            self.logged_in = True
        return valid, message

    def _verifyOAuth(self):
        try:
            file_path = os.path.dirname(__file__) + '\\' + 'secret_token.txt'

            with open(file_path, 'rt') as token_file:
                data = json.load(token_file)
                consumer_key = data['consumer_key']
                consumer_secret = data['consumer_secret']
                access_token_key = data['access_token_key']
                access_token_secret = data['access_token_secret']

                url = self.apiUrl + r'/account/verify_credentials.json'

                auth = OAuth1(consumer_key,
                              consumer_secret,
                              access_token_key,
                              access_token_secret)
                response = requests.get(url, auth=auth)
                try:
                    self.verify_response(response.status_code)
                    self.auth = auth
                    me = response.json()
                    return True, me, f'Logged in successfully as {me["screen_name"]}'
                except Unauthorized:
                    return False, None, 'Authorization failed! Invalid or expired token.'

        except json.decoder.JSONDecodeError:
            print("Exception: secret_token.txt is not in json format!")
            return False, None, "secret_token.txt is not in json format!"

        except KeyError:
            print("Exception: secret_token.txt is missing some keys!")
            return False, None, "secret_token.txt is missing some keys!"

        except FileNotFoundError:
            print("Exception: secret_token.txt is missing!")
            return False, None, "secret_token.txt is missing!"
        #
        # except twitter.error.TwitterError:
        #     print("Invalid or expired token!")
        #     return False, api, "Invalid or expired token!"
        #
        # return True, api, message

    def collectHomeLine(self, chunk_size=200):
        if not self.logged_in:
            raise Unauthorized('Authentication not verified!')
        if chunk_size < 0:
            chunk_size = 1
        elif chunk_size > 200:
            chunk_size = 200

        params = {'count': chunk_size}
        fullUrl = self.apiUrl + r'/statuses/home_timeline.json'
        valid, data = self.make_request(fullUrl, params=params)
        return data

    def make_request(self, fullUrl, params=None, header=None):
        if params is None:
            params = {}
            
        params.update({'tweet_mode':'extended'})
        response = requests.get(fullUrl, headers=header, params=params, auth=self.auth)
        
        if self.verify_response(response.status_code):
            return True, response.json()
        else:
            return False, None

    def request_status(self, statusID):        
        fullUrl = self.apiUrl + r'/statuses/show.json'
        params={'id':statusID}
        valid, data = self.make_request(fullUrl, params=params)    
        return data
        
    @staticmethod
    def verify_response(resp_code):
        if resp_code == 200:
            return True
        # if resp_code == 400:
        #     pass
        elif resp_code == 401:
            raise Unauthorized('No access to this request')
        # elif resp_code == 402:
        #     pass
        elif resp_code == 404:
            raise ApiNotFound('Error 404')
        elif resp_code == 429:
            raise  TooManyRequests('Error 429, too many requests.')
        else:
            raise Exception(f'Error, Response code {resp_code}')

    # def CollectHome(self, count=200):
    #     try:
    #         home = self.api.GetHomeTimeline(count=count)
    #         return home
    #
    #     except AttributeError:
    #         raise TwitterLoginFailed("Error! Login status: {}".format(self.logged_in))

    # @staticmethod
    # def _overrider(display=True):
    #     text = []
    #
    #     def add_items_method(self):
    #         return self.__dict__.items()
    #
    #     def __getitem__(cls, x, missing=None):
    #         return getattr(cls, x, missing)
    #
    #     # @classmethod
    #     # def __getitem_class__(cls, x):
    #     #     return getattr(cls, x)
    #
    #     twitter.User.items = add_items_method
    #     text += ["New Method twitter.User.items"]
    #
    #     twitter.User.__getitem__ = __getitem__
    #     text += ["User is subscriptable twitter.User.__getitem__"]
    #
    #     twitter.Status.items = add_items_method
    #     text += ["New Method twitter.Status.items"]
    #
    #     twitter.Status.__getitem__ = __getitem__
    #     text += ["Status is subscriptable twitter.Status.__getitem__"]
    #
    #     twitter.Status.get = __getitem__
    #     text += ["New Method twitter.Status.get"]
    #
    #     if display:
    #         for comment in text:
    #             print('\t', comment)
    #         print('#' * 20, 'End of overloading.', '#' * 20, '\n')


class Unauthorized(Exception):  # 401
    """Base class for Twitter errors"""
    @property
    def message(self):
        '''Returns the first argument used to construct this error.'''
        return self.args[0]


class ApiNotFound(Exception):  # 404
    """Base class for Twitter errors"""
    @property
    def message(self):
        '''Returns the first argument used to construct this error.'''
        return self.args[0]


class TooManyRequests(Exception):  # 429
    """Base class for Twitter errors"""
    @property
    def message(self):
        '''Returns the first argument used to construct this error.'''
        return self.args[0]


if __name__ == "__main__":
    app = TwitterApi()
    r = app.collectHomeLine()
    app.request_status(1188957411794653186)
    
