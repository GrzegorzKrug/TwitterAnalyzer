from setuptools import setup

setup(
   name='TwiterAnalyzer',
   version='1.0',
   description='Gathering Tweets, Posting Tweets, Manipulation stored Tweets' \
   +' in CSV',
   author='Grzegorz Krug',
   author_email='my mail',
   packages=['TwiterAnalyzer'],  #same as name
   install_requires=['pandas', 'json', 'glob', 'threading', 'PyQt5',
                     'requests', 'requests_oauthlib', 'os', 'time',
                     'traceback'], #external packages as dependencies
)
