import unittest

from lexeur.lexeur import lexical_analysis
from parseur.table_syntaxique import table_syntaxique
from parseur.ast_pars import parseur, construire_arbre
from parseur.ast_pars import elaguer

import parseur.show as show


class MyTestCase(unittest.TestCase):
    def test_pres(self):
        with open("tests/test_semantic/test_all.txt") as f:
            source_code = f.read()

        tok, lex,  = lexical_analysis(source_code)
        list_regle = parseur(tok, lex, table_syntaxique)
        
        
        if list_regle == []:
            print("Erreur lors de la compilation")
        elif False: # Passer en False pour ne pas afficher les arbres
            arbre = construire_arbre(list_regle)
            show.afficher(arbre, 'LR', 'test_pres_syntax_tree_LR', './output/basic')
            show.afficher(arbre, '', 'test_pres_syntax_tree', './output/basic')

            arbre_elaguer = elaguer(arbre)

            show.afficher(arbre_elaguer, 'LR', 'test_pres_syntax_tree_elaguer_LR', './output/reduced')
            show.afficher(arbre_elaguer, '', 'test_pres_syntax_tree_elaguer', './output/reduced')

if __name__ == '__main__':
    unittest.main()
