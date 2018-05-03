from flask import Flask, render_template, flash, redirect, request, url_for, make_response, session
from flask_pymongo import PyMongo
from pymongo import MongoClient
import random
from forms import LoginForm
from random import shuffle
import keen
import json
from config import Config
# from secrets import token_hex
import random
from models import get_random_string, get_playlist_videos, get_tags, list_to_string
from classifier import search
from http import cookies
import os
from furl import furl
import requests
from bson.objectid import ObjectId

app = Flask(__name__)
app.config.from_object(Config)

client = MongoClient('mongodb://maryann:ferrari1357@ds159845.mlab.com:59845/tube')
db = client['tube']

keen.project_id = "5aa05555c9e77c00010a94be"
keen.write_key = "AAD43B2F5097D6C2178160538A16593FAA95F8C8D5EE2527F4961A21AE83D3355D75AA50B4616A3A1BEA3439153C3AEEBEE67B8A82A9F93BE58B76A2A435E096D860CE17593216BC8E605B18EB74664397BBB07CB60EE9D3640AD0570207283A"
keen.read_key = "A8B4DC61230BAFC32A7627130B3F702A58FCFD2A96DF525A468ED37E53A857B06E34E454AB9A1FC650B65898DBA58B0E62D18E4531F6D9B95B444B03932A460FD0FD3766FCB81F1F10E2E5623CC9CDB023EE0410C727A7D75928E0FCDC9BD2FB"

playlist_id = "PL1b8owEkl1hbpHBaBVEJqTp1oDs-lilJu"
playlist_url = "https://www.youtube.com/playlist?list=PL1b8owEkl1hbpHBaBVEJqTp1oDs-lilJu"
api_key = "AIzaSyAFPIXRHo1lUTrkKnVAfZRIHO74WBfmq6A"

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')
@app.route('/index')
def index():
    videos = list(db.videos.find({}).sort("video_id", -1))
    keen.add_event("view", {"page": "home"})
    return render_template('home.html', videos=videos, user=user, playlist_url=playlist_url)
  
@app.route('/recent')
def recent():
    keen.add_event("view", { "page": "recent" })  
    recent_videolist = keen.select_unique("video_view", target_property="page", timeframe="this_7_days", filters=[{ "property_name": "_id", "operator": "ne", "property_value": user }])
    return render_template('recent.html', recent_videolist=recent_videolist)
  
@app.route('/dev/videos/<video>', methods=['GET'])
def video(video):
    tags = list_to_string(video)
    search_term = tags +  " -" + video
    videos = search(search_term)
    amount_of_related_videos = len(videos)
    random_videos_to_get = 6 - amount_of_related_videos
    random_videos = db.videos.find().limit(random_videos_to_get)
    videos.append(random_videos)
    referring_url = request.headers.get("Referer")
    keen.add_event("view", { "_id": user, "page": "video", "referrer": referring_url,})
    keen.add_event("video_view", { "_id": user, "page": video, "referrer": referring_url,  })
    return render_template('video.html', video=video, videos=videos, tags=tags, user=user)

@app.route('/tags/<tag>', methods=['GET'])
def tag(tag):
    return render_template('tag.html', tag=tag, tag_videolist=tag_videolist, taglist=taglist)

if __name__ == '__main__':
      app.run(debug=True, host='0.0.0.0')