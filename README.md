# SysPort2020


**FaceDetect** contient les codes destinés à tourner sur l'ordinateur (serveur web et IA).

**SysPortApp** contient le code de l'application Android.


------------------------------- **PARTIE I : PRE-REQUIS** --------------------------

Installer Python 3
Installer les bibliothèques Python Tensorflow2, OpenCV, et Flask.
Pour chacune d'elle saisir dans un terminal la commande : pip install nom_bibliothèque

Il faut aussi installer Android Studio pour pouvoir compiler l'application sur un téléphone après l'avoir branché à l'ordinateur.


-------------------- **PARTIE II : DESCRIPTION DES REPERTOIRES** -------------------------

Répertoires:
	FaceDetect :
		Contient les codes Python dédiés à l'ordinateur


	SysPortApp :
		Contient le codes de l'application Android


Description du sous-répertoire "FaceDetect" :
	Facenet-Real-time-face-recognition-using-deep-learning-Tensorflow-master :
		Contient les codes de l'IA utilisant Tensorflow.
		C'est celui qu'on a le plus utilisé durant le projet et pour les démonstrations.


	Face-Rec-Caffe :
		Contient les codes de l'IA utilisant Caffe


-------------------- **PARTIE III : CODES PYTHON** -----------------------------------

Dans la suite on suppose qu'on se trouve dans le répertoire:
	Facenet-Real-time-face-recognition-using-deep-learning-Tensorflow-master\src\codeReconnaissance

--------- Ajout de photos d'une nouvelle personne avant entrainement:
- Ouvrir le script auto_build_face_dataset.py
- A la ligne 9, remplacer "new_person_name" par le prénom et le nom de la personne:
	args = {"output": "train_img/new_person_name", "detector": "face_detection_model", "confidence": 0.5}
- Dans la table "Clients" de la BDD, il faut renseigner les consommations de la nouvelle personne

--------- Entrainement du model:
- Vider le contenu du répertoire "pre_img"
- Exécuter successivement les scrips :
	"data_preprocess.py", "train_main.py"

--------- Lancement du serveur:
On a deux possibilités :
- soit exécuter le script "serveur_web"
- ou soit exécuter le script "serveurGUI" qui ouvre une interface, puis démarrer le serveur en cliquant sur "connect"

Le serveur se charge de lancer le programme de reconnaissance (identify_face_video.identify_on_video) lorsqu'il recoit la requête correspondante à startCamera.


-------------------- **PARTIE IV : FONCTIONNEMENT** -----------------------------------

1- Lancer le serveur

2- Saisir l'adresse du serveur sur le téléphone et lancer. 

-------------------- **PARTIE V : CONFIGURATION ANDROID STUDIO** -----------------------------------

1- Installer/mettre à jour la version 4.1.1 ou 4.1.2 d'Android Studio

2- Lancer Android Studio et cliquer sur Configure -> SDK Manager
	1- Dans l'onglet SDK Platforms, sélectionner Android 10 et télécharger
	2- Dans l'onglet SDK Tools, vérifier que "Android SDK Build-Tools" et "Android SDK Platform-tools" sont sélectionnés.
	   Les mettre à jours si possible.
	3- Revenir à l'acceuil d'android Studio.

3- Pour ouvrir le projet, cliquer sur "Open an Exixting Project" ou "Import Project".

4- Si l'erreur "Gradle project sync failed. Please fix your project and try again." apparait,
   suivre la démarche suivante:
	1- faire File -> Invalidate caches / Restart
	2- Fermer Android Studio
	3- Supprimer le répertoire .gradle qui se trouve votre répertoire utilisateur (exemple: C:\Users\Abdel) 
	4- Redémarrer Android Studio, vous verez normalement qu'il télécharge gradle en arrière plan. Attendre
	   que le téléchargement se termine.
	5- Cliquer sur Build au bas de l'écran et voir s'il n'y a pas d'erreur de synchronisation.
  
5- S'il n'y a pas d'erreur de synchro, se rendre dans le fichier build.gradle(Project: SysportApp) accessible dans la section Gradle Scripts.
   Voir s'il n'y a pas des changements de version qui sont suggérés. Si oui, appliquer ces changements.
   A la fin des changements, cliquer sur "Sync now" qui apparaitra quelque part sur l'écran.

6- Compilation sur un téléphone Android
	1- Pour autoriser le débogage sur votre téléphone, rendez-vous sur le lien suivant:
		https://developer.android.com/studio/debug/dev-options
	2- Si vous êtes sur Windows, vous aurez besoin d'installer un driver pour autoriser le débogage via USB:
		https://developer.android.com/studio/run/oem-usb
 	3- Connectez le téléphone Android via un cable USB, une notification doit normalement apparaitre sur l'écran du téléphone.
	   Cocher la case "Toujours autorisé".
	   Le nom du téléphone doit apparaitre dans la liste des appareils.
	4- Sélectionnez votre appareil et compilez.

	5- Lors d'une première installation, se rendre dans les paramètres du téléphone et accorder les autorisations d'accès à l'appareil photo.
