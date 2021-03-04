import sqlite3


class Bdd():
    def __init__(self, nom_BDD, nom_table):
        self.nomBDD = nom_BDD
        self.nom_table = nom_table
        self.dict_col = {'Nom': 'ID', 'Type': 'INTEGER'}
        self.listingCol = [self.dict_col]
        # Ici c'est la classe mère, pourvue d'une méthode pour initialiser
        # la création de la BDD et créer les différentes tables.

    def creation(self):
        """c'est la méthode qui sert à créer la BDD et à ajouter
        une table ou à juste ajouter une table à une BDD existante
        """
        conn = sqlite3.connect(self.nomBDD)
        c = conn.cursor()
        c.execute('CREATE TABLE {tn} ({nf} {ft})' \
                  .format(tn=self.nom_table, nf=self.dict_col['Nom'], ft=self.dict_col['Type']))
        conn.commit()
        conn.close()


class modifBDD(Bdd):
    def __init__(self, nom_BDD, nom_table):
        super().__init__(nom_BDD, nom_table)
        self.nmbrNewCol = 1

        # Cette classe hérite de BDD, elle sert à ajouter dans une table des colonnes, à les initialiser et à en
        # modifier les valeurs

    def ajoutColonne(self, nom, type, def_val=0.0):
        """ Ajoute des colonnes ayant un nom, un type SQL, et une valeur par défaut
        """
        conn = sqlite3.connect(self.nomBDD)
        c = conn.cursor()
        c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct} DEFAULT '{df}'". \
                  format(tn=self.nom_table, cn=str(nom), ct=str(type), df=def_val))
        conn.commit()
        conn.close()
        self.dict_col['Nom' + str(self.nmbrNewCol)] = str(nom)
        self.dict_col['Type' + str(self.nmbrNewCol)] = str(type)
        self.nmbrNewCol += 1

    def insertion(self, IDentifiant, Colonne, Val):
        """Initialise une entrée (caractérisé par son ID) dans la colonne
        Colonne avec la valeur Val
        """
        conn = sqlite3.connect(self.nomBDD)
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO {tn} ({idf}, {cn}) VALUES ({id}, {val})".\
                  format(tn=self.nom_table, idf='ID', cn=Colonne, id=IDentifiant, val=Val))
        conn.commit()
        conn.close()

    def update(self, IDentifiant, Colonne, Val):
        """ Sert à modifier la valeur d'une colonne pour un
        identifiant donné déjà initialisé
        """
        conn = sqlite3.connect(self.nomBDD)
        c = conn.cursor()
        if type(Val) == float:
            c.execute('''UPDATE {tn}
                      SET {cln}=({val})
                      WHERE {idf}={id}'''. \
                      format(tn=self.nom_table, cln=str(Colonne), val=float(Val), idf='ID', id=int(IDentifiant)))
        elif type(Val) == int:
            c.execute('''UPDATE {tn}
                        SET {cln}=({val})
                        WHERE {idf}={id}'''. \
                      format(tn=self.nom_table, cln=str(Colonne), val=int(Val), idf='ID', id=int(IDentifiant)))
        else:
            c.execute('''UPDATE {tn}
                         SET {cln}=('{val}')
                         WHERE {idf}={id}'''. \
                      format(tn=self.nom_table, cln=str(Colonne), val=(Val), idf='ID', id=int(IDentifiant)))
        conn.commit()
        conn.close()
