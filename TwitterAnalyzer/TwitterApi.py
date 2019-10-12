import requests
import json
import twitter


class TwitterApi(twitter.Api):
    def __init__(self, autologin=True):
        self._overrider(False)
        twitter.Api.__init__(self)
        self.logged_in = False
        self.api = None
        self.following = None
        self.me = None

        if autologin:
            self._login_procedure()

    def _get_following(self):
        return self.api.GetFollowersPaged()[2]  # index 0,1 are empty

    def _login_procedure(self):
        self.logged_in, self.api = self._autologin_from_file()
        if self.logged_in:
            self.me = self.api.VerifyCredentials()
            print('Logged in succesfuly as {}.'.format(self.me['screen_name']))

    def _autologin_from_file(self):
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

class TwitterLoginFailed(Exception):
    """Base class for Twitter errors"""

    @property
    def message(self):
        '''Returns the first argument used to construct this error.'''
        return self.args[0]

if __name__ == "__main__":
    app = TwitterApi()
