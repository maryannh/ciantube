from flask import Flask, render_template, request
from flask_pymongo import PyMongo
from random import sample
import keen

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://maryann:ferrari1357@ds159845.mlab.com:59845/tube'
mongo = PyMongo(app)

keen.project_id = "5aa05555c9e77c00010a94be"
keen.write_key = "AAD43B2F5097D6C2178160538A16593FAA95F8C8D5EE2527F4961A21AE83D3355D75AA50B4616A3A1BEA3439153C3AEEBEE67B8A82A9F93BE58B76A2A435E096D860CE17593216BC8E605B18EB74664397BBB07CB60EE9D3640AD0570207283A"
keen.read_key = "A8B4DC61230BAFC32A7627130B3F702A58FCFD2A96DF525A468ED37E53A857B06E34E454AB9A1FC650B65898DBA58B0E62D18E4531F6D9B95B444B03932A460FD0FD3766FCB81F1F10E2E5623CC9CDB023EE0410C727A7D75928E0FCDC9BD2FB"

user = "5aa10855333361ff705c95b6"

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')
def index():
    channels = mongo.db.channels
    videos = mongo.db.videos
    url = request.headers.get("Referer")
    ip = request.remote_addr
    keen.add_event("view", { "_id": user, "page": "home", "referrer": url, "ip": ip })
    tags = list(videos.distinct("tags"))
    taglist = sample(tags, k=len(tags))
    random_videolist = list(videos.aggregate([{ "$lookup":
     {
       "from": "channels",
       "localField": "channel",
       "foreignField": "_id",
       "as": "video_info"
     }
    },
                                              
            { "$sample": { "size": 12 } }                          
                                      
     ]))
  
    return render_template('home.html', taglist=taglist, tags=tags, random_videolist=random_videolist)
  
@app.route('/new')
def new():
    channels = mongo.db.channels
    videos = mongo.db.videos
    url = request.headers.get("Referer")
    ip = request.remote_addr
    keen.add_event("view", { "_id": user, "page": "home", "referrer": url, "ip": ip })
    new_videolist = list(videos.aggregate([{ "$lookup":
     {
       "from": "channels",
       "localField": "channel",
       "foreignField": "_id",
       "as": "video_info"
     }
    }
     ]))
  
    return render_template('new.html', new_videolist=new_videolist)
  
@app.route('/recent')
def recent():
    channels = mongo.db.channels
    videos = mongo.db.videos
    url = request.headers.get("Referer")
    ip = request.remote_addr
    keen.add_event("view", { "_id": user, "page": "recent", "referrer": url, "ip": ip })
    recent_videolist = keen.select_unique("video_view", target_property="page", timeframe="this_7_days")
    return render_template('recent.html', recent_videolist=recent_videolist)
  
@app.route('/videos/<video>', methods=['GET'])
def video(video):
    channels = mongo.db.channels
    videos = mongo.db.videos
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
    channels = mongo.db.channels
    videos = mongo.db.videos
    url = request.headers.get("Referer")
    ip = request.remote_addr
    keen.add_event("view", { "_id": user, "page": "tag", "referrer": url, "ip": ip })
    tags = list(videos.distinct("tags"))
    taglist = sample(tags, k=len(tags))
    tag_videolist = list(videos.aggregate([{ "$lookup":
     {
       "from": "channels",
       "localField": "channel",
       "foreignField": "_id",
       "as": "video_info"
     },
},
    { "$match" : { "tags" : tag } }    
                                      
                                      ]))
    
    
    return render_template('tag.html', tag=tag, tag_videolist=tag_videolist, taglist=taglist)

if __name__ == '__main__':
      app.run(debug=True, host='0.0.0.0')