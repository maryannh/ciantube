from flask import Flask, render_template, request, url_for
from flask_pymongo import PyMongo
from pymongo import MongoClient
from random import shuffle
import keen
import json
import requests
from furl import furl
from bson.objectid import ObjectId

app = Flask(__name__)

client = MongoClient('mongodb://maryann:ferrari1357@ds159845.mlab.com:59845/tube')
db = client['tube']

keen.project_id = "5aa05555c9e77c00010a94be"
keen.write_key = "AAD43B2F5097D6C2178160538A16593FAA95F8C8D5EE2527F4961A21AE83D3355D75AA50B4616A3A1BEA3439153C3AEEBEE67B8A82A9F93BE58B76A2A435E096D860CE17593216BC8E605B18EB74664397BBB07CB60EE9D3640AD0570207283A"
keen.read_key = "A8B4DC61230BAFC32A7627130B3F702A58FCFD2A96DF525A468ED37E53A857B06E34E454AB9A1FC650B65898DBA58B0E62D18E4531F6D9B95B444B03932A460FD0FD3766FCB81F1F10E2E5623CC9CDB023EE0410C727A7D75928E0FCDC9BD2FB"

user = "5aa10855333361ff705c95b6"
playlist = db.users.find_one({"_id": ObjectId(user)}, {"_id": 0, "playlist": 1})
playlist_url = playlist.get("playlist")
url_parts = furl(playlist_url) 
playlist_id = url_parts.args['list']
api_key = "AIzaSyAFPIXRHo1lUTrkKnVAfZRIHO74WBfmq6A"


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')
@app.route('/index')
def index():
    url = request.headers.get("Referer")
    ip = request.remote_addr
    keen.add_event("view", { "_id": user, "page": "home", "referrer": url, "ip": ip })
    part = 'contentDetails'
    max_result = "50"
    api_url = "https://www.googleapis.com/youtube/v3/playlistItems?part=" + part + "&maxResults=" + max_result + "&playlistId=" + playlist_id + "&fields=items(contentDetails(videoId%2CvideoPublishedAt))&key=" + api_key
    r = requests.get(api_url)
    data = r.json()
    videos = list(data['items'])
    shuffle(videos)
    return render_template('home.html', videos=videos)
  
@app.route('/new')
def new():
    part = 'contentDetails'
    max_result = "12"
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
    ip = request.remote_addr
    keen.add_event("view", { "_id": user, "page": "recent", "referrer": url, "ip": ip })
    recent_videolist = keen.select_unique("video_view", target_property="page", timeframe="this_7_days")
    return render_template('recent.html', recent_videolist=recent_videolist)
  
@app.route('/videos/<video>', methods=['GET'])
def video(video):
    channels = db.channels
    videos = db.videos
    url = request.headers.get("Referer")
    ip = request.remote_addr
    keen.add_event("view", { "_id": user, "page": "video", "referrer": url, "ip": ip })
    keen.add_event("video_view", { "_id": user, "page": video, "referrer": url, "ip": ip })
    random_videolist = list(videos.aggregate([{ "$lookup":
     {
       "from": "channels",
       "localField": "channel",
       "foreignField": "_id",
       "as": "video_info"
     }
    },
            { "$match": {"_id": { "$ne": video }} },
                                              
            { "$sample": { "size": 12 } }                          
                                      
     ]))
    return render_template('video.html', video=video, random_videolist=random_videolist)
  
@app.route('/tags/<tag>', methods=['GET'])
def tag(tag):
    return render_template('tag.html', tag=tag, tag_videolist=tag_videolist, taglist=taglist)

if __name__ == '__main__':
      app.run(debug=True, host='0.0.0.0')