import os


class Client():
    def __init__(self, path):
        print("------------------------------------------------------- Début des tests -----------------------------------------------------")
        self.path = path
        nom_prenom = os.path.basename(path)
        identifiant = []
        for x in nom_prenom.split(" "):
            identifiant.append(x)
        self.nom = identifiant[0]
        self.prenom = identifiant[1]
        self.dette = 0
        self.tauxAlcool = 0


    # @property
    # def nom(self):
    #     return self.nom

    # @nom.setter
    # def nom(self, nom):
    #     if not nom:
    #         self.nom = "Unknown"
    #     else:
    #         self.nom = nom

    # @property
    # def prenom(self):
    #     return self.prenom

    # @prenom.setter
    # def prenom(self, prenom):
    #     if not prenom:
    #         self.prenom = "Unknown"
    #     else:
    #         self.prenom = prenom

    # @property
    # def path(self):
    #     return self.path

    # @path.setter
    # def path(self, path):
    #     if not path:
    #         self.path = "Unknown"
    #     else:
    #         self.path = path

    # @property
    # def dette(self):
    #     return self.dette

    # @dette.setter
    # def dette(self, dette):
    #     if not dette:
    #         self.dette = 0
    #     else:
    #         self.dette = dette

    # @property
    # def tauxAlcool(self):
    #     return self.tauxAlcool

    # @tauxAlcool.setter
    # def tauxAlcool(self, tauxAlcool):
    #     if not tauxAlcool:
    #         self.tauxAlcool = 0
    #     else:
    #         self.tauxAlcool = tauxAlcool







