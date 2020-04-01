from setuptools import setup

setup(
   name='twitter_analyzer',
   version='0.5',
   description='Gathering Tweets, Posting Tweets, Manipulation stored Tweets' \
   +' in CSV',
   author='Grzegorz Krug',
   author_email='my mail',
   packages=['twitter_analyzer'],  #same as name
   install_requires=[
       'pandas==1.0.1', 'PyQt5==5.14.1', 'request==2019.4.13', 'requests==2.23.0',
       'requests_oauthlib==1.3.0', 'pytest==5.3.5',
       'psycopg2-binary==2.8.4', 'SQLAlchemy==1.3.15', 'pytest==5.3.5'
   ],
)
