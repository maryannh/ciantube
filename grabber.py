from __future__ import unicode_literals
import youtube_dl
from pymongo import MongoClient
import schedule
import time

client = MongoClient('mongodb://maryann:ferrari1357@ds159845.mlab.com:59845')
db = client.tube
users = db.users

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)
        
user = "5aa10855333361ff705c95b6"        
playlist = db.users.findOne({
  "_id": user
},
{
  "_id": 1
}
)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([playlist])