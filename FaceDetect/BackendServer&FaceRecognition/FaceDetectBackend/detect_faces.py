# import the necessary packages
import os.path
import numpy as np
import cv2
import json
import uuid
#import argparse


#Function detect face from image
def faceDetect(image):
    # load our serialized model from disk
    print("[INFO] loading model...")
    #net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])
    prototxt = 'deploy.prototxt.txt'
    model = 'res10_300x300_ssd_iter_140000.caffemodel'
    net = cv2.dnn.readNetFromCaffe(prototxt, model)

    # load the input image and construct an input blob for the image
    # by resizing to a fixed 300x300 pixels and then normalizing it
    #image = cv2.imread(args["image"])
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0,
	    (300, 300), (104.0, 177.0, 123.0))

    # pass the blob through the network and obtain the detections and
    # predictions
    print("[INFO] computing object detections...")
    net.setInput(blob)
    detections = net.forward()

    # loop over the detections
    for i in range(0, detections.shape[2]):
	    # extract the confidence (i.e., probability) associated with the
	    # prediction
	    confidence = detections[0, 0, i, 2]
    
	    # filter out weak detections by ensuring the `confidence` is
	    # greater than the minimum confidence
        # if confidence > args["confidence"]:
	    if confidence > 0.5 :
		    # compute the (x, y)-coordinates of the bounding box for the
		    # object
		    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
		    (startX, startY, endX, endY) = box.astype("int")
 
		    # draw the bounding box of the face along with the associated
		    # probability
		    text = "{:.2f}%".format(confidence * 100)
		    y = startY - 10 if startY - 10 > 10 else startY + 10
		    cv2.rectangle(image, (startX, startY), (endX, endY),
			    (0, 255, 0), 15)  
		    cv2.putText(image, text, (startX, y),
			    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 15)
    
    #save file
    #path_file = ('C:/Users/USER/Documents/Sysport/FaceDetect/FaceDetectBackend/static/%s.jpg' %uuid.uuid4().hex)
    path_file = ('static/%s.jpg' %uuid.uuid4().hex)
    cv2.imwrite(path_file,image)
    return json.dumps(path_file) #return image file name
