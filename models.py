import random
import hashlib
import time
import requests
from random import shuffle
from furl import furl

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

def get_playlist_videos(playlist_url, max_result):
    """
    Returns a shuffled list of videos from a playlist
    """
    part = 'contentDetails'
    api_key = "AIzaSyAFPIXRHo1lUTrkKnVAfZRIHO74WBfmq6A"
    url_parts = furl(playlist_url)
    playlist_id = url_parts.args['list']
    api_url = "https://www.googleapis.com/youtube/v3/playlistItems?part=" + part + "&maxResults=" + max_result + "&playlistId=" + playlist_id + "&fields=items(contentDetails(videoId%2CvideoPublishedAt))&key=" + api_key
    r = requests.get(api_url)
    data = r.json()
    videos = list(data['items'])
    shuffle(videos)
    return videos