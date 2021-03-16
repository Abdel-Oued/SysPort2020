from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json

import tensorflow as tf
from scipy import misc
import cv2
import numpy as np
from src.codeReconnaissance import detect_face, facenet
import os
import time
import pickle
from PIL import Image
import glob

from src.codeBdd import interroBdd
from src.codeBdd import Client

M = interroBdd.Interro('Clients', 'Clients')
# M.creation()
# M.ajoutColonne('Nom', 'TEXT', 'nomClient')
# M.ajoutColonne('Prenom', 'TEXT', 'prenomClient')
# M.ajoutColonne('Path', 'TEXT', 'Oui')
# M.ajoutColonne('Dette', 'INTEGER', 0.0)
# M.ajoutColonne('tauxAlcool', 'INTEGER', 0.0)

# print("la bdd a été créée")  # test
#
# i = 1
# list = glob.glob('../../train_img/*')
# for x in list:
#     client = Client(x)
#
#     # Mise à jour du nom du client
#     M.insertion(i, 'Nom', 0.0)
#     # print("nom", i, " : ", client.nom)
#     M.update(i, 'Nom', client.nom)
#
#     # print("client.nom / type(client.nom) :",client.nom,"/",type(client.nom))  # renvoit nom / str
#     # print("int(client.nom) / type(int(client.nom)) :",int(client.nom),"/",type(int(client.nom)))
#
#     # print("nom ",i," : ",M.gation_ID(i,'Nom'), type(M.gation_ID(i,'Nom')))
#
#     # Mise à jour du prenom du client
#     # M.insertion(i, 'Prenom', 0.0)
#     # print("prenom", i, " : ", client.prenom)
#     M.update(i, 'Prenom', client.prenom)
#     # print("prenom ",i," : ",M.gation_ID(i,'Prenom'), type(M.gation_ID(i,'Prenom')))
#
#     # Mise à jour du path du client
#     # M.insertion(i, 'Path', 0.0)
#     # print("path", i, " : ", x)
#     M.update(i, 'Path', x)
#     # print("path ",i," : ",M.gation_ID(i,'Path'), type(M.gation_ID(i,'Path')))
#
#     # Mise à jour de la dette du client
#     # M.insertion(i, 'Dette', 0.0)
#     # print("dette", i, " : ", client.dette)
#
#     # print("client.dette / type(client.dette) :",client.dette,"/",type(client.dette)) #renvoit 0 / int
#     # print("int(client.dette) / type(int(client.dette)) :",int(client.dette),"/",type(int(client.dette)))
#
#     M.update(i, 'Dette', int(client.dette))
#     # print("dette ",i," : ",M.gation_ID(i,'Dette'), type(M.gation_ID(i,'Dette')))
#
#     # Mise à jour du taux d'alcoolémie du client
#     # M.insertion(i, 'tauxAlcool', 0.0)
#     # print("tauxAlcool", i, " : ", client.tauxAlcool)
#     M.update(i, 'tauxAlcool', int(client.tauxAlcool))
#     # print("tauxAlcool ",i," : ",M.gation_ID(i,'tauxAlcool'), type(M.gation_ID(i,'tauxAlcool')))
#
#     i += 1
#
# print("la bdd a été mise  jour")  # test
#
# # tests des fcts
# M.update(1, 'Dette', 45)
# M.update(2, 'Dette', 74)
# M.update(3, 'Dette', 99)
# M.update(4, 'Dette', 50000)
# M.update(5, 'Dette', 0.5)
#
# M.update(1, 'tauxAlcool', 0.1)
# M.update(2, 'tauxAlcool', 0.55)
# M.update(3, 'tauxAlcool', 3)
# M.update(4, 'tauxAlcool', 89)
# M.update(5, 'tauxAlcool', 1.6)

# print("\n----------------- NOUVEAUX TESTS -----------------------------------")
# print('Sunny Deol a une dette de : ', M.gation_ID(M.gation_index('Sunny', 'Nom'),'Dette'))
# print("Sunny Deol a un taux d'alcoolemie de : ", M.gation_ID(M.gation_index('Sunny', 'Nom'), 'tauxAlcool'))

input_video = "akshay_mov.mp4"
modeldir = './model/20170511-185253.pb'
classifier_filename = './class/classifier.pkl'
npy = './npy'
train_img = "./train_img"

liste_json = []

with tf.Graph().as_default():
    gpu_options = tf.compat.v1.GPUOptions(per_process_gpu_memory_fraction=0.6)
    sess = tf.compat.v1.Session(config=tf.compat.v1.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
    with sess.as_default():
        pnet, rnet, onet = detect_face.create_mtcnn(sess, npy)

        minsize = 20  # minimum size of face
        threshold = [0.6, 0.7, 0.7]  # three steps's threshold
        factor = 0.709  # scale factor
        margin = 44
        frame_interval = 3
        batch_size = 1000
        image_size = 182
        input_image_size = 160

        HumanNames = os.listdir(train_img)
        HumanNames.sort()

        print('Loading Modal')
        facenet.load_model(modeldir)
        images_placeholder = tf.compat.v1.get_default_graph().get_tensor_by_name("input:0")
        embeddings = tf.compat.v1.get_default_graph().get_tensor_by_name("embeddings:0")
        phase_train_placeholder = tf.compat.v1.get_default_graph().get_tensor_by_name("phase_train:0")
        embedding_size = embeddings.get_shape()[1]

        classifier_filename_exp = os.path.expanduser(classifier_filename)
        with open(classifier_filename_exp, 'rb') as infile:
            (model, class_names) = pickle.load(infile)

        video_capture = cv2.VideoCapture('rtsp://192.168.8.5:1234/')#input_video)
        c = 0 #

        print('Start Recognition')
        prevTime = 0
        while True:
            ret, frame = video_capture.read()

            frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)  # resize frame (optional)

            curTime = time.time() + 1  # calc fps
            timeF = frame_interval


            if (c % timeF == 0):  # la détection est faite chaque timeF frame
                find_results = []

                if frame.ndim == 2:
                    frame = facenet.to_rgb(frame)
                frame = frame[:, :, 0:3]
                bounding_boxes, _ = detect_face.detect_face(frame, minsize, pnet, rnet, onet, threshold, factor)
                nrof_faces = bounding_boxes.shape[0]
                print('Detected_FaceNum: %d' % nrof_faces)

                if nrof_faces > 0:
                    det = bounding_boxes[:, 0:4]
                    img_size = np.asarray(frame.shape)[0:2]

                    cropped = []
                    scaled = []
                    scaled_reshape = []
                    bb = np.zeros((nrof_faces, 4), dtype=np.int32)

                    for i in range(nrof_faces):
                        emb_array = np.zeros((1, embedding_size))

                        bb[i][0] = det[i][0]
                        bb[i][1] = det[i][1]
                        bb[i][2] = det[i][2]
                        bb[i][3] = det[i][3]

                        # inner exception
                        if bb[i][0] <= 0 or bb[i][1] <= 0 or bb[i][2] >= len(frame[0]) or bb[i][3] >= len(frame):
                            print('Face is very close!')
                            continue

                        cropped.append(frame[bb[i][1]:bb[i][3], bb[i][0]:bb[i][2], :])
                        cropped[i] = facenet.flip(cropped[i], False)
                        # scaled.append(misc.imresize(cropped[i], (image_size, image_size), interp='bilinear'))
                        scaled.append(
                            np.array(Image.fromarray(cropped[i]).resize((image_size, image_size), Image.BILINEAR)))
                        scaled[i] = cv2.resize(scaled[i], (input_image_size, input_image_size),
                                               interpolation=cv2.INTER_CUBIC)
                        scaled[i] = facenet.prewhiten(scaled[i])
                        scaled_reshape.append(scaled[i].reshape(-1, input_image_size, input_image_size, 3))
                        feed_dict = {images_placeholder: scaled_reshape[i], phase_train_placeholder: False}
                        emb_array[0, :] = sess.run(embeddings, feed_dict=feed_dict)
                        predictions = model.predict_proba(emb_array)
                        print(predictions)
                        best_class_indices = np.argmax(predictions, axis=1)
                        best_class_probabilities = predictions[np.arange(len(best_class_indices)), best_class_indices]
                        # print("predictions")
                        print(best_class_indices, ' with accuracy ', best_class_probabilities)

                        # definir un sueil de probabilite


                        # # print(best_class_probabilities)
                        if best_class_probabilities > 0.53:

                            nom_prenom = HumanNames[best_class_indices[0]]
                            nom = nom_prenom.split()[0]
                            prenom = nom_prenom.split()[1]

                            print("nom : ", nom)
                            print("taux d'alcool:", M.gation_ID(M.gation_index('\"%s\"' % (nom), 'Nom'), 'tauxAlcool'))
                            print("dette:", M.gation_ID(M.gation_index('\"%s\"' % (nom), 'Nom'), 'Dette'))

                            # écrire les données qui nous intéressent dans un fichier json pour ensuite les transmettre à l'application

                            data = {"nom": nom, "prenom": prenom,
                                    "dette": M.gation_ID(M.gation_index('\"%s\"' % (nom), 'Nom'), 'Dette'),
                                    "tauxAlcool": M.gation_ID(M.gation_index('\"%s\"' % (nom), 'Nom'), 'tauxAlcool')}
                            # ajouter les coordonnees

                            if data not in liste_json:  # pour éviter d'ajouter 2 fois la même personne dans la liste de dictionnaire
                                liste_json.append(data)
                            with open("../codeTransfert/information.json", "w") as write_file:
                                json.dump(liste_json, write_file)

                            cv2.rectangle(frame, (bb[i][0], bb[i][1]), (bb[i][2], bb[i][3]), (0, 255, 0),
                                          2)  # boxing face

                            # plot result idx under box
                            text_x = bb[i][0]
                            text_y = bb[i][3] + 20
                            print('Result Indices: ', best_class_indices[0])
                            print(HumanNames)

                            for H_i in HumanNames:
                                if HumanNames[best_class_indices[0]] == H_i:
                                    result_names = HumanNames[best_class_indices[0]]
                                    cv2.putText(frame, result_names, (text_x, text_y), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                                                1, (0, 0, 255), thickness=1, lineType=2)
                else:
                    print('Alignment Failure')
            # c+=1
            cv2.imshow('Video', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        video_capture.release()
        cv2.destroyAllWindows()
