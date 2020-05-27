from PIL import Image
import io
from redis import Redis
from multiprocessing import Process
from datetime import datetime

r = Redis(
    host='redis-11474.c10.us-east-1-2.ec2.cloud.redislabs.com',
    port=11474, 
    password='IwNcW6koViX3AowEKOTNAb35tEcJwvsL')

def start():
    ##reset  all rediis
    r.set('start', 0)
    r.set('confirm', 0)
    r.set('s-object', "")
    r.set('s-time', "")
    r.set('s-array', "")

    im = Image.open('image.jpg')
    im_resize = im.resize((500, 500))
    buf = io.BytesIO()
    im_resize.save(buf, format='JPEG')

    r.set('imagedata', buf.getvalue())
    r.set('start', 1)
    #print(datetime.now())
    r.set('date-time', str(datetime.now()))

def getResults():
    while(True):
        ob = r.get('s-object')
        t = r.get('s-time')
        ar = r.get('s-array')
        text = r.get("text")
        try:
            if(int(r.get('confirm').decode('utf-8')) == 1):
                print(ob.decode('utf-8'))
                print(t.decode('utf-8'))
                print(ar.decode('utf-8'))
                print(text.decode('utf-8'))
                print("Done")
                return
        except:
            pass

if __name__ == '__main__':
    print("starting now")
    p1 = Process(target=start)
    p1.start()
    p2 = Process(target=getResults)
    p2.start()