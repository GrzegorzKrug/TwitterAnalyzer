from setuptools import setup

setup(
   name='TwitterAnalyzer',
   version='1.0',
   description='Gathering Tweets, Posting Tweets, Manipulation stored Tweets' \
   +' in CSV',
   author='Grzegorz Krug',
   author_email='my mail',
   packages=['TwitterAnalyzer'],  #same as name
   install_requires=['pandas', 'json', 'glob', 'threading', 'PyQt5',
                     'request', 'requests_oauthlib'], #external packages as dependencies
)
