import os

SECRET_KEY = os.environ.get('SECRET_KEY')

MONGO_URL = os.environ.get('MONGO_URL')

KEEN_WRITE = os.environ.get('KEEN_WRITE')
KEEN_READ = os.environ.get('KEEN_READ')
KEEN_PROJECT = os.environ.get('KEEN_PROJECT')

YOUTUBE_KEY = os.environ.get('YOUTUBE_KEY')