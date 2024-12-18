from copy import deepcopy
import table_des_symboles as table_des_symboles
import table_des_symboles.symbole

#Fichier contenant les controles sémantiques à faire lors de la fabrication de la TDS


#Fonctions pour la TDS
def getBloc(tds, pile):
    current_node = tds
    for element in pile:
        current_node = current_node[element]
    return current_node

# Retourne l'occurence de la variable (la déclaration la plus récente, si il y a en a plusieurs), None si la variable n'existe pas
def getVar(tds, pile, variable_name):
    current_node = getBloc(tds, pile)
    for element in current_node:
        if element == variable_name:
            return current_node[element]
    return None

# Retourne la valeur correspondant au nom de la variable indiquée, si la variable n'est pas déclaré retourne None
def getValue(tds, pile, variable_name):
    variable = getVar(tds, pile, variable_name)
    if variable != None:
        return variable.value
    return None

# Retourne les paramètres correspondant au nom de la fonction donnée en entrée, none si la fonction n'héxiste pas
def getParams(tds, pile, fonction_name):
    fonction = getVar(tds, pile, fonction_name)
    if fonction != None:
        return fonction.parametres
    return None

# Fonction qui retourne le type de la variable sous le bon format pour les comparer (Integer, Char, ...), permet de comparer avec le type renvoyer par la fonction type() qui sont de la forme <class 'int'>, <class 'str'>, ...
def getType(variable_name):
    if type(variable_name) == int:
        return "integer"
    if type(variable_name) == str:
        return "char" # A modifier pour distinguer les chaines de caractères des string (python considère un caractère comme une chaine de caractère de taille 1 donc str)
    if type(variable_name) == float:
        return "float"
    if type(variable_name) == bool:
        return "boolean"
 



# Controles sémantiques pour les variables

#Controle de l'imbrication des variables (si la variable a été déclarée dans le bloc courant ou dans un bloc parent avant d'être initialisée)
def variableImbricationControl(pile_originale, tds, variable):
    pile = deepcopy(pile_originale)
    while (pile) :
        var = getVar(tds, pile, variable)
        if (type(var) == table_des_symboles.symbole.variable):
            if var.parametre == 2 :
                print ("\tErreur de sémantique: la variable de boucle for ne peut pas être affecté à l'intérieur de la boucle")
            return True
        else :
            pile.pop()
    return (pile!=[])

#Return la var dans le parents le plus proche
def getParentsVar(pile_originale, tds, variable):
    pile = deepcopy(pile_originale)
    while (pile) :
        if (getVar(tds, pile, variable)!=None):
            return getVar(tds, pile, variable)
        else :
            pile.pop()
    return None

#Controle de l'affectation des variables (si la variable a été initialisée dans le bloc courant ou dans un bloc parent avant d'être utilisée)
def variableAffectationControl(pile_originale, tds, variable):
    pile = deepcopy(pile_originale)
    while (pile) :
        var = getVar(tds, pile, variable)
        if type(var) == table_des_symboles.symbole.variable and var.parametre == 1 : # Si c'est un paramètre de fonction on peut l'utiliser dans la fonction sans l'avoir initialisée
            return True
        elif type(var) == table_des_symboles.symbole.variable and var.value != None : # La variable a été initialisée
            return True
        else :
            pile.pop()
    return False


# Controle de la résolution de type entre variable = VALEUR (si la variable a été déclarée avec un type et que la valeur affectée est du même type) 
def valueTypeControl(pile_originale, tds, variable_name, value):
    pile = deepcopy(pile_originale)
    while (pile[-1][:4]=='else' or pile[-1][:5]=='elsif' or pile[-1][:2]=='if' or pile[-1][:3]=='for' or pile[-1][:5]=='while'):
        pile.pop()
    variable = getVar(tds, pile, variable_name)
    if variable != None:
        return variable.type == getType(value)
    
    return False

# Controle de la résolution de type entre variable = VALEUR (si la variable a été déclarée avec un type et que la valeur affectée est du même type) 
def valueIsTypeControl(pile_originale, tds, type, value):
    pile = deepcopy(pile_originale)
    while (pile[-1][:4]=='else' or pile[-1][:5]=='elsif' or pile[-1][:2]=='if' or pile[-1][:3]=='for' or pile[-1][:5]=='while'):
        pile.pop()
    variable = getVar(tds, pile, type)
    if variable != None:
        return variable.type == getType(value)
    
    return False

# Controle de la résolution type entre Variable = VARIABLE (si la variable a été déclarée avec un type et que la variable affectée est du même type)
def variableTypeControl(pile_originale, tds, variable_gauche_name, variable_droite_name):
    pile = deepcopy(pile_originale)
    while (pile[-1][:4]=='else' or pile[-1][:5]=='elsif' or pile[-1][:2]=='if' or pile[-1][:3]=='for' or pile[-1][:5]=='while'):
        pile.pop()
    variable_gauche = getVar(tds, pile, variable_gauche_name)
    variable_droite = getVar(tds, pile, variable_droite_name)
    if variable_gauche != None and variable_droite != None:
        return variable_gauche.type == variable_droite.type
    return False


# Retourne l'occurence de la fonction (la déclaration la plus récente, si il y a en a plusieurs), None si la fonction n'existe pas
def getFunction(tds, pile, fonction_name):
    current_node = getBloc(tds, pile)
    for element in current_node:
        if element == fonction_name:
            return current_node[element]
    return None

# Controle de la résolutio type entre Variable = FONCTION (si la variable a été déclarée avec un type et que la fonction affectée est du même type)
def returnTypeControl(pile_originale, tds, tds_data, variable_gauche_name,fonction_name):
    pile = deepcopy(pile_originale)
    while (pile[-1][:4]=='else' or pile[-1][:5]=='elsif' or pile[-1][:2]=='if' or pile[-1][:3]=='for' or pile[-1][:5]=='while'):
        pile.pop()
    variable_gauche = getVar(tds, pile, variable_gauche_name)
    fonction = getFunction(tds, pile, fonction_name)
    if variable_gauche != None and fonction != None:
        for i in tds_data[fonction_name].var_de_retour:
            if variable_gauche.type == i.type:
                return True
    if fonction == None:
        print("Erreur de sémantique : la fonction ", fonction_name, " n'a pas été déclarée")
    return False


#Controls sémantiques pour les fonctions"

#Controle de l'imbrication des fonctions
#(si la fonction a été déclarée dans le bloc courant ou dans un bloc parent avant d'être utilisée)
def fonctionImbricationControl(pile_originale, tds, fonction):
    pile = deepcopy(pile_originale)
    while (pile) :
        if (getVar(tds, pile, fonction)!= None):
            return True
        else :
            pile.pop()
    return False

#Controle du nombre de paramètres lors de l'appel à une fonction
def fonctionParamControl(pile_originale, tds, fonction, params):
    pile = deepcopy(pile_originale)
    while (pile) :
        fonct = getVar(tds, pile, fonction)
        if fonct != None:
            if len(params) == len(fonct.parametres):
                return True
        else :
            pile.pop()
    return False


# Controle de la résolution type - valeur des paramètres (si les paramètres ont été déclarés avec un type et que la valeur affectée est du même type)
def fonctionParamTypeControl(pile_originale,tds, fonction, params, tds_data):
    pile = deepcopy(pile_originale)
  
    func = getFunction(tds, pile, fonction.name)
    
    k= 0
    rep = 1
    func.popitem()
    for i in func:
        var_param = tds_data[i].type # On récupère la variable correspondant à la definition de la fonction

        if params[k][0] == 4 and var_param == "integer":
            k = k + 1
        else:
            k = k + 1
            rep = 0
    return rep


# Controle du type de retour de la fonction
#def fonctionReturnTypeControl(pile_originale, tds, fonction, type_retour):
    


#Vérification spécifique en Ada

#Vérification de la déclaration de procédure ou de fonction
#dans une déclaration de procédure ou de fonction, si un identificateur suit le mot clé end, alors celui-ci doit être
#identique au nom de la procédure ou de la fonction déclarée.


   
    
#Vérification des déclarations
#toutes les déclarations d'un même niveau doivent porter des noms diérents. La seule exception est celle d'un
#type enregistrement déclaré, puis déni plus loin (il faut donc vérifier à la déclaration que le nom n'est pas déjà dans la TDS)
def declarationControl(pile_originale, tds, ident):
    pile = deepcopy(pile_originale)
    while (pile) :
        if getVar(tds, pile, ident):
            return False #si on trouve une variable avec le même nom, on renvoie False 
            #pour l'instant on ne peut pas vérifier si c'est un type enregistrement déclaré puis déni plus loin
        else :
            pile.pop()
    return True



#Vérification fin de fonction 
#l'exécution de toute fonction doit impérativement se terminer par une instruction return
def fonctionReturnControl(pile_originale, tds):
    pile = deepcopy(pile_originale)
    while (pile) :
        if getValue(tds, pile, "return") != None: 
            return True
        else :
            pile.pop()
    return False
#attention !
#ici on vérifie simplement qu'il y a un return on ne vérifie pas qu'il y a un paramètre de retour
#on ne vérifie pas non plus que le type du retour est le bon


#Vérification concernant le mode des paramètres
"""
-dans un appel de fonction ou de procédure, si un paramètre formel est déclaré in out, alors le paramètre effectif
correspondant doit être une valeur gauche, c'est à dire :
- soit une variable,
- soit une expression x.f avec x une variable de type enregistrement


- dans une fonction ou une procédure, si un paramètre formel x est déclaré in explicitement ou par défaut, alors sa
valeur ne peut pas être modifiée avec une affectation x := e. De la même façon, si x est de type enregistrement,
un champ de x ne peut pas être modifié avec une affectation x.f := e

"""
def paramInControl(pile_originale, tds, param):
    pile = deepcopy(pile_originale)
    while (pile) :
        if getVar(tds, pile, param) != None:
            mode = getVar(tds, pile, param).mode
            if mode == "in":
                return True
        else :
            pile.pop()
    return False
#on regarde si le paramètre est déclaré en in
#si c'est le cas on ne peut pas le modifier avec une affectation 
#donc si on a une affectation on renvoie False
#cela n'est valable que pour les paramètres de fonction ou de procédure et non pas pour les variables 
#il va falloir revoir un certain nombre de truc là je crois... 
