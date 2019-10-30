from setuptools import setup

setup(
   name='Analyzer',
   version='1.0',
   description='Gathering Tweets, Posting Tweets, Manipulation stored Tweets' \
   +' in CSV',
   author='Grzegorz Krug',
   author_email='my mail',
   packages=['Analyzer'],  #same as name
   install_requires=['pandas', 'json', 'glob', 'threading', 'PyQt5',
                     'requests', 'requests_oauthlib', 'time'], #external packages as dependencies
)
