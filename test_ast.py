import lexeur.lexeur as lex
import parseur.parseur as parse
import parseur.ast_pars as ast
import parseur.show as show
import parseur.prune_ast as prune

from parseur.table_syntaxique import table_syntaxique as table_ll1
from display.create_tree import create_tree
import networkx as nx
import matplotlib as plt

def print_tokens(tokens):
    current_line = tokens[0][2]

    for _, (token_type, token_value, token_line) in enumerate(tokens):
        if token_line != current_line:
            print()
            current_line = token_line

        print(f"<{token_type}, {token_value}>", end=' ')
        
        

def print_explicit_tokens(tokens, list_type_token, lexical_table):
    current_line = tokens[0][2]

    for _, (token_type, token_value, token_line) in enumerate(tokens):
        if token_line != current_line:
            print()
            current_line = token_line
        if token_type == 4:
            print(f"<{list_type_token[token_type]}, {token_value}>", end=' ')
        else:
            print(f"<{list_type_token[token_type]}, {lexical_table[token_type][token_value]}>", end=' ')


list_type_token = {
        0: "Keyword",
        1: "Operator",
        2: "Syntax Operator",
        3: "Identifier",
        4: "Constant Number",
        5: "Invalid Character"
    }


def test_parseur(filename):
    with open(filename, 'r') as file:
        source_code = file.read()

    #On lance l'analyse lexicale
    tokens, lexical_table = lex.lexical_analysis(source_code)
    
    print("\n \nTable Lexicale:")
    for key, values in lexical_table.items():
        print(f"    {list_type_token[key]}: {values}")
    print(f"\n\nListe des tokens pour {filename} avec les tokens de la forme <type, valeur>: \n")
    
    #version tokens explicites
    print_explicit_tokens(tokens, list_type_token, lexical_table)
    
    #version tokens brutes
    print("\n\n\n\nListe brutes des tokens: \n")
    print_tokens(tokens)
    
    #On fait à présent l'analyse syntaxique
    print("\n\n\n\nAnalyse syntaxique: \n")
    resultat_ast_parseur = ast.parse(tokens, lexical_table, table_ll1)
    if resultat_ast_parseur:
        arbre = ast.construire_arbre(resultat_ast_parseur)
    return arbre


arbre = test_parseur("tests/test_lexeur/test2.txt")
show.visualize_tree(arbre).render(filename='syntax_tree', directory='./output', cleanup=True, format='png', engine='dot')

#arbre_elague = prune.remove_empty_nodes(arbre)

#show.visualize_tree(arbre_elague).render(filename='prun_syntax_tree', directory='./output', cleanup=True, format='png', engine='dot')

