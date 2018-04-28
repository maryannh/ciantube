from flask import Flask, render_template, flash, redirect, request, url_for, make_response, session
from flask_pymongo import PyMongo
from pymongo import MongoClient
import random
from forms import LoginForm
from random import shuffle
import keen
import json
from config import Config
from secrets import token_hex
from http import cookies
import os
import requests
from furl import furl
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
user = "not_logged_in"

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')
@app.route('/index')
def index():
    playlist_url = "https://www.youtube.com/playlist?list=PL1b8owEkl1hbpHBaBVEJqTp1oDs-lilJu"
    part = 'contentDetails'
    max_result = "50"
    user = request.cookies.get('ct_cookie')
    if user:
        # query database for playlist_url for user
        playlist_url_doc = db.users.find_one({"user": user}, {"playlist_url": 1, "_id": 0})
        playlist_url = playlist_url_doc['playlist_url']
    else:
        if 'session_name' in session:
            user = session['session_name']
        else:
            session['session_name'] = token_hex(16)
            user = session['session_name']
    url_parts = furl(playlist_url)
    playlist_id = url_parts.args['list']
    api_url = "https://www.googleapis.com/youtube/v3/playlistItems?part=" + part + "&maxResults=" + max_result + "&playlistId=" + playlist_id + "&fields=items(contentDetails(videoId%2CvideoPublishedAt))&key=" + api_key
    r = requests.get(api_url)
    data = r.json()
    videos = list(data['items'])
    shuffle(videos)
    url = request.headers.get("Referer")
    keen.add_event("view", { "_id": user, "page": "home", "referrer": url, })
    return render_template('home.html', videos=videos, user=user, playlist_url=playlist_url, url_parts=url_parts, playlist_id=playlist_id)
  
@app.route('/new')
def new():
    part = 'contentDetails'
    max_result = "12"
    user = request.cookies.get('ct_cookie')
    if user:
        # query database for playlist_url for user
        playlist_url_doc = db.users.find_one({"user": user}, {"playlist_url": 1, "_id": 0})
        playlist_url = playlist_url_doc['playlist_url']
    else:
        playlist_url = "https://www.youtube.com/playlist?list=PL1b8owEkl1hbpHBaBVEJqTp1oDs-lilJu"
        if 'session_name' in session:
            user = session['session_name']
        else:
            session['session_name'] = token_hex(16)
            user = session['session_name']
    url_parts = furl(playlist_url) 
    playlist_id = url_parts.args['list']
    api_url = "https://www.googleapis.com/youtube/v3/playlistItems?part=" + part + "&maxResults=" + max_result + "&playlistId=" + playlist_id + "&fields=items(contentDetails(videoId%2CvideoPublishedAt))&key=" + api_key
    url = request.headers.get("Referer")
    r = requests.get(api_url)
    data = r.json()
    keen.add_event("view", { "_id": user, "page": "new", "referrer": url, })
    new_videolist = list(data['items']) 
    return render_template('new.html', new_videolist=new_videolist)
  
@app.route('/recent')
def recent():
    url = request.headers.get("Referer")
    user = request.cookies.get('ct_cookie')
    if user:
        # query database for playlist_url for user
        playlist_url_doc = db.users.find_one({"user": user}, {"playlist_url": 1, "_id": 0})
        playlist_url = playlist_url_doc['playlist_url']
    else:
        playlist_url = "https://www.youtube.com/playlist?list=PL1b8owEkl1hbpHBaBVEJqTp1oDs-lilJu"
        if 'session_name' in session:
            user = session['session_name']
        else:
            session['session_name'] = token_hex(16)
            user = session['session_name']
    keen.add_event("view", { "_id": user, "page": "recent", "referrer": url, })  
    recent_videolist = keen.select_unique("video_view", target_property="page", timeframe="this_7_days", filters=[{ "property_name": "_id", "operator": "ne", "property_value": user }])
    return render_template('recent.html', recent_videolist=recent_videolist)
  
@app.route('/dev/videos/<video>', methods=['GET'])
def video(video):
    part = 'contentDetails'
    max_result = "50"
    user = request.cookies.get('ct_cookie')
    if user:
        # query database for playlist_url for user
        playlist_url_doc = db.users.find_one({"user": user}, {"playlist_url": 1, "_id": 0})
        playlist_url = playlist_url_doc['playlist_url']
    else:
        playlist_url = "https://www.youtube.com/playlist?list=PL1b8owEkl1hbpHBaBVEJqTp1oDs-lilJu"
        if 'session_name' in session:
            user = session['session_name']
        else:
            session['session_name'] = token_hex(16)
            user = session['session_name']
    url_parts = furl(playlist_url) 
    playlist_id = url_parts.args['list']
    api_url = "https://www.googleapis.com/youtube/v3/playlistItems?part=" + part + "&maxResults=" + max_result + "&playlistId=" + playlist_id + "&fields=items(contentDetails(videoId%2CvideoPublishedAt))&key=" + api_key
    r = requests.get(api_url)
    data = r.json()
    videos = list(data['items'])
    shuffle(videos)
    url = request.headers.get("Referer")
    keen.add_event("view", { "_id": user, "page": "video", "referrer": url,})
    keen.add_event("video_view", { "_id": user, "page": video, "referrer": url,  })
    return render_template('video.html', video=video, videos=videos)
  
@app.route('/config', methods=['GET', 'POST'])
def config():
    form = LoginForm()
    if form.validate_on_submit():
        playlist_url = form.playlist.data
        url_parts = furl(playlist_url) 
        playlist_id = url_parts.args['list']
        playlist_details_url = "https://www.googleapis.com/youtube/v3/playlists?part=snippet%2CcontentDetails&id=" + playlist_id + "&maxResults=1&fields=items%2Fsnippet%2Ftitle&key=" + api_key
        r = requests.get(playlist_details_url)
        data = r.json()
        playlist_info = list(data['items'])
        for info in playlist_info:
            playlist_name = info['snippet']['title']
        flash('The {} playlist has been added'.format(
        playlist_name))
        response = redirect(url_for('index'))
        if form.remember_me.data == True:
            user = playlist_id + "_" + token_hex(16)
            db.users.insert( { "playlist_url": playlist_url, "playlist_id": playlist_id, "user": user } )
            keen.add_event("add_playlist", { "_id": user, "playlist_id": playlist_id,})
            response.set_cookie('ct_cookie', user)
        else:
            if 'session_name' in session:
                user = session['session_name']
            else:
                session['session_name'] = token_hex(16)
                user = session['session_name']
        return response
    # keen.add_event("view", { "_id": user, "page": "config", "referrer": url,})
    return render_template('config.html', title='Sign In', form=form)


@app.route('/tags/<tag>', methods=['GET'])
def tag(tag):
    return render_template('tag.html', tag=tag, tag_videolist=tag_videolist, taglist=taglist)

if __name__ == '__main__':
      app.run(debug=True, host='0.0.0.0')