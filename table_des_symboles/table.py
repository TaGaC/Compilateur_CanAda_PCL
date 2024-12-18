import os
import re

from .symbole import *
from .semantics_controls import * 


class table:
    def __init__(self):
        self.path = ["F"]
        self.tds= {"F":{}}
        self.tds_data = {} 
        self.functions = []
        self.block_tokens = {(0,8) : "function", (0,18): "procedure", (0,2):"begin", (0,7):"for", (0,9):"loop", (0,27):"while"}
        self.end_tokens = {(0,5): "end"}
        self.variables_tokens = {}
    
    def get_current_bloc(self):
        current_node = self.tds
        for element in self.path:
            current_node = current_node[element]
        return current_node

    def create_block(self, block_name):
        current_node = self.get_current_bloc()
        if block_name in current_node:
            current_node[block_name+str((current_node.count(block_name)+1))] = {}
        else:
            current_node[block_name + "0"] = {}

    def import_function(self, function):
        block = self.get_current_bloc()
        self.path.append(function.name) 
        block[function.name] = {}
        self.tds_data[function.name] = function
        pass

    def import_variable(self, variable):
        block = self.get_current_bloc()
        if type(block)==dict and variable.name not in block:
            block[variable.name] = variable
        elif type(block)==fonction and variable.name not in block.sous_bloc:
            block.sous_bloc[variable.name]=variable
        self.tds_data[variable.name] = variable

#################################################### Pas compris après MDRRR ################################################################

    def import_token(self, entry):
        if entry in self.block_tokens:
            # Ajouter une entrée "bloc" dans la TDS
            block = self.get_current_bloc()
            if self.enum_bloc(block):
                for element in self.enum_bloc(block):
                    #print(f"element name: {element}")
                    pass
                name = self.block_tokens[entry] + str(self.countRegEx(block, self.block_tokens[entry]))
            else:
                #print("bloc vide")
                pass
        elif entry in self.end_tokens:
            self.import_end_tokens()
        elif entry in self.variables_tokens:
            self.import_variables_tokens(entry)

    def add_value(self, entry):
        current_node = self.tds
        for element in self.path:
            current_node = current_node[element]
        if (sc.variableImbricationControle(current_node, entry[1], self.path)): ############################### A modifier, pour faire fonctionner
            print(f"Erreur: la variable {entry[1]} existe déjà.")
        else :
            current_node[entry[0]] = entry[1]
    
    def countRegEx(self, lst, expr):
        return len([element for element in lst if re.search(expr, element)])

    def extract_repr(self, node):
        repr_str=""
        if type(node)==dict:
            for element in node:
                if element == None:
                    return ""
                elif type(element)==variable:
                    repr_str += element.__repr__()
                elif type(element)==fonction or type(element)==procedure:
                    repr_str += element.__repr__()
                    repr_str += (":{" + self.extract_repr(element) + "}")
                elif type(element)==str:
                    repr_str += element + ":{" + self.extract_repr(node[element]) + "}"
                else:
                    print(f"type de bloc non reconnu: {type(element)}")
                    print(element)
        elif type(node) == fonction:
            for element in node.sous_bloc: 
                if element == None:
                    return ""
                elif type(element)==variable:
                    repr_str += element.__repr__()
                elif type(element)==fonction or type(element)==procedure:
                    repr_str += element.__repr__()
                    repr_str += (":{" + self.extract_repr(element) + "}")
                elif type(element)==str:
                    repr_str += element + ":{" + self.extract_repr(node.sous_bloc) + "}"
                else:
                    print(f"type de bloc non reconnu: {type(element)}")
                    print(element)
        return repr_str

    def __repr__(self):
        print('\n\n')
        print(self.tds)
        print('\n\n')
        #print(self.tds['F']['undebut'].sous_bloc['airerectangle'])
        repr_str = self.extract_repr(self.tds)
        return repr_str
        print(self.tds)
        print(self.tds["F"]["undebut"].sous_bloc)
        return "ok"
