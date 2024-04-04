import table_des_symboles
import table_des_symboles.semantics_controls as sc

# Définition de la structure de l'arbre
class Node:
    def __init__(self, fct, children=None, value=None):
        """
        Initialise un nouveau nœud de l'arbre.

        :param type: Type de nœud (par exemple, 'Add', 'Subtract', 'Number', 'Identifier', etc.)
        :param children: Liste des nœuds enfants (sous-arbres).
        :param value: Valeur du nœud (utile pour les feuilles comme les nombres ou les identifiants).
        """
        self.fct = fct
        self.children = children if children is not None else []
        self.value = value

    def add_child(self, child):
        """
        Ajoute un enfant à ce nœud.

        :param child: Nœud enfant à ajouter.
        """
        self.children.append(child)

    def remove_child(self, child):
        """
        Supprime un enfant de ce nœud.

        :param child: Nœud enfant à supprimer.
        """
        self.children.remove(child)

    def __repr__(self):
        """
        Représentation textuelle pour le débogage.
        print(node) permet d'afficher l'arbre sous forme de texte.
        """
        return f"Node({self.fct}, children={self.children}, value={self.value})"

list_types = {"integer", "character", "string", "boolean", "access"}
catch_tokens = {(0,8) : "function", (0,18): "procedure", (0,5): "end", (0,2):"begin", (0,7):"for", (0,9):"loop", (0,27):"while"}


def inverser_enfants_arbre(node):
    if node.children:
        node.children.reverse()  # Inverser l'ordre des enfants du nœud courant
        for enfant in node.children:
            inverser_enfants_arbre(enfant)  # Répéter récursivement pour chaque enfant


# Fonction qui permet de dire si une chaines de caractères est un terminal ou non
def est_terminal(element):
    # Si l'élément de la pile est un tuple alors c'est un terminal ou que c'est "eof" alors c'est un terminal sinon si c'est une string alors c'est un non terminal
    if (type(element) == tuple) or (element == "eof"):
        return True
    else:
        return False

# début du parseur:
# L'analyseur prend en entrée la phrase (la liste de token) à identifier et la table d'analyse LL
# Pour réaliser l'analyse on crée une pile qui à l'initialisation contient l'axiome de la grammaire
# L'analyseur donne en sortie la liste des règles qui permettent de construire la phrase. Avec cette liste on va créer l'AST

def token_to_str(token, lexical_table):
    token_type, token_value, token_line = token
    token_str = lexical_table[token_type][token_value] if token_type in lexical_table else str(token_value)
    return f"{token_str}"

def highlight_error(token_str):
    RED = '\033[91m'
    END = '\033[0m'
    return f"{RED}{token_str}{END}"



def import_tds(token_lu, lexical_table, list_tokens, ind, tds):
    # On regarde si le token lu est dans la liste de token à repérer ou si c'est une variable
    if((token_lu[0], token_lu[1]) in catch_tokens or token_lu[0] == 3):
        
        # Lorsque l'on arrive à la fin d'un block ("end") on m'est à jour le PATH
        if (token_lu[0], token_lu[1]) == (0, 5):
            tds.path.pop()
        
        # Ici on gère les "procedure" et les "function" que l'on regarde plusieurs fois
        elif (token_lu == (0, 8) or token_lu == (0, 18)) and (lexical_table[list_tokens[ind+1][0]][list_tokens[ind+1][1]] == tds.path[-1]):
            pass

        # Ici on gère les variables
        elif (token_lu[0] == 3):
            # Si c'est un type c'est que l'on définit une variable. Donc on ne s'en occupe pas. On les récupère lorsque initialise la varible
            if lexical_table[token_lu[0]][token_lu[1]] in list_types:
                pass
            # la définition d'une variable : 'name : type := valeur'. On vérifie si l'on est sur name
            elif lexical_table[list_tokens[ind+1][0]][list_tokens[ind+1][1]]==":":
                name_var = lexical_table[token_lu[0]][token_lu[1]]
                type_var = lexical_table[list_tokens[ind+2][0]][list_tokens[ind+2][1]]
                # S'il y a une valeur on la récupère
                if lexical_table[list_tokens[ind+3][0]][list_tokens[ind+3][1]]=="=":
                    var = table_des_symboles.variable(name = name_var, type_entree = type_var, value = lexical_table[list_tokens[ind+4][0]][list_tokens[ind+4][1]])
                    tds.import_variable(var)
                # Sinon on laisse sans valeur
                else :
                    var = table_des_symboles.variable(name = name_var, type_entree = type_var)
                    tds.import_variable(var)
            
            # l'affectation d'une varible : 'name = valeur'. On vérifie si la variable a été déclarée avant affectation et on affecte la variable
            elif lexical_table[list_tokens[ind+1][0]][list_tokens[ind+1][1]]=="=":
                if sc.variableImbricationControl(tds.path, tds.tds, lexical_table[list_tokens[ind][0]][list_tokens[ind][1]]):
                    tds.tds_data[lexical_table[list_tokens[ind][0]][list_tokens[ind][1]]].value = lexical_table[list_tokens[ind+2][0]][list_tokens[ind+2][1]]
                    pass
                else:
                    print(f"\tErreur de sémantique: la variable {lexical_table[list_tokens[ind][0]][list_tokens[ind][1]]} n'a pas été déclarée avant affectation.")
                    pass

            elif lexical_table[list_tokens[ind+1][0]][list_tokens[ind+1][1]] in lexical_table[1] or lexical_table[list_tokens[ind-1][0]][list_tokens[ind-1][1]] in lexical_table[1] :
                if sc.variableAffectationControl(tds.path, tds.tds, lexical_table[list_tokens[ind][0]][list_tokens[ind][1]]):
                    pass
                else:
                    print(f"\tErreur de sémantique: la variable {lexical_table[list_tokens[ind][0]][list_tokens[ind][1]]} n'a pas été initialisée avant utilisation.")
                    pass
        
        # Ici on gère les procédures
        elif (token_lu[0],token_lu[1])==(0,18):
            # J'initialise mes variables
            index = ind
            list_name_params = []
            list_type_params = []
            params = {}

            # On se place au niveau du nom de la procedure
            index += 1
            # On récupère le nom de la variable
            procedure_name = lexical_table[list_tokens[index][0]][list_tokens[index][1]]     
            # On étudie cette fois les params
            index += 1

            # tant que l'on est pas sur le token is
            while lexical_table[list_tokens[index][0]][list_tokens[index][1]] != "is": 
                if list_tokens[index]==(-1, 'EOF', -1):
                    break
                
                # On vérifie si le token est un type et on l'ajoute dans la liste des types des params
                if lexical_table[list_tokens[index][0]][list_tokens[index][1]] in list_types:
                    list_type_params.append(list_tokens[index])
                # Si c'est un autre id c'est un nom et on l'ajoute à la liste des noms des params
                elif list_tokens[index][0] == 3:
                    list_name_params.append(list_tokens[index])
                # On incrémente notre index
                if index<len(list_tokens)-1:
                    index += 1
                # Condition au cas où, on break (Si on n'incrémente plus et que l'on n'est pas sortie de la boucle)
                else:
                    break
            
            # Vérification que les params sont bien initialisé
            if len(list_name_params)!=len(list_type_params):
                print(f"\tErreur de sémantique: un (ou plusieurs) paramètre(s) de la procédure n'a (ont) pas de type.")
                pass
            
            # Ici on créée l'instance de la procedure
            else:
                for n in range(len(list_name_params)):
                    params["var" + str(n)] = table_des_symboles.variable(name = list_name_params[n], type_entree = list_type_params[n])
                function = table_des_symboles.fonction(name = procedure_name, parametres = params)
                tds.import_function(function)

        # Ici on gère les function    
        elif (token_lu[0],token_lu[1])==(0,8):
            # J'initialise mes variables
            index = ind
            list_name_params = []
            list_type_params = []
            params = {}

            # On se place au niveau du nom de la procedure
            index += 1
            # On récupère le nom de la variable
            function_name = lexical_table[list_tokens[index][0]][list_tokens[index][1]]
            # On étudie cette fois les params
            index += 1

            # tant que l'on est pas sur un token 'return' ou tant que l'on n'est pas sur le token is
            while (list_tokens[index][0],list_tokens[index][1])!= (0,21): #or not lexical_table[list_tokens[index][0]][list_tokens[index][1]] == "is":
                if list_tokens[index]==(-1, 'EOF', -1):
                    break

                # On vérifie si le token est un type et on l'ajoute dans la liste des types des params
                elif lexical_table[list_tokens[index][0]][list_tokens[index][1]] in list_types:
                    list_type_params.append(list_tokens[index])
                # Si c'est un autre id c'est un nom et on l'ajoute à la liste des noms des params
                elif list_tokens[index][0] == 3:
                    list_name_params.append(list_tokens[index])
                # On incrémente notre index
                if index<len(list_tokens)-1:
                    index += 1
                # Condition au cas où, on break (Si on n'incrémente plus et que l'on n'est pas sortie de la boucle)
                else :
                    break
            # Vérification que les params sont bien initialisé
            if len(list_name_params)!=len(list_type_params):
                print(f"\tErreur de sémantique: un (ou plusieurs) paramètre(s) de la fonction n'a (ont) pas de type.")
                pass

            #return_type = lexical_table(list_tokens[index])
            else :
                for n in range(len(list_type_params)):
                    params[table_des_symboles.variable(name = list_name_params[n], type_entree = list_type_params[n])] = None
                function = table_des_symboles.fonction(name = function_name, parametres = params, type_de_retour=lexical_table[list_tokens[index][0]][list_tokens[index][1]])
                tds.import_function(function)


# Fonction qui permet de faire l'analyse syntaxique
def parseur(list_tokens, lexical_table, table_ll1):
    pile = []
    pile.append("F")  # on empile l'axiome de la grammaire
    token_lu = list_tokens[0]
    sommet_pile = pile[-1]
    succes = False
    erreur = False
    ind = 0  # indice de la liste de token
    pile_arbre = []  # pile qui va contenir les noeuds de l'arbre
    tds = table_des_symboles.table()

    while not (succes or erreur):
        sommet_pile = pile[-1]  
        token_lu = list_tokens[ind]

        if not est_terminal(sommet_pile):
            token_lu_table = (token_lu[0], 0, token_lu[2]) if token_lu[0] in [3, 4] else token_lu
            rule = table_ll1[sommet_pile].get((token_lu_table[0], token_lu_table[1]))

            if rule is not None:
                if rule != ["epsilon"]:
                    
                    pile.pop()
                    regleC = rule.copy()
                    regleC.reverse()
                    pile.extend(regleC)
                    pile_arbre.append([sommet_pile, regleC])
                else:
                    
                    pile.pop()
                    pile_arbre.append([sommet_pile, "epsilon"])
                    
            else:
                erreur = True
                #Affichage de l'erreur
                token_precedent = list_tokens[ind - 1] if ind > 0 else None
                token_suivant = list_tokens[ind + 1] if ind + 1 < len(list_tokens) else None
                print(f"\tErreur de syntaxe détectée à la ligne {token_lu[2]}:")
                if token_precedent and token_suivant:
                    print(f"\t{token_to_str(token_precedent, lexical_table)} {highlight_error(token_to_str(token_lu, lexical_table))} {token_to_str(token_suivant, lexical_table)}\n")
                elif token_precedent:
                    print(f"\t\t{token_to_str(token_precedent, lexical_table)} {highlight_error(token_to_str(token_lu, lexical_table))}\n")
                elif token_suivant:
                    print(f"\t\t{highlight_error(token_to_str(token_lu, lexical_table))} {token_to_str(token_suivant, lexical_table)}\n")
                

        # Cas 2 : si le sommet de la pile est un terminal (<type_token, valeur_token> donc forme ou "eof")
        else:
            if sommet_pile == (0, 32):
                if token_lu[1] == 32 and token_lu[0] == 0:
                    succes = True
                else:
                    erreur = True
                    print(f"    Erreur de fin de fichier inattendue: fin du fichier atteinte mais il reste des éléments dans la pile, Ligne {token_lu[2]}")
            else:
                if (sommet_pile == (3, 0) and token_lu[0] == 3) or (sommet_pile == (4, 0) and token_lu[0] == 4):
                    
                    # On envoie le token pour savoir s'il est nécessaire de le prendre en compte dans la TDS
                    import_tds(token_lu, lexical_table, list_tokens, ind, tds)
                    
                    pile.pop()
                    ind += 1
                    pile_arbre.append([sommet_pile, lexical_table[token_lu[0]][token_lu[1]]])
                elif sommet_pile[0] == token_lu[0] and sommet_pile[1] == token_lu[1]:
                    
                    # On envoie le token pour savoir s'il est nécessaire de le prendre en compte dans la TDS
                    import_tds(token_lu, lexical_table, list_tokens, ind, tds)
                    
                    pile.pop()
                    ind += 1
                    pile_arbre.append([sommet_pile, lexical_table[token_lu[0]][token_lu[1]]])
                else:
                    erreur = True
                    print(f"\tErreur de non-correspondance de token: attendu {sommet_pile}, trouvé {lexical_table[token_lu[0]][token_lu[1]]}, Ligne {token_lu[2]}")
            

    if succes:
        print("L'analyse syntaxique a réussi sans erreur.")
        print(tds.tds)
        return pile_arbre
    else:
        print("L'analyse syntaxique a échoué en raison d'une erreur de syntaxe.")
        return []


# Fonction qui permet de construire l'AST à partir de la liste des règles
def inverser_enfants_arbre(node):
    if node.children:
        node.children.reverse()  # Inverser l'ordre des enfants du nœud courant
        for enfant in node.children:
            inverser_enfants_arbre(enfant)  # Répéter récursivement pour chaque enfant

def construire_arbre(liste_regles):
    arbre = Node(liste_regles[0][0])  # On crée la racine de l'arbre
    pile_arbre = []  # On crée une pile qui va contenir les noeuds de l'arbre
    pile_arbre.append(arbre)  # On empile la racine de l'arbre

    for i in range(len(liste_regles)):  # On parcourt la liste des règles

        current_node = pile_arbre.pop()  # On dépile le sommet de la pile des noeuds de l'arbre

        if est_terminal(current_node.fct):  # Si le sommet de la pile est un terminal alors on a une feuille
            if current_node.fct == (3, 0):
                current_node.value = liste_regles[i][1]  # On donne la valeur de la feuille
                current_node.fct = "Ident"
            elif current_node.fct == (4, 0):
                current_node.value = liste_regles[i][1]
                current_node.fct = "Number"
            else:
                current_node.value = liste_regles[i][1]
                current_node.fct = "Keyword"

        elif liste_regles[i][1] == "epsilon":  # Si on a epsilon alors on a une feuille vide
            current_node.value = None

        else:  # Sinon on a un non terminal

            for j in range(len(liste_regles[i][1])):  # On parcourt la règle
                current_node.add_child(Node(liste_regles[i][1][j]))  # On ajoute ses enfants au noeud courant
                pile_arbre.append(current_node.children[j])  # On empile les enfants du noeud courant
    inverser_enfants_arbre(arbre)
    return arbre  # On retourne l'arbre


# def prune(tree) :
def remove_unless_character(node):
    # Élaguer récursivement les enfants d'abord
    children_to_keep = []
    for child in node.children:
        pruned_child = remove_unless_character(child)
        if pruned_child or (
                child.value is None and any(isinstance(grandchild.value, tuple) for grandchild in child.children)):
            children_to_keep.append(child)

    # Mettre à jour les enfants après l'élagage
    node.children = children_to_keep

    # Si après l'élagage il ne reste aucun enfant et que la valeur du nœud est élagable, élaguer le nœud
    if not node.children and node.value in (None, "epsilon", ";", "(", ")", ",", ":"):
        return None  # Le nœud est élagable

    return node  # Garder le nœud


def remonter_feuilles(node):
    # Si le nœud a exactement un enfant et que la valeur du nœud est None, remonter cet enfant
    if len(node.children) == 1 and node.value is None:
        return remonter_feuilles(node.children[0])

    # Sinon, appliquer la fonction récursivement à tous les enfants
    new_children = []
    for child in node.children:
        new_child = remonter_feuilles(child)
        if new_child:
            new_children.append(new_child)

    node.children = new_children

    return node



# remove unles node like ";" "(" ")"
def remove_unless_node(node):
    # Élaguer récursivement les enfants d'abord
    children_to_keep = []
    for child in node.children:
        pruned_child = remove_unless_node(child)
        if pruned_child or (
                child.value is None and any(isinstance(grandchild.value, tuple) for grandchild in child.children)):
            children_to_keep.append(child)

    # Mettre à jour les enfants après l'élagage
    node.children = children_to_keep

    # Si après l'élagage il ne reste aucun enfant et que la valeur du nœud est élagable, élaguer le nœud
    if not node.children and node.value in (";", "(", ")"):
        return None  # Le nœud est élagable

    return node  # Garder le nœud

def remove_intermediary_node(root_node):
    def replace_recursive(node, parent, index):
        if node.fct == "PARAM_POINT_VIRG_PLUS" or node.fct == "DECL_STAR" or node.fct == "INSTR_PLUS" or node.fct == "INSTR'":
            # Supprimer le nœud "PARAM_POINT_VIRG_PLUS" du parent
            parent.children.pop(index)

            # Ajouter les nœuds "PARAM" à la place de "PARAM_POINT_VIRG_PLUS"
            for param_node in node.children:
                parent.children.insert(index, param_node)
                index += 1

        # Parcourir récursivement les enfants du nœud actuel
        for i, child in enumerate(node.children):
            replace_recursive(child, node, i)

    # Créer un nœud factice pour représenter la racine parente du nœud racine réel
    fake_root = Node("FAKE_ROOT", children=[root_node])

    # Appeler la fonction récursive avec le faux nœud racine
    replace_recursive(fake_root, None, None)

    # Mettre à jour le nœud racine réel en utilisant le seul enfant du faux nœud racine
    root_node = fake_root.children[0]


def elaguer(arbre):
    arbre = remove_unless_character(arbre)
    arbre = remonter_feuilles(arbre)
    arbre = remove_unless_node(arbre)
    remove_intermediary_node(arbre)
    return arbre
