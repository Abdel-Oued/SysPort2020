#START

import os.path
from detect_faces import faceDetect
import numpy as np
import cv2
import json
from flask import Flask, request, Response
import uuid

#Function detect face from image
#def faceDetect(img):
#    #cascPath = "haarcascade_frontalface_default.xml"
#    #face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + cascPath)
#    face_cascade = cv2.CascadeClassifier('face_detect_cascade.xml')
#    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
#    faces = face_cascade.detectMultiScale(gray,1.2,5)
#    for(x,y,w,h) in faces:
#        img = cv2.rectangle(img,(x,y),(w+w,y+h),(0,255,0))
#    #save file
#    #path_file = ('C:/Users/USER/Documents/Sysport/FaceDetect/FaceDetectBackend/static/%s.jpg' %uuid.uuid4().hex)
#    path_file = ('static/%s.jpg' %uuid.uuid4().hex)
#    cv2.imwrite(path_file,img)
#    return json.dumps(path_file) #return image file name

#API
app = Flask(__name__)

#route http post to this method
@app.route('/api/upload', methods=['POST'])
def upload():
    #retrieve image from client
    img = cv2.imdecode(np.fromstring(request.files['image'].read(),np.uint8),cv2.IMREAD_UNCHANGED)
    #img = cv2.imdecode(np.frombuffer(request.files['image'].read(),np.uint8),cv2.IMREAD_UNCHANGED)
    #process image
    img_processed = faceDetect(img)
    #response
    return Response(response=img_processed,status=200,mimetype="application/json") #return json string

@app.route("/")
def index():
    return "Welcome to SysPort !"


@app.route("/information/")
def information():
    # information = [{"nom":"Sunny","prenom":"Deol","dette":30,"tauxAlcool":0},
    #                {"nom":"Salman","prenom":"Khan","dette":0,"tauxAlcool":1.6}]
    # information = {"nom":"Sunny","prenom":"Deol","dette":30,"tauxAlcool":0}
    # return Response(response=json.dumps(information), status=200, mimetype="application/json")

    #cas ou les infos sont enregistrées dans un fichier
    out_file = open("information.json", "r")
    return Response(response=out_file, status=200, mimetype="application/json")


if __name__ == "__main__":
    #start server
    #app.run(host="0.0.0.0", port=5000)
    app.run(host="0.0.0.0", port=8080) #, ssl_context='adhoc')  # https