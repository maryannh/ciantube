import random
import hashlib
import time
import requests
from random import shuffle
from furl import furl
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from textblob import TextBlob, Word

SECRET_KEY = 's9S7vrcky2Z96Ak0QBUSynFtXj00mQkDwKM6oguktXS4bveJBG'

try:
    random = random.SystemRandom()
    using_sysrandom = True
except NotImplementedError:
    import warnings
    warnings.warn('A secure pseudo-random number generator is not available '
                  'on your system. Falling back to Mersenne Twister.')
    using_sysrandom = False


def get_random_string(length=16,
                      allowed_chars='abcdefghijklmnopqrstuvwxyz'
                                    'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
    """
    Returns a securely generated random string.

    The default length of 12 with the a-z, A-Z, 0-9 character set returns
    a 71-bit value. log_2((26+26+10)^12) =~ 71 bits
    """
    if not using_sysrandom:
        # This is ugly, and a hack, but it makes things better than
        # the alternative of predictability. This re-seeds the PRNG
        # using a value that is hard for an attacker to predict, every
        # time a random string is required. This may change the
        # properties of the chosen random sequence slightly, but this
        # is better than absolute predictability.
        random.seed(
            hashlib.sha256(
                ("%s%s%s" % (
                    random.getstate(),
                    time.time(),
                    SECRET_KEY)).encode('utf-8')
            ).digest())
    return ''.join(random.choice(allowed_chars) for i in range(length))

def get_playlist_api_url(playlist_url, max_result):
    """
    Returns a URL to be used to access YouTube Data API PlaylistItems 
    """
    part = 'contentDetails'
    api_key = "AIzaSyAFPIXRHo1lUTrkKnVAfZRIHO74WBfmq6A"
    url_parts = furl(playlist_url)
    playlist_id = url_parts.args['list']
    playlist_api_url = "https://www.googleapis.com/youtube/v3/playlistItems?part=" + part + "&maxResults=" + max_result + "&playlistId=" + playlist_id + "&fields=items(contentDetails(videoId%2CvideoPublishedAt))&key=" + api_key
    return playlist_api_url

def get_playlist_videos(playlist_url, max_result):
    """
    Returns a shuffled list of videos from a playlist
    """
    playlist_api_url = get_playlist_api_url(playlist_url, max_result)
    r = requests.get(playlist_api_url)
    data = r.json()
    videos = list(data['items'])
    shuffle(videos)
    return videos

def get_playlist_videos_by_user(playlist_url, max_result, user):
    """
    Returns a list of videos from a playlist along with the user ID from the database
    """
    playlist_api_url = get_playlist_api_url(playlist_url, max_result)
    r = requests.get(playlist_api_url)
    data = r.json()
    videos_from_api = list(data['items'])
    videos = []
    for video in videos_from_api:
        video_id = video['contentDetails']['videoId']
        video_info = {"video_id": video_id, "user": user}
        videos.append(video_info)
    return videos

def get_description(video_id):
    """
    Returns the first sentence from the description of a video 
    """
    part = 'snippet'
    api_key = "AIzaSyAFPIXRHo1lUTrkKnVAfZRIHO74WBfmq6A"
    api_url = "https://www.googleapis.com/youtube/v3/videos?part=" + part + "&id=" + video_id + "&fields=items%2Fsnippet%2Fdescription&key=" + api_key
    r = requests.get(api_url)
    data = r.json()
    full_description = data['items'][0]['snippet']['description']
    blob = TextBlob(full_description)
    description = str(blob.sentences[0])
    return description

def get_tags(video_id):
    """
    Returns the noun phrases from the first sentence of a YouTube video description
    """
    description = get_description(video_id)
    blob = TextBlob(description)
    sentence = blob.sentences[0]
    tags = []
    for word,pos in sentence.tags:
        if pos == 'NN':
            tags.append(word)
    return tags

    
def get_youtube_tags(video_id):
    """
    Get the tags from the YouTube API
    """
    api_key = "AIzaSyAFPIXRHo1lUTrkKnVAfZRIHO74WBfmq6A"
    api_url =  "https://www.googleapis.com/youtube/v3/videos?part=snippet&id=" + video_id + "&fields=items%2Fsnippet%2Ftags&key=" + api_key
    r = requests.get(api_url)
    data = r.json()
    youtube_tags = data['items'][0]['snippet']['tags']
    return youtube_tags
    
def get_title(video_id):
    """
    Get the title from the YouTube API
    """
    api_key = "AIzaSyAFPIXRHo1lUTrkKnVAfZRIHO74WBfmq6A"
    api_url =  "https://www.googleapis.com/youtube/v3/videos?part=snippet&id=" + video_id + "&fields=items%2Fsnippet%2Ftitle&key=" + api_key
    r = requests.get(api_url)
    data = r.json()
    title = data['items'][0]['snippet']['title']
    return title
    
def list_to_string(video):
    tags = get_tags(video)
    tag_string = ' '.join(tags)
    return tag_string

# tags = list_to_string("QA2yjW1XUvA")
# print(tags)