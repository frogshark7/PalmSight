import os
import subprocess
import time
from multiprocessing import Process
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from redis import Redis
import pexpect
import wget
import datetime
from rq import Queue
from firebase_admin import storage
import shutil
import urllib.request
import json
import boto3
import logging
from botocore.exceptions import ClientError
import flask 
import os
import sys
import base64
import json
from PIL import Image
import io
client = boto3.client('sagemaker')
client3 = boto3.client('textract')

client2 = boto3.client('sagemaker-runtime')
cli = Redis('localhost')
rdb = Redis(
    host='redis-11474.c10.us-east-1-2.ec2.cloud.redislabs.com',
    port=11474,
    password='IwNcW6koViX3AowEKOTNAb35tEcJwvsL')

try:
    rdb.get('mode').decode('utf-8')
    rdb.get('confirm').decode('utf')
    rdb.get('start').decode('utf-8')
except:
    rdb.set('mode', 0)
    rdb.set('confirm', 0)
    rdb.set('start', 0)
    '''
cred = credentials.Certificate("fire-sdk.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://fire-30e38.firebaseio.com/'
})
'''
def v3(prev):
    init = int(cli.get('read').decode('utf-8'))
    print(init)
    print(prev)
    if init != prev:
        start = time.time()
        with open("send.png", "rb") as image:
            f = image.read()
            b = bytearray(f)
            print('here')
            jsonstring = (client2.invoke_endpoint(
            EndpointName='sample-endpoint-134EEA74-A9CA-4B4F-8DB1-B9721EEFC63B-2',\
            Body=b,\
            ContentType="image/png",
            ))['Body'].read().decode("utf-8")
            jsonstring = json.loads(jsonstring)
            listofargs = []
            for i in jsonstring:
                secondlist = []
                secondlist.append(i["id"])
                secondlist.append(i["score"] * 100)
                secondlist.append([i["top"],i["left"],(int(i["right"])-int(i["left"])),(int(i["bottom"])-int(i["top"]))])
                listofargs.append(secondlist)
#                print("yolo", listofargs)
            cli.set('writev3', str(listofargs))
        cint = int(cli.get('confirm').decode('utf-8'))
        cint += 1
        cli.set('confirm', cint)
        print('v3 time:', time.time() - start)
    return init

def pythia():
    os.system("python3 runpythia.py")

def caption():
    os.system("python3 runcaption.py")

def exe():
    os.system("python3 exec.py")

def mrcnn(prev):
    init = int(cli.get('read').decode('utf-8'))
    if init != prev:
        start = time.time()
        with open("send.png", "rb") as image:
            f = image.read()
            b = bytearray(f)
            print('here')
            jsonstring = (client2.invoke_endpoint(
            EndpointName='sample-endpoint-134EEA74-A9CA-4B4F-8DB1-B9721EEFC63B-1',\
            Body=b,\
            ContentType="image/png",
            ))['Body'].read().decode("utf-8")
            jsonstring = json.loads(jsonstring)
            listofargs = []
            for i in jsonstring:
                secondlist = []
                secondlist.append(i["id"])
                secondlist.append(i["score"] * 100)
                secondlist.append([i["top"],i["left"],(int(i["right"])-int(i["left"])),(int(i["bottom"])-int(i["top"]))])
                listofargs.append(secondlist)
#               print("rcnn", listofargs)
            cli.set('writemrcnn', str(listofargs))
        cint = int(cli.get('confirm').decode('utf-8'))
        cint += 1
        cli.set('confirm', cint)
        print('v3 time:', time.time() - start)
    return init
def text(prev):
    init = int(cli.get('read').decode('utf-8'))
    s = time.time()
    if init != prev:
        with open("send.png", "rb") as image:
            f = image.read() 
            b = bytearray(f)
            response = client3.detect_document_text(
            Document={
                'Bytes': b
            }
            )
            columns = []
            lines = []
            for item in response["Blocks"]:
                if item["BlockType"] == "LINE":
                    column_found=False
                    for index, column in enumerate(columns):
                        bbox_left = item["Geometry"]["BoundingBox"]["Left"]
                        bbox_right = item["Geometry"]["BoundingBox"]["Left"] + item["Geometry"]["BoundingBox"]["Width"]
                        bbox_centre = item["Geometry"]["BoundingBox"]["Left"] + item["Geometry"]["BoundingBox"]["Width"]/2
                        column_centre = column['left'] + column['right']/2

                        if (bbox_centre > column['left'] and bbox_centre < column['right']) or (column_centre > bbox_left and column_centre < bbox_right):
                            lines.append([index, item["Text"]])
                            column_found=True
                            break
                    if not column_found:
                        columns.append({'left':item["Geometry"]["BoundingBox"]["Left"], 'right':item["Geometry"]["BoundingBox"]["Left"] + item["Geometry"]["BoundingBox"]["Width"]})
                        lines.append([len(columns)-1, item["Text"]])

            lines.sort(key=lambda x: x[0])
            text = ""
            for line in lines:
                text = text+line[1]
                text = text + '\n'
            text = text.strip()

        print(text)
        ''''
        ref = db.reference()
        ref.update({"text":text})'''
        print(text)
        cli.set('text', text)
        print("text time:", time.time() - s, "\n")
    return init
    

def search():
    os.system("python3 exes.py")

def check():
    prev = 0
    init = 0
    while(True):
        init = int(cli.get('confirm').decode('utf-8'))
        if init == 2:
            print("exe ran")
            exe()
        prev = init
def once():
    done = 0
    #cred = credentials.Certificate("fire-sdk.json")
    #app2 = firebase_admin.initialize_app(cred, {'storageBucket': 'fire-30e38.appspot.com'}, name='storage2')
    print('here')
    while(True):
        #ref = db.reference("status/mode")
        #con = db.reference("status/confirm")
        #start = db.reference("status/start")
        start = rdb.get('start').decode('utf-8')
        con = rdb.get('confirm').decode('utf-8')
        #print(con)
       # print("start:" + start)
        ref = rdb.get('mode').decode('utf-8')
        #if(int(ref.get()) == 0 and int(con.get()) == 0):
        if(int(ref) == 0 and int(con) == 0):
            done = 0
        #stat = int(ref.get())
        #if(int(start.get()) > 0 and done == 0):
        if(int(start) > 0 and done == 0):
            try:
                os.remove("send.png")
            except:
                pass
            #bucket = storage.bucket(app=app2)
            #blob = bucket.blob("sent.jpg")
            #url = blob.generate_signed_url(datetime.timedelta(seconds=300), method='GET')
            #urllib.request.urlretrieve(url, '../send.jpg')

            bytes = rdb.get('imagedata')
            f = open('send.png','wb')
            f.write(bytes)
            f.close()

            start = time.time()
            cli.set('read', int(cli.get('read').decode('utf-8')) + 1)
            while(True):
                if int(cli.get('confirm').decode('utf-8')) == 3:
                    print('here')
                    #ref = db.reference("scan")
                    #ref2 = db.reference("date-time")
                    #ref3 = db.reference("log")
                    #log2ref = db.reference("log2")
                    #stat = db.reference("status")
                    #t = ref2.get()
                    t = rdb.get('date-time')
                    print("TIME:", t)
                    exe = str(cli.get('exe').decode('utf-8'))
                    array = str(cli.get('array').decode('utf-8'))
                    #ref.set({"object":exe, "time":t, "array":array})
                    #ref3.push({"object":exe, "time":t, "array": array})
                    #log2ref.push({"object":exe, "time":t, "array":array})
                    #stat.update({"confirm": 1})
                    rdb.set('s-object', exe)
                    rdb.set('s-time', t)
                    rdb.set('s-array', array)
                    rdb.set('text', str(cli.get('text').decode('utf-8')))

                    print("fire scan")
                    print(exe)
                    cli.set('confirm', 0)
                    rdb.set('confirm', 1)   
                    end = time.time()
                    print("Total", end - start)
                    done = 1
                    break

def reset():
    cli.set('confirm', 0)
    cli.set('read', 0)
    cli.set('writev3', '')
    cli.set('writeoid', '')
    cli.set('write9000', '')
    cli.set('writemrcnn', '')
    cli.set('writepythia', '')
    cli.set('exe', '')
    cli.set('array', '[]')
#    p8 = Process(target=pythia)
#    p8.start()
#    p9 = Process(target=caption)
#    p9.start()