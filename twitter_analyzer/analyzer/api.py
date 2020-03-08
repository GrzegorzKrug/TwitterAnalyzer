# TwitterApi.py
# Grzegorz Krug

import requests
import json
import sys
import os

from requests_oauthlib import OAuth1, OAuth1Session


class TwitterApi:
    def __init__(self, auto_login=True):
        self.apiUrl = r'https://api.twitter.com/1.1/'
        self.apiUpload = r'https://upload.twitter.com/1.1/'
        self.logged_in = False
        self.auth = None
        self.authSess = None
        self.following = None
        self.me = None

        self._set_auth()

        if auto_login:
            valid, text = self.login_procedure()

    def login_procedure(self):
        valid, self.me, message = self._verifyOAuth()
        if valid:
            self.logged_in = True
        else:
            print(f'Error: {message}\n'
                  'Check "Analyzer\\Readme.md" if you got problems')
            sys.exit(1)
        return valid, message

    def _set_auth(self):
        file_path = os.path.join(os.path.dirname(__file__), 'secret_token.txt')
        try:
            with open(file_path, 'rt') as token_file:
                data = json.load(token_file)
                consumer_key = data['consumer_key']
                consumer_secret = data['consumer_secret']
                access_token_key = data['access_token_key']
                access_token_secret = data['access_token_secret']

                auth = OAuth1(consumer_key,
                              consumer_secret,
                              access_token_key,
                              access_token_secret)

                self.auth = auth
                self.authSess = OAuth1Session(consumer_key,
                                              consumer_secret,
                                              access_token_key,
                                              access_token_secret)
                return True, "Its ok"

        except FileNotFoundError:
            with open(file_path, 'wt') as file:
                data = json.dumps({
                    "consumer_key": "ABC",
                    "consumer_secret": "ABC",
                    "access_token_key": "ABC",
                    "access_token_secret": "ABC"},
                    indent=4)
                file.write(data)
                return True, "Created blank secret file."

        except json.decoder.JSONDecodeError:
            message = "Exception: secret_token.txt is not in json format!"
            return False, message

        except KeyError:
            message = "Exception: secret_token.txt is missing some keys!"
            return False, message

    def _verifyOAuth(self):
        try:
            valid, message = self._set_auth()
            if not valid:
                return False, None, message
            url = self.apiUrl + r'/account/verify_credentials.json'
            response = requests.get(url, auth=self.auth)
            self.verify_response(response)
            me = response.json()
            return True, me, f'Logged in successfully as {me["screen_name"]}'
        except Unauthorized:
            return False, None, 'Authorization failed! Invalid or expired token.'

    def collectHomeLine(self, chunk_size=200):
        # if not self.logged_in:
        #     raise Unauthorized('Authentication not verified!')
        if chunk_size < 0:
            chunk_size = 1
        elif chunk_size > 200:
            chunk_size = 200

        params = {'count': chunk_size}
        full_url = self.apiUrl + r'/statuses/home_timeline.json'
        valid, data = self.make_request(full_url, params=params)
        return data

    def make_request(self, full_url, params=None, header=None, extended=True):
        if params is None:
            params = {}
        if extended:
            params.update({'tweet_mode': 'extended'})
        response = requests.get(full_url, headers=header, params=params, auth=self.auth)
        
        if self.verify_response(response):
            return True, response.json()
        else:
            return False, None

    def post_image(self, imageBinary):
        full_url = self.apiUpload + r'/media/upload.json'
        if imageBinary:
            files = {'media': imageBinary}
        else:
            raise ValueError('No image is given, can not post tweet')        
        data = self.authSess.post(full_url, files=files)
        return data.json()['media_id']

#    def postLarge_image(self, imagePath):
#        fullUrl = self.apiUpload + r'/media/upload.json'
#        sizeB = os.path.getsize(imagePath)
#
#        'Step 1 of 4 INIT'
#        params = {'command': 'INIT',
#                  'media_type ': r'image/png',
#                  'total_bytes': sizeB}
#
#        valid, resp_init = self.post_request(fullUrl, params=params)
#        media_id = resp_init['media_id']
#        print(media_id)
#
#        'Step 2 of 4 Append'
#        fullUrl = self.apiUpload + r'/media/upload.json'
#        with open(imagePath, 'rb') as image:
#            params = {'command': 'APPEND',
#                      'media_id ': media_id,
#                      'media': image,
#                      'segment_index': 0}
#            files = {}
# ##        valid, resp_init = self.post_request(fullUrl, params=params, files=files)
#            valid, resp_init = self.authSess.post(fullUrl, params=params, files=files)
#        'Step 3 of 4 Get id'
#        'Step 4 of 4 Finalize'

    def post_request(self, fullUrl, header=None, params=None, files=None):
        if params is None:
            params = {}
        if files is None:
            files = {}
        response = requests.post(fullUrl, headers=header, params=params, auth=self.auth)        
        if self.verify_response(response):
            return True, response.json()
        else:
            return False, None
        
    def post_status(self, text, image_path=None, image_binary=None):
        params = {}
        pic_id = None
        
        if image_path:
            with open(image_path, 'rb') as image:
                pic_id = self.post_image(image.read())            
            params.update({'media_ids': pic_id})
            
        elif image_binary:
            pic_id = self.post_image(image_binary)
            params.update({'media_ids': pic_id})
            
        if text:
            params.update({'status': str(text)})
                    
        fullUrl = self.apiUrl + r'/statuses/update.json'        
        valid, data = self.post_request(fullUrl, params=params)
         
    def request_status(self, statusID):        
        full_url = self.apiUrl + r'/statuses/show.json'
        params = {'id': int(statusID)}
        valid, data = self.make_request(full_url, params=params)
        return data
        
    @staticmethod
    def verify_response(response):
        resp_code = response.status_code
        if resp_code == 200:
            return True
        elif resp_code == 202:
            return True
        # elif resp_code == 400:
        # pass
        elif resp_code == 401:
            raise Unauthorized('No access to this request')
        # elif resp_code == 402:
        #     pass
        elif resp_code == 404:
            raise ApiNotFound('Error 404')
        elif resp_code == 429:
            raise TooManyRequests('Error 429, too many requests.')
        else:            
            raise Exception(f'Error {resp_code}: {response.json()}')

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
        """Returns the first argument used to construct this error."""
        return self.args[0]


class ApiNotFound(Exception):  # 404
    """Base class for Twitter errors"""
    @property
    def message(self):
        """Returns the first argument used to construct this error."""
        return self.args[0]


class TooManyRequests(Exception):  # 429
    """Base class for Twitter errors"""
    @property
    def message(self):
        """Returns the first argument used to construct this error."""
        return self.args[0]


if __name__ == "__main__":
    app = TwitterApi()
    # app.post_status('Test Api imagebinary', imagePath='220_kookaburra.png')
    # app.postLarge_image('220_kookaburra.png')
