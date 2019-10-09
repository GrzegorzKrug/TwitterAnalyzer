import requests
import json
import twitter

class TwitterApi(twitter.Api):
    def __init__(self, autologin=True):
        twitter.Api.__init__(self)

        self.logged_in = False
        if autologin:
            self.logged_in = self._login_from_file()
            if self.logged_in:
                print("Logged in succesfuly!")

    def _login_from_file(self):
        with open('secret_token.txt', 'rt') as token_file:

            try:
                data = json.load(token_file)
                consumer_key = data['consumer_key']
                consumer_secret = data['consumer_secret']
                access_token_key = data['access_token_key']
                access_token_secret = data['access_token_secret']

                self.login_to_twitter(consumer_key=consumer_key,
                                  consumer_secret=consumer_secret,
                                  access_token_key=access_token_key,
                                  access_token_secret=access_token_secret)

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

        return True

    @staticmethod
    def login_to_twitter(consumer_key=None,
                         consumer_secret=None,
                         access_token_key=None,
                         access_token_secret=None):

        creditals = {'consumer_key':consumer_key,
                     'consumer_secret':consumer_secret,
                     'access_token_key':access_token_key,
                     'access_token_secret': access_token_secret}

        for key, value in creditals.items():
            if None == value:
                raise ValueError("Missing token = {}".format(key))



if __name__ == "__main__":
    app = TwitterApi()
