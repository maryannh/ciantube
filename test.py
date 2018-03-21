from __future__ import unicode_literals
import youtube_dl
from pymongo import MongoClient
import schedule
import time
import pprint
from bson.objectid import ObjectId

client = MongoClient('mongodb://maryann:ferrari1357@ds159845.mlab.com:59845/tube')

db = client['tube']

user = "5aa10855333361ff705c95b6"

pprint.pprint(db.users.find_one({"_id": ObjectId(user)}, {"_id": 0, "playlist": 1}))