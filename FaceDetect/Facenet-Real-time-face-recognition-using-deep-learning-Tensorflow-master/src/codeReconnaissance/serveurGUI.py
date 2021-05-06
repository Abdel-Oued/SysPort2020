# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\test.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import json
from flask import Flask, request, Response, jsonify
from threading import Thread
from src.codeReconnaissance import identify_face_video
import json, os, signal

app = Flask(__name__)


@app.route("/")
def index(self):
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


@app.route('/stopServer', methods=['GET'])
def stopServer():
    os.kill(os.getpid(), signal.SIGINT)
    return jsonify({ "success": True, "message": "Server is shutting down..." })

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btnConnect = QtWidgets.QPushButton(self.centralwidget)
        self.btnConnect.setGeometry(QtCore.QRect(330, 260, 75, 23))
        self.btnConnect.setObjectName("btnConnect")
        self.btnConnect.clicked.connect(self.transfert_information)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(240, 70, 271, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")
        #self.lbltxt = QtWidgets.QLabel(self.centralwidget)
        #self.lbltxt.setObjectName("lbltxt")
        #self.lbltxt.setGeometry(QtCore.QRect(330, 220, 75, 23))

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(210, 190, 71, 16))
        self.label_2.setObjectName("label_2")
        self.txtIP = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.txtIP.setGeometry(QtCore.QRect(290, 190, 171, 21))
        self.txtIP.setObjectName("txtIP")
        self.btnDeconnect = QtWidgets.QPushButton(self.centralwidget)
        self.btnDeconnect.setGeometry(QtCore.QRect(330, 300, 75, 23))
        self.btnDeconnect.setObjectName("btnDeconnect")
        self.btnDeconnect.clicked.connect(self.deconnexion_serveur)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btnConnect.setText(_translate("MainWindow", "Connect"))
        self.label.setText(_translate("MainWindow", "Welcome to the server"))
        self.label_2.setText(_translate("MainWindow", "Enter your ip:"))
        self.btnDeconnect.setText(_translate("MainWindow", "deconnect"))

    def getIp(self):
        ip = self.txtIP.toPlainText()
        #print(ip)
        self.lbltxt.setText(ip)


    def transfert_information(self):
        app.run(host="0.0.0.0", port=8080)  # ssl_context='adhoc')  # https

    # def identify_face_video():
    #     M = interroBdd.Interro('Clients', 'Clients')
    #     input_video = "akshay_mov.mp4"
    #     modeldir = './model/20170511-185253.pb'
    #     classifier_filename = './class/classifier.pkl'
    #     npy = './npy'
    #     train_img = "./train_img"
    #
    #     liste_json = []
    #     with tf.Graph().as_default():
    #         gpu_options = tf.compat.v1.GPUOptions(per_process_gpu_memory_fraction=0.6)
    #         sess = tf.compat.v1.Session(
    #             config=tf.compat.v1.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
    #         with sess.as_default():
    #             pnet, rnet, onet = detect_face.create_mtcnn(sess, npy)
    #
    #             minsize = 20  # minimum size of face
    #             threshold = [0.6, 0.7, 0.7]  # three steps's threshold
    #             factor = 0.709  # scale factor
    #             margin = 44
    #             frame_interval = 3
    #             batch_size = 1000
    #             image_size = 182
    #             input_image_size = 160
    #
    #             HumanNames = os.listdir(train_img)
    #             HumanNames.sort()
    #
    #             print('Loading Modal')
    #             facenet.load_model(modeldir)
    #             images_placeholder = tf.compat.v1.get_default_graph().get_tensor_by_name("input:0")
    #             embeddings = tf.compat.v1.get_default_graph().get_tensor_by_name("embeddings:0")
    #             phase_train_placeholder = tf.compat.v1.get_default_graph().get_tensor_by_name("phase_train:0")
    #             embedding_size = embeddings.get_shape()[1]
    #
    #             classifier_filename_exp = os.path.expanduser(classifier_filename)
    #             with open(classifier_filename_exp, 'rb') as infile:
    #                 (model, class_names) = pickle.load(infile)
    #
    #             video_capture = cv2.VideoCapture('rtsp://192.168.8.99:1234/')  # input_video)
    #             c = 0  #
    #
    #             print('Start Recognition')
    #             prevTime = 0
    #             while True:
    #                 ret, frame = video_capture.read()
    #
    #                 frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)  # resize frame (optional)
    #
    #                 curTime = time.time() + 1  # calc fps
    #                 timeF = frame_interval
    #
    #                 if (c % timeF == 0):  # la détection est faite chaque timeF frame
    #                     find_results = []
    #
    #                     if frame.ndim == 2:
    #                         frame = facenet.to_rgb(frame)
    #                     frame = frame[:, :, 0:3]
    #                     bounding_boxes, _ = detect_face.detect_face(frame, minsize, pnet, rnet, onet, threshold, factor)
    #                     nrof_faces = bounding_boxes.shape[0]
    #                     print('Detected_FaceNum: %d' % nrof_faces)
    #
    #                     if nrof_faces > 0:
    #                         det = bounding_boxes[:, 0:4]
    #                         img_size = np.asarray(frame.shape)[0:2]
    #
    #                         cropped = []
    #                         scaled = []
    #                         scaled_reshape = []
    #                         bb = np.zeros((nrof_faces, 4), dtype=np.int32)
    #
    #                         for i in range(nrof_faces):
    #                             emb_array = np.zeros((1, embedding_size))
    #
    #                             bb[i][0] = det[i][0]
    #                             bb[i][1] = det[i][1]
    #                             bb[i][2] = det[i][2]
    #                             bb[i][3] = det[i][3]
    #
    #                             # inner exception
    #                             if bb[i][0] <= 0 or bb[i][1] <= 0 or bb[i][2] >= len(frame[0]) or bb[i][3] >= len(
    #                                     frame):
    #                                 print('Face is very close!')
    #                                 continue
    #
    #                             cropped.append(frame[bb[i][1]:bb[i][3], bb[i][0]:bb[i][2], :])
    #                             cropped[i] = facenet.flip(cropped[i], False)
    #                             # scaled.append(misc.imresize(cropped[i], (image_size, image_size), interp='bilinear'))
    #                             scaled.append(
    #                                 np.array(
    #                                     Image.fromarray(cropped[i]).resize((image_size, image_size), Image.BILINEAR)))
    #                             scaled[i] = cv2.resize(scaled[i], (input_image_size, input_image_size),
    #                                                    interpolation=cv2.INTER_CUBIC)
    #                             scaled[i] = facenet.prewhiten(scaled[i])
    #                             scaled_reshape.append(scaled[i].reshape(-1, input_image_size, input_image_size, 3))
    #                             feed_dict = {images_placeholder: scaled_reshape[i], phase_train_placeholder: False}
    #                             emb_array[0, :] = sess.run(embeddings, feed_dict=feed_dict)
    #                             predictions = model.predict_proba(emb_array)
    #                             print(predictions)
    #                             best_class_indices = np.argmax(predictions, axis=1)
    #                             best_class_probabilities = predictions[
    #                                 np.arange(len(best_class_indices)), best_class_indices]
    #                             # print("predictions")
    #                             print(best_class_indices, ' with accuracy ', best_class_probabilities)
    #
    #                             # definir un sueil de probabilite
    #
    #                             # # print(best_class_probabilities)
    #                             if best_class_probabilities > 0.53:
    #
    #                                 nom_prenom = HumanNames[best_class_indices[0]]
    #                                 nom = nom_prenom.split()[0]
    #                                 prenom = nom_prenom.split()[1]
    #
    #                                 print("nom : ", nom)
    #                                 print("taux d'alcool:",
    #                                       M.gation_ID(M.gation_index('\"%s\"' % (nom), 'Nom'), 'tauxAlcool'))
    #                                 print("dette:", M.gation_ID(M.gation_index('\"%s\"' % (nom), 'Nom'), 'Dette'))
    #
    #                                 # écrire les données qui nous intéressent dans un fichier json pour ensuite les transmettre à l'application
    #
    #                                 data = {"nom": nom, "prenom": prenom,
    #                                         "dette": M.gation_ID(M.gation_index('\"%s\"' % (nom), 'Nom'), 'Dette'),
    #                                         "tauxAlcool": M.gation_ID(M.gation_index('\"%s\"' % (nom), 'Nom'),
    #                                                                   'tauxAlcool')}
    #                                 # ajouter les coordonnees
    #
    #                                 if data not in liste_json:  # pour éviter d'ajouter 2 fois la même personne dans la liste de dictionnaire
    #                                     liste_json.append(data)
    #                                 with open("../codeTransfert/information.json", "w") as write_file:
    #                                     json.dump(liste_json, write_file)
    #
    #                                 cv2.rectangle(frame, (bb[i][0], bb[i][1]), (bb[i][2], bb[i][3]), (0, 255, 0),
    #                                               2)  # boxing face
    #
    #                                 # plot result idx under box
    #                                 text_x = bb[i][0]
    #                                 text_y = bb[i][3] + 20
    #                                 print('Result Indices: ', best_class_indices[0])
    #                                 print(HumanNames)
    #
    #                                 for H_i in HumanNames:
    #                                     if HumanNames[best_class_indices[0]] == H_i:
    #                                         result_names = HumanNames[best_class_indices[0]]
    #                                         cv2.putText(frame, result_names, (text_x, text_y),
    #                                                     cv2.FONT_HERSHEY_COMPLEX_SMALL,
    #                                                     1, (0, 0, 255), thickness=1, lineType=2)
    #                     else:
    #                         print('Alignment Failure')
    #                 # c+=1
    #                 cv2.imshow('Video', frame)
    #
    #                 if cv2.waitKey(1) & 0xFF == ord('q'):
    #                     break
    #
    #             video_capture.release()
    #             cv2.destroyAllWindows()

if __name__ == "__main__":
    app1 = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app1.exec_())
