from pymongo import MongoClient
from models import get_playlist_videos, get_tags, get_description, get_youtube_tags, get_title, list_to_string
import boto3
import pprint
import urllib.request

def tag_videos():
    """
    tag videos with noun phrases from YouTube descriptions
    """
    client = MongoClient('mongodb://maryann:ferrari1357@ds159845.mlab.com:59845/tube')
    db = client['tube']
    playlists = list(db.seed_playlist.find({"added": {"$ne": "yes"}}, {"playlist_id": 1, "_id": 0}))
    for playlist in playlists:
        playlist_id = playlist['playlist_id']
        video_list = list(get_playlist_videos(playlist_id))
        for video in video_list:
            video_id = video['video_id']
            description = get_description(video_id)
            title = get_title(video_id)
            youtube_tags = get_youtube_tags(video_id)
            db.videos.update( { "video_id": video_id }, 
                             {"$set": { "video_id": video_id, "description": description, "youtube_tags": youtube_tags, "title": title }}, upsert = True )
            print(video_id, "added")
        db.seed_playlist.update({"playlist_id": playlist_id}, {"$set": {"added": "yes"}}, upsert=True)
            
def search(search_term):
    client = MongoClient('mongodb://maryann:ferrari1357@ds159845.mlab.com:59845/tube')
    db = client['tube']
    search_results = db.videos.find(
    {"$text": {"$search": search_term}},
    {"score": {"$meta": "textScore"}}
    ).sort([("score", {"$meta": "textScore"}
            )]).limit(6)
    results = []
    for result in search_results:
        results.append(result)
    return results
