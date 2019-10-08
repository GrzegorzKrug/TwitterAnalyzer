# TwitterAnalyzer.py
# Grzegorz Krug
import twitter
import json
from LibOverrider import overrider

overrider()  # Override and show what was overrided


class TwitterAnalyzer:
    def __init__(self, autologin=True):
        self._loged_in = False
        self.api = None
        self.following = None

        if autologin:
            self._loged_in, self.api = self._login_from_file()

            if self._loged_in:
                user_data = self.api.VerifyCredentials()
                print('Logged in as {}'.format(user_data['screen_name']))

                self.following = self._get_following()

        for user in self.following:
            print("Currently following: {}".format(user['screen_name']))

    def _get_following(self):
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


if __name__ == "__main__":
    app = TwitterAnalyzer()
            



