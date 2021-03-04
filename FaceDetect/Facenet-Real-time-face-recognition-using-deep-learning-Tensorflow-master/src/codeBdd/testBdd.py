import glob
from src.codeBdd.interroBdd import *
from src.codeBdd.Client import *


if __name__ == "__main__":
# def M():
# Ici ça créer la BDD et une première table avec toutes les images + le chemin
    M = Interro('Clients','Clients')
    M.creation()
    M.ajoutColonne('Nom','TEXT','nomClient')
    M.ajoutColonne('Prenom','TEXT','prenomClient')
    M.ajoutColonne('Path','TEXT','Oui')
    M.ajoutColonne('Dette','INTEGER', 0.0)
    M.ajoutColonne('tauxAlcool','INTEGER', 0.0)

    print("la bdd a été créée") #test

    i=1
    # list = glob.glob('/home/bourgeat/Documents/S3/projet/Partie 1 reco/Facenet-Real-time-face-recognition-using-deep-learning-Tensorflow-master/Facenet-Real-time-face-recognition-using-deep-learning-Tensorflow-master/train_img/*')
    list = glob.glob('./train_img/*')

    for x in list:
        client = Client(x)

        #Mise à jour du nom du client
        M.insertion(i,'Nom',0.0)
        # print("nom", i, " : ", client.nom)
        M.update(i,'Nom',client.nom)

        # print("client.nom / type(client.nom) :",client.nom,"/",type(client.nom))  # renvoit nom / str
        # print("int(client.nom) / type(int(client.nom)) :",int(client.nom),"/",type(int(client.nom)))

        print("nom ",i," : ",M.gation_ID(i,'Nom'), type(M.gation_ID(i,'Nom')))

        #Mise à jour du prenom du client
        # M.insertion(i, 'Prenom', 0.0)
        # print("prenom", i, " : ", client.prenom)
        M.update(i,'Prenom',client.prenom)
        print("prenom ",i," : ",M.gation_ID(i,'Prenom'), type(M.gation_ID(i,'Prenom')))

        #Mise à jour du path du client
        # M.insertion(i, 'Path', 0.0)
        # print("path", i, " : ", x)
        M.update(i,'Path',x)
        print("path ",i," : ",M.gation_ID(i,'Path'), type(M.gation_ID(i,'Path')))

        #Mise à jour de la dette du client
        # M.insertion(i, 'Dette', 0.0)
        # print("dette", i, " : ", client.dette)

        # print("client.dette / type(client.dette) :",client.dette,"/",type(client.dette)) #renvoit 0 / int
        # print("int(client.dette) / type(int(client.dette)) :",int(client.dette),"/",type(int(client.dette)))

        M.update(i,'Dette',int(client.dette))
        print("dette ",i," : ",M.gation_ID(i,'Dette'), type(M.gation_ID(i,'Dette')))

        #Mise à jour du taux d'alcoolémie du client
        # M.insertion(i, 'tauxAlcool', 0.0)
        # print("tauxAlcool", i, " : ", client.tauxAlcool)
        M.update(i,'tauxAlcool',int(client.tauxAlcool))
        print("tauxAlcool ",i," : ",M.gation_ID(i,'tauxAlcool'), type(M.gation_ID(i,'tauxAlcool')))

        i+=1


    print("la bdd a été mise  jour") #test

    #tests des fcts
    M.update(1,'Dette',45)
    M.update(2,'Dette',74)
    M.update(3,'Dette',99)
    M.update(4,'Dette',50000)
    M.update(5,'Dette',0.5)

    M.update(1, 'tauxAlcool', 0.1)
    M.update(2, 'tauxAlcool', 0.55)
    M.update(3, 'tauxAlcool', 3)
    M.update(4, 'tauxAlcool', 89)
    M.update(5, 'tauxAlcool', 1.6)


    print("\n----------------- NOUVEAUX TESTS -----------------------------------")
    #print('Sunny Deol a une dette de : ', M.gation_ID(M.gation_index('Sunny', 'Nom'),'Dette'))
    #print("Sunny Deol a un taux d'alcoolemie de : ", M.gation_ID(M.gation_index('Sunny', 'Nom'), 'tauxAlcool'))

    # return M





