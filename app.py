from flask import Flask, render_template, flash, redirect, request, url_for, make_response, session
from flask_pymongo import PyMongo
from pymongo import MongoClient
import random
from forms import SuggestForm, AddForm
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
import config

app = Flask(__name__)
app.config.from_object(Config)

client = MongoClient(config.MONGO_URL)
db = client['tube']

playlist_id = "PL1b8owEkl1hbpHBaBVEJqTp1oDs-lilJu"
playlist_url = "https://www.youtube.com/playlist?list=PL1b8owEkl1hbpHBaBVEJqTp1oDs-lilJu"

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')
@app.route('/index')
def index():
    choose_method = ["popular", "trending"]
    method = random.choice(choose_method)
    if method == "popular":
        timeframe = "this_1_years"
    if method == "trending":
        timeframe = "this_7_days"
    keen.add_event("view", { "page": method })  
    videos = keen.count("video_view", timeframe=timeframe, group_by="page", order_by={"property_name": "result", "direction": keen.direction.ASCENDING})
    return render_template('home.html', videos=videos, playlist_url=playlist_url)
  
@app.route('/new')
def new():
    keen.add_event("view", { "page": "new" })  
    new_videolist = list(db.videos.find({}).sort("updated.$date", -1).limit(12))
    return render_template('new.html', new_videolist=new_videolist)

@app.route('/popular')
def popular():
    choose_method = ["popular", "trending"]
    method = random.choice(choose_method)
    if method == "popular":
        timeframe = "this_1_years"
    if method == "trending":
        timeframe = "this_7_days"
    keen.add_event("view", { "page": method })  
    popular_videolist = keen.count("video_view", timeframe=timeframe, group_by="page")
    return render_template('popular.html', popular_videolist=popular_videolist)
  
@app.route('/videos/<video>', methods=['GET'])
def video(video):
    tags = list_to_string(video)
    search_term = tags +  " -" + video
    videos = search(search_term)
    amount_of_related_videos = len(videos)
    random_videos_to_get = 8 - amount_of_related_videos
    random_videos = db.videos.find().limit(random_videos_to_get)
    videos.append(random_videos)
    referring_url = request.headers.get("Referer")
    keen.add_event("view", {"page": "video"})
    keen.add_event("video_view", {"page": video })
    return render_template('video.html', video=video, videos=videos, tags=tags)

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/suggest', methods=['GET', 'POST'])
def suggest():
    form = SuggestForm()
    keen.add_event("view", {"page": "suggest"})
    if form.validate_on_submit():
        suggestion = form.suggestion.data
        # add mongodb update stuff here
        db.suggestions.insert({"suggestion": suggestion})
        flash('Thanks for your suggestion!')
        return redirect('/index')
    return render_template('suggest.html', form=form)

@app.route('/add_bt7j0srn69', methods=['GET', 'POST'])
def add_bt7j0srn69():
    form = AddForm()
    if form.validate_on_submit():
        playlist_id = form.playlist.data
        db.seed_playlist.insert({"playlist_id": playlist_id})
        flash('Playlist added')
        return redirect('/add_bt7j0srn69')
    return render_template('add.html', form=form)

@app.route('/tags/<tag>', methods=['GET'])
def tag(tag):
    return render_template('tag.html', tag=tag, tag_videolist=tag_videolist, taglist=taglist)

if __name__ == '__main__':
      app.run(debug=True, host='0.0.0.0')