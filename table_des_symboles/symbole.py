import sys

class variable:

    def __init__(self, name, type_entree="None", mode="in", value = None, size=0, Dimension=0, ligne_declaration=None, ligne_utilisation=None, address=None, parametre = 0):
        self.name = name
        self.type = type_entree
        self.value = value
        self.size = size
        self.Dimension = Dimension
        self.ligne_declaration = ligne_declaration
        self.ligne_utilisation  = ligne_utilisation
        self.address = address
        self.mode = mode
        self.parametre = parametre
        #Ajouter l'offset

    def __repr__(self):
        return f"variable({self.name},{self.type},{self.mode},{self.value},{self.size},{self.Dimension},{self.ligne_declaration},{self.ligne_utilisation},{self.address},{self.parametre})"
        """
        sys.stdout.write("\t\tType: " + str(self.type_entree))
        sys.stdout.write("\t\tTaille: " + str(self.Dimension))
        sys.stdout.write("\t\tDimension: " + str(self.ligne_declaration))
        sys.stdout.write("\t\tLigne de déclaration: " + self.name)
        utilisation_str = ""
        if len(self.ligne_utilisation)>1:
            for ligne in self.ligne_utilisation:
                utilisation_str += ligne
            sys.stdout.write("\t\tLignes d'utilisation: " + str(utilisation_str))
        sys.stdout.write("\t\tLigne d'utilisation: " + str(self.ligne_utilisation[0]))
        sys.stdout.write("Adresse mémoire: " + str(self.address))
        return repr
        """

class fonction:

    def __init__(self, name, parametres = {}, var_de_retour = {}, size=0, Dimension=0, ligne_declaration=None, ligne_utilisation=None, address=None):
        self.name = name
        self.parametres = parametres
        self.var_de_retour = var_de_retour
        self.size = size
        self.Dimension = Dimension
        self.ligne_declaration = ligne_declaration
        self.ligne_utilisation  = ligne_utilisation
        self.address = address

    def __repr__(self):
        return "function name:  " + self.name

    def __str__(self):
        return f"fonction({self.name}): {self.__repr__()}"
        """
        if len(self.parametres)>1:
            parametres_str = ""
            for element in self.parametres:
                parametres_str+= (self.parametres + ", ")
        sys.stdout.write("\t\tParamètres: " + parametres_str)
        sys.stdout.write('Retour: ' + self.retour)
        sys.stdout.write("\t\tTaille: " + str(self.Dimension))
        sys.stdout.write("\t\tDimension: " + str(self.ligne_declaration))
        sys.stdout.write("\t\tLigne de déclaration: " + self.name)
        utilisation_str = ""
        if len(self.ligne_utilisation)>1:
            for ligne in self.ligne_utilisation:
                utilisation_str += ligne
            sys.stdout.write("\t\tLignes d'utilisation: " + str(utilisation_str))
        sys.stdout.write("\t\tLigne d'utilisation: " + str(self.ligne_utilisation[0]))
        sys.stdout.write("Adresse mémoire: " + str(self.address))
        return repr
        """

class procedure:

    def __init__(self, name, parametres = {}, size=0, Dimension=0, ligne_declaration=None, ligne_utilisation=None, address=None):
        self.name = name
        self.parametres = parametres
        self.size = size
        self.Dimension = Dimension                                     
        self.ligne_declaration = ligne_declaration
        self.ligne_utilisation  = ligne_utilisation
        self.address = address

    def __repr__(self):
        return f"procedure({self.name}) : self.{self.parametres}"
        sys.stdout.write("\n\t => PROCEDURE\n")
        sys.stdout.write("\t\tNom: " + str(self.name))
        if len(self.parametres)>1:
            parametres_str = ""
            for element in self.parametres:
                parametres_str+= (self.parametres + ", ")
        sys.stdout.write("\t\tParamètres: " + parametres_str)
        sys.stdout.write("\t\tTaille: " + str(self.Dimension))
        sys.stdout.write("\t\tDimension: " + str(self.ligne_declaration))
        sys.stdout.write("\t\tLigne de déclaration: " + self.name)
        utilisation_str = ""
        if len(self.ligne_utilisation)>1:
            for ligne in self.ligne_utilisation:
                utilisation_str += ligne
            sys.stdout.write("\t\tLignes d'utilisation: " + str(utilisation_str))
        sys.stdout.write("\t\tLigne d'utilisation: " + str(self.ligne_utilisation[0]))
        sys.stdout.write("Adresse mémoire: " + str(self.address))
