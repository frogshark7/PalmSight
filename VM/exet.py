import io
import os
from google.cloud import vision
from google.cloud.vision import types
import enchant
import re
from redis import Redis
import math
import json
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import time
'''
cred = credentials.Certificate("fire-sdk.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://fire-30e38.firebaseio.com/'
})
'''

cli = Redis('localhost')

rdb = Redis(
    host='redis-11474.c10.us-east-1-2.ec2.cloud.redislabs.com',
    port=11474,
    password='IwNcW6koViX3AowEKOTNAb35tEcJwvsL')

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="BlindCV-0869c1c7984f.json"
client = vision.ImageAnnotatorClient()

def gettext():
    file_name = os.path.join(os.path.dirname(__file__), '../send.jpg')
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()
    image = types.Image(content=content)
    reply = client.text_detection(image=image)
    labels = reply.text_annotations
    d = enchant.Dict("en_US")
    try:
        text = next(iter(labels)).description
        words = (text.replace("\n", " ")).split(" ")
        for i in range(len(words)):
            words[i] = (re.sub(r"[^a-zA-Z0-9]","",words[i])).lower()
        words = list(filter(None, words))
        response = ""
        for i in range(len(words)-1, -1, -1):
            if not d.check(words[i]):
                del words[i]
        response = " ".join(str(x) for x in words)
        if response == "":
            response = "no text found"
    except:
        response = "no text found"
    return response

init = 0
prev = 0