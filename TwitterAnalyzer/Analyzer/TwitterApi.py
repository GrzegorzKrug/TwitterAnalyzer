# TwitterApi.py
# Grzegorz Krug
import requests
from requests_oauthlib import OAuth1
import json
import twitter
import os


class TwitterApi:
    def __init__(self, autologin=True):
        self._overrider(False)
        self.logged_in = False
        self.apiUrl = r'https://api.twitter.com/1.1/'
        self.following = None
        self.me = None
        self._verifyOAuth()
        if autologin:
            valid, text = self._verifyOAuth()
            print(text)
            if valid:
                self.logged_in = True
            # self.request_me()

    def _login_procedure(self):
        self.logged_in, self.api, message = self._autologin_from_file()
        if self.logged_in:
            self.me = self.api.VerifyCredentials()
            text = 'Logged in succesfuly as {}.'.format(self.me['screen_name'])
            return True, text
        else:
            return False, message

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
                ressponse = requests.get(url, auth=auth)
                try:
                    self.verify_response(ressponse.status_code)
                    message = 'Logged in succesfuly'
                    return True, message
                except Unauthorized:
                    return False, 'Authorization failed! Invalid or expired token.'

        except json.decoder.JSONDecodeError:
            print("secret_token.txt is not in json format!")
            return False, "secret_token.txt is not in json format!"

        except KeyError:
            print("secret_token.txt is missing some keys!")
            return False, "secret_token.txt is missing some keys!"

        except FileNotFoundError:
            print("secret_token.txt is missing!")
            return False, "secret_token.txt is missing!"
        #
        # except twitter.error.TwitterError:
        #     print("Invalid or expired token!")
        #     return False, api, "Invalid or expired token!"
        #
        # return True, api, message

    def verify_response(self, resp_code):
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
            raise  TooManyRequests('Error 429')
        else:
            raise Exception(f'Error, Response code {resp_code}')

    def CollectHome(self, count=200):
        try:
            home = self.api.GetHomeTimeline(count=count)
            return home

        except AttributeError:
            raise TwitterLoginFailed("Error! Login status: {}".format(self.logged_in))

    @staticmethod
    def _overrider(display=True):
        text = []

        def add_items_method(self):
            return self.__dict__.items()

        def __getitem__(cls, x, missing=None):
            return getattr(cls, x, missing)

        # @classmethod
        # def __getitem_class__(cls, x):
        #     return getattr(cls, x)

        twitter.User.items = add_items_method
        text += ["New Method twitter.User.items"]

        twitter.User.__getitem__ = __getitem__
        text += ["User is subscriptable twitter.User.__getitem__"]

        twitter.Status.items = add_items_method
        text += ["New Method twitter.Status.items"]

        twitter.Status.__getitem__ = __getitem__
        text += ["Status is subscriptable twitter.Status.__getitem__"]

        twitter.Status.get = __getitem__
        text += ["New Method twitter.Status.get"]

        if display:
            for comment in text:
                print('\t', comment)
            print('#' * 20, 'End of overloading.', '#' * 20, '\n')


class TooManyRequests(Exception):  # 429
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

class Unauthorized(Exception):  # 401
    """Base class for Twitter errors"""
    @property
    def message(self):
        '''Returns the first argument used to construct this error.'''
        return self.args[0]


if __name__ == "__main__":
    app = TwitterApi()
