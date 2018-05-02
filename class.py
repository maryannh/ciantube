from pymongo import MongoClient
from models import get_playlist_videos, get_playlist_videos_by_user, get_description_noun_phrases
import boto3
import urllib.request

def tag_videos():
    client = MongoClient('mongodb://maryann:ferrari1357@ds159845.mlab.com:59845/tube')
    db = client['tube']
    playlists = list(db.users.find({}, {"playlist_url": 1, "user": 1, "_id": 0}))
    for playlist in playlists:
        playlist_url = playlist['playlist_url']
        user = playlist['user']
        video_list = list(get_playlist_videos_by_user(playlist_url, "50", user))
        for video in video_list:
            video_id = video['video_id']
            user = video['user']
            tags = get_description_noun_phrases(video_id)
            db.videos.update( { "video_id": video_id }, {"$set": { "video_id": video_id, "user": user, "tags": tags }}, upsert = True )

        