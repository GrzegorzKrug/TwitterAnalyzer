# api.py
# Grzegorz Krug

import requests
import json
import os

from .custom_logger import define_logger
from requests_oauthlib import OAuth1, OAuth1Session


class TwitterApi:
    def __init__(self, verify=False):
        self.apiUrl = r'https://api.twitter.com/1.1/'
        self.apiUpload = r'https://upload.twitter.com/1.1/'
        self.logged_in = False
        self.auth = None
        self.authSess = None
        self.following = None
        self.me = None
        self.logger_api = define_logger("Api")

        self._set_auth()
        if verify:
            valid = self.verify_procedure()

    def _make_request(self, full_url, params=None, header=None, extended=True) \
            -> "True, Data or False, None":
        if params is None:
            params = {}
        if extended:
            params.update({'tweet_mode': 'extended'})

        response = requests.get(full_url, headers=header, params=params, auth=self.auth)

        if self._verify_response(response):
            return True, response.json()
        else:
            return False, None

    def _set_auth(self):
        file_path = os.path.join(os.path.dirname(__file__), 'secret_token.txt')
        self.logger_api.debug("Loading credentials")
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
                return True

        except FileNotFoundError:
            with open(file_path, 'wt') as file:
                data = json.dumps({
                    "consumer_key": "ABC",
                    "consumer_secret": "ABC",
                    "access_token_key": "ABC",
                    "access_token_secret": "ABC"},
                    indent=4)
                file.write(data)
                self.logger_api.error('File not found. Created blank secret file.')
                return True

        except json.decoder.JSONDecodeError:
            msg = "Exception: secret_token.txt is not in json format!"
            self.logger_api.error(msg)
            return False

        except KeyError:
            msg = "Exception: secret_token.txt is missing some keys!"
            self.logger_api.error(msg)
            return False

    def _verify_oauth(self):
        try:
            valid = self._set_auth()
            if not valid:
                return False, None
            url = self.apiUrl + r'/account/verify_credentials.json'
            self.logger_api.debug('Checking credentials')
            response = requests.get(url, auth=self.auth)

            self._verify_response(response)
            me = response.json()
            return True, me
        except Unauthorized:
            self.logger_api.error("Authorization failed! Invalid or expired token.")
            return False, None

    @staticmethod
    def _verify_response(response):
        resp_code = response.status_code
        if resp_code == 200:
            return True
        elif resp_code == 202:
            return True
        # elif resp_code == 400:
        # pass
        elif resp_code == 401:
            raise Unauthorized(str(response.json()))
        elif resp_code == 403:
            raise Unauthorized(str(response.json()))
        elif resp_code == 404:
            raise ApiNotFound(str(response.json()))
        elif resp_code == 429:
            raise TooManyRequests('Error 429, too many requests.')
        else:
            raise Exception(f'Error {resp_code}: {response.json()}')

    def request_home_timeline(self, chunk_size: "max is 200" = 200):
        """Api that requests from endpoint of home timeline"""
        if chunk_size < 0:
            chunk_size = 1
        elif chunk_size > 200:
            chunk_size = 200

        params = {'count': chunk_size}
        full_url = self.apiUrl + r'/statuses/home_timeline.json'
        self.logger_api.debug("Requesting home timeline")
        valid, data = self._make_request(full_url, params=params)
        return valid, data

    def post_image(self, image: "binary"):
        full_url = self.apiUpload + r'/media/upload.json'
        if image:
            files = {'media': image}
        else:
            raise ValueError('No image is given, can not post tweet')
        self.logger_api.debug(f"Posting image")
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
#            valid, resp_init = self.post_request(fullUrl, params=params, files=files)
#            valid, resp_init = self.authSess.post(fullUrl, params=params, files=files)
#        'Step 3 of 4 Get id'
#        'Step 4 of 4 Finalize'

    def post_request(self, full_url, header=None, params=None, files=None):
        if params is None:
            params = {}
        if files is None:
            files = {}
        response = requests.post(full_url, headers=header, params=params, auth=self.auth)
        if self._verify_response(response):
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

        full_url = self.apiUrl + r'/statuses/update.json'
        self.logger_api.debug(f"Posing status")
        valid, data = self.post_request(full_url, params=params)
         
    def request_status(self, status_id):
        full_url = self.apiUrl + r'/statuses/show.json'
        params = {'id': int(status_id)}
        self.logger_api.debug(f"Requesting status: {status_id}")
        valid, data = self._make_request(full_url, params=params)
        return data
        
    def verify_procedure(self):
        valid, self.me = self._verify_oauth()
        if valid:
            self.logged_in = True
            self.logger_api.info("Verified OAuth successfully")
        else:
            self.logger_api.error("Check 'analyzer\\Readme.md' if you got problems")
        return valid


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
    pass
