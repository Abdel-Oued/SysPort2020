import json
import os
import pickle
from flask import Flask, request, Response
import tensorflow as tf
from threading import Thread
from multiprocessing.dummy import Process
import identify_face_video


app = Flask(__name__)


@app.route('/')
def index():
    return "Welcome to SysPort !"


@app.route('/information/', methods=['GET'])
def information():
    """
    Répond aux requêtes du client sur cet endpoint.
    :return: Retourne les informations.
    """
    out_file = open("information.json", "r")
    return Response(response=out_file, status=200, mimetype="application/json")


@app.route('/startcamera/', methods=['POST'])
def startCamera():
    """
    Démarre la camera en exécutant le programme de reconnaissance faciale.
    :return: Le statut du traitement.
    """
    # récupération du paramètre ip_adress de la requête
    ip_adress = request.form.get('ip_adress')
    print(ip_adress)
    #on definit identify_functions.video_source comme étant ip_adress
    identify_face_video.video_source = ip_adress
    # exécution de la méthode identify_functions.identify_on_video dans un Thread
    t = Thread(target=identify_face_video.identify_on_video, name="video", args=(), daemon=True)
    t.start()
    return Response(status=200)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

