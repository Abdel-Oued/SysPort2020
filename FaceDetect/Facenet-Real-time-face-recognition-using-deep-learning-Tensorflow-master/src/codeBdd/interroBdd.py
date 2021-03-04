from src.codeBdd.creationBdd  import *


class Interro(modifBDD):

    # Hérite de modifBDD, sert à ressortir en console des valeurs des tables

    def __init__(self,nom_BDD,nom_table):
        super().__init__(nom_BDD,nom_table)



    def gation_ID(self,ID,Colonne):
        """"
        Cette fonction va renvoyer la valeur présente dans la colonne Colonne, pour l'entrée ayant l'id ID
        retourne une valeur de type string
        """
        conn = sqlite3.connect(self.nomBDD)
        c = conn.cursor()
        c.execute('SELECT {cn} FROM {tn} WHERE {idf}={ID}'.\
                  format(cn=str(Colonne),tn=self.nom_table,idf='ID', ID=ID))
        row = c.fetchone()
        # print(row[0], type(row[0]))
        c.close()
        conn.close()

        # return str(row)
        return str(row[0])



    def gation_index(self,val,Colonne):
        conn = sqlite3.connect(self.nomBDD)
        c = conn.cursor()
        # print(self.nom_table)
        # print(Colonne)
        # print(val)
        # c.execute("""SELECT ID FROM \"%s\" WHERE \"%s\"=%s"""%(self.nom_table,Colonne,val))
        c.execute('SELECT ID FROM {tn} WHERE {idf}={ID}'.format(tn=self.nom_table,idf=str(Colonne), ID=str(val)))
        # c.execute("""SELECT ID FROM \"%s\" WHERE ?=?"""%(self.nom_table),(Colonne,val))

        row=c.fetchone()
        # print(row[0])
        c.close()
        conn.close()
        #Cette fonction va renvoyer l'id ayant pour valeur val dans la colonne Colonne
        # return str(row)
        return str(row[0])


    #
    # def get_Colonne(self,val,Colonne):  #ilfaut rajouter une condition sur le nom
    #     conn = sqlite3.connect(self.nomBDD)
    #     c = conn.cursor()
    #     # c.execute('SELECT \"%s\" FROM \"%s\" WHERE \"%s\"=(SELECT ID FROM \"%s\" WHERE \"%s\"=\"%s\")'%(str(Colonne),self.nom_table,'ID',self.nom_table,Colonne,val))
    #     # c.execute("""SELECT \"%s\" FROM \"%s\" WHERE 'Nom' = \"%s\""""%(str(Colonne),self.nom_table,nom))
    #     c.execute("""SELECT \"%s\" FROM \"%s\" WHERE Nom = \"%s\""""%(str(Colonne),self.nom_table,val))
    #
    #     row = c.fetchone()
    #     # print(row)
    #     conn.close()
    #     # print(str(row[0]))
    #     return str(row[0])
    #

    def get_Colonne(self,nom,Colonne):  #ilfaut rajouter une condition sur le nom
    # def get_Colonne(self,Colonne):  # ilfaut rajouter une condition sur le nom

        conn = sqlite3.connect(self.nomBDD)
        c = conn.cursor()
        # c.execute('SELECT \"%s\" FROM \"%s\" WHERE \"%s\"=(SELECT ID FROM \"%s\" WHERE \"%s\"=\"%s\")'%(str(Colonne),self.nom_table,'ID',self.nom_table,Colonne,val))
        c.execute("""SELECT \"%s\" FROM \"%s\" WHERE 'Nom' = \"%s\""""%(str(Colonne),self.nom_table,str(nom)))
        # c.execute("""SELECT \"%s\" FROM \"%s\""""%(str(Colonne),self.nom_table))

        row = c.fetchone()
        # print(row)
        conn.close()
        # print(str(row[0]))
        return str(row[0])


    def getDette(self,nom):
        conn = sqlite3.connect(self.nomBDD)
        c = conn.cursor()
        c.execute(""" SELECT Dette FROM \"%s\" WHERE ID=(SELECT ID FROM \"%s\" WHERE Nom = \"%s\")"""%(self.nom_table,self.nom_table,nom))
        row = c.fetchone()
        conn.close()
        return str(row[0])




