from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import os
import pickle

import cv2
import numpy as np
import tensorflow as tf
from PIL import Image
from threading import Thread
from multiprocessing.dummy import Pool, Process

from src.codeBdd import interroBdd
from src.codeReconnaissance import detect_face, facenet
import serveur_web

video_source = ""

bdd = interroBdd.Interro('Clients', 'Clients')
modeldir = './model/20170511-185253.pb'
classifier_filename = './class/classifier.pkl'
npy = './npy'
train_img = './train_img'
liste_json = []
HumanNames = os.listdir(train_img)
HumanNames.sort()
frame_interval = 3
minsize = 20  # minimum size of face
threshold = [0.6, 0.7, 0.7]  # three steps's threshold
factor = 0.709  # scale factor
margin = 44
nb_frames_with_face = 3
batch_size = 1000
image_size = 182
input_image_size = 160
names = []
c = 0

tf.compat.v1.disable_eager_execution()

with tf.Graph().as_default():
    gpu_options = tf.compat.v1.GPUOptions(per_process_gpu_memory_fraction=0.6)
sess = tf.compat.v1.Session(config=tf.compat.v1.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
with sess.as_default():
    pnet, rnet, onet = detect_face.create_mtcnn(sess, npy)

    print('Loading Model')
    facenet.load_model(modeldir)
    images_placeholder = tf.compat.v1.get_default_graph().get_tensor_by_name("input:0")
    embeddings = tf.compat.v1.get_default_graph().get_tensor_by_name("embeddings:0")
    phase_train_placeholder = tf.compat.v1.get_default_graph().get_tensor_by_name("phase_train:0")
    embedding_size = embeddings.get_shape()[1]

    classifier_filename_exp = os.path.expanduser(classifier_filename)
    with open(classifier_filename_exp, 'rb') as infile:
        (model, class_names) = pickle.load(infile)


def identify_on_video():
    """
    Programme de reconnaissance faciale sur vidéo.
    :return: None.
    """
    input_video = 'rtsp://' + str(video_source) + ':1234/'

    with sess.as_default():
        video_capture = cv2.VideoCapture(input_video)
        ready_to_detect_identity = True

        print('Start Recognition')
        prevTime = 0
        while True:
            ret, frame = video_capture.read()
            if not ret:
                break

            if ready_to_detect_identity:
                ### S'il n'y a pas déjà une image en cours de traitement, alors on traite la nouvelle image
                ready_to_detect_identity = False
                pool = Pool(processes=1)
                frame, ready_to_detect_identity = pool.apply_async(recognize_image, [frame, embedding_size, images_placeholder, embeddings, phase_train_placeholder, sess, model, pnet, rnet, onet]).get()
                pool.close()

            # c+=1
            cv2.imshow('Video', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        video_capture.release()
        cv2.destroyAllWindows()

        # à la fin on efface le contenu du fichier information.json
        liste_json = []
        # with open("../codeTransfert/information.json", "w") as write_file:
        with open("information.json", "w") as write_file:
            json.dump(liste_json, write_file)


def recognize_image(frame_1, embedding_size, images_placeholder, embeddings, phase_train_placeholder, sess, model, pnet, rnet, onet):
    """
    Traite une image pour reconnaitre les personnes q'elle contient.
    :return: image traitée
    """
    # rotate frame
    global names
    (h, w) = frame_1.shape[:2]
    (cX, cY) = (w // 2, h // 2)  # center of the frame

    # rotate our image by -90 degrees around the image
    M = cv2.getRotationMatrix2D((cX, cY), -90, 1.0)
    frame = cv2.warpAffine(frame_1, M, (w, h))

    frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)  # resize frame (optional)

    # curTime = time.time() + 1  # calc fps
    timeF = frame_interval

    if (c % timeF == 0):  # la détection est faite chaque timeF frame
        find_results = []

        if frame.ndim == 2:
            frame = facenet.to_rgb(frame)
        frame = frame[:, :, 0:3]
        bounding_boxes, _ = detect_face.detect_face(frame, minsize, pnet, rnet, onet, threshold, factor)
        nrof_faces = bounding_boxes.shape[0]

        if nrof_faces > 0:
            print('Detected_FaceNum: %d' % nrof_faces)
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

                # # print(best_class_probabilities)
                if best_class_probabilities > 0.6:
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

                            # on sauvegarde le nom dans une liste names
                            # si le nom apparait 2 fois sur 3 detections alors on le garde
                            # sinon ce n'est pas une bonne détection
                            if result_names in names:
                                names = []
                                cv2.putText(frame, result_names, (text_x, text_y), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                                            1, (0, 0, 255), thickness=1, lineType=2)
                                nom_prenom = H_i
                                nom = nom_prenom.split()[0]
                                prenom = nom_prenom.split()[1]

                                # écrire les données qui nous intéressent dans un fichier json pour ensuite les transmettre à l'application
                                # avec les coordonnees

                                t = Process(target=writeInformation, args=(nom, prenom, bb, liste_json, i))
                                t.start()
                            else:
                                names.append(result_names)
                                if len(names) >= 3:
                                    names = []

        else:
            # print('Alignment Failure')
            pass
    return frame, True


def addPerson(list_info, new_info):
    """
    Fonction pour la mise à jour de la liste des informations à renvoyer au téléphone.
    :param list_info: liste des informations
    :param new_info: nouvelle information

    :return: None
    """
    change = False
    info = {}
    indice = 0
    for indice, info in enumerate(list_info):
        if info["nom"] == new_info["nom"] and info["prenom"] == new_info["prenom"]:
            change = True
            break
    if change:
        list_info.remove(info)
        list_info.insert(indice, new_info)
    else:
        list_info.append(new_info)
    return


def writeInformation(nom, prenom, bb, liste_json, i):
    """
    Ecrit les données recueillies dans le fichier information.json.
    :return:
    """
    # écrire les données qui nous intéressent dans un fichier json pour ensuite les transmettre à l'application
    # avec les coordonnees
    data = {"nom": nom, "prenom": prenom,
            "dette": bdd.gation_ID(bdd.gation_index('\"%s\"' % (nom), 'Nom'), 'Dette'),
            "tauxAlcool": bdd.gation_ID(bdd.gation_index('\"%s\"' % (nom), 'Nom'),
                                        'tauxAlcool'),
            "x": int(bb[i][0]),
            "y": int(bb[i][3])}

    # pour éviter d'ajouter 2 fois la même personne dans la liste de dictionnaires
    # on a créer une fonction pour l'ajout
    addPerson(liste_json, data)
    # with open("../codeTransfert/information.json", "w") as write_file:
    with open("information.json", "w") as write_file:
        json.dump(liste_json, write_file)

    return
