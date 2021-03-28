#244 1786
import os
import time
import cv2
import numpy as np
from ppadb.client import Client
adb = Client(host = '127.0.0.1',port = 5037)

devices = adb.devices()

if len(devices) == 0:
    print('no device attached')
    quit()
device = devices[0]

while True:
    img = device.screencap()
    with open('screen.png','wb') as f:
       f.write(img)
    img = cv2.imread('screen.png')
    #print(img.shape)
    #img = cv2.resize(img,(324,702))
    floor = img[1900:1901,3:1075]
    #print(floor[0])
    r1,g1,b1 = floor[0][0][0],floor[0][0][1],floor[0][0][2]
    edge=[]
    #print(floor[0][1])
    count = 0
    for (r,g,b) in floor[0]:
        count+=1
        #print(r,g,b)
        if (r+g+b == r1+g1+b1):
            continue
        if (r+g+b !=0 and r1+g1+b1 == 0):
            edge.append(count)
        elif(r+g+b == 0 and r1+g1+b1 != 0):
            edge.append(count)
        r1,g1,b1 =r,g,b
    print(edge)
    #print(len(edge))
    if(len(edge) == 2):
        edge.append(1075)
    elif(len(edge) == 3):
        distance = ((edge[1]+edge[2])/2-edge[0])*0.999
    elif(len(edge) == 4):
        distance = (edge[2]+edge[3])/2-edge[1]
    else:
        continue
    distance*=0.975
    print(distance)
    #print(img)
    #cv2.imshow('img',floor)
    os.system('adb shell input swipe 500 500 500 500 '+str(int(distance)))
    #os.system('adb shell input swipe 500 500 500 500 50')
    time.sleep(3)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cv2.destroyAllWindows()