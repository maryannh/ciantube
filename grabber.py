from __future__ import unicode_literals
import youtube_dl
from pymongo import MongoClient
import schedule
import time
import pprint
from bson.objectid import ObjectId

client = MongoClient('mongodb://maryann:ferrari1357@ds159845.mlab.com:59845/tube')

db = client['tube']

user = "5aa10855333361ff705c95b6"

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)
        
user = "5aa10855333361ff705c95b6"        
playlist = db.users.find_one({"_id": ObjectId(user)}, {"_id": 0, "playlist": 1})
playlist_url = playlist.get("playlist")


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


ydl_opts = {
    'forceid': True,
    'dump_single_json': True,
    'simulate': True,
    'skip_download': True,
    'download_archive': "downloaded.txt",
    'outtmpl': '%(id)s',
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([playlist_url])