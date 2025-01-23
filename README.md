
# Projet de Compilation : Compilateur du langage canAda

Ce projet consiste à développer un **compilateur** pour une version simplifiée du langage Ada, nommée **canAda**. 
Le but est de comprendre et de mettre en œuvre toutes les étapes nécessaires à la compilation, depuis l'analyse lexicale 
jusqu'à la génération de code assembleur ARM.

## Objectifs du Projet
- Implémenter un **analyseur lexical** capable de reconnaître les unités lexicales du langage canAda.
- Développer un **analyseur syntaxique descendant** pour valider la grammaire des programmes écrits en canAda.
- Construire et visualiser un **arbre abstrait** représentant la structure du programme.
- Effectuer des **contrôles sémantiques** pour vérifier la cohérence des programmes.
- Générer du **code assembleur ARM** pour exécuter les programmes compilés.

## Étapes de Réalisation
### Module PCL1 : Analyse lexicale, syntaxique et construction de l'arbre abstrait
1. Définir la grammaire complète du langage canAda.
2. Implémenter un analyseur lexical et syntaxique sans générateur automatique.
3. Construire l'arbre abstrait et fournir une visualisation graphique.
4. Détecter et signaler les erreurs lexicales et syntaxiques avec des messages explicites (numéros de ligne inclus).

### Module PCL2 : Contrôles sémantiques et génération de code
1. Implémenter les vérifications sémantiques (déclarations, types, portée, etc.).
2. Générer le code assembleur ARM de manière incrémentale.
3. Tester le compilateur sur des programmes canAda variés et documenter ses limites.

## Fonctionnalités
- Analyse et détection d'erreurs lexicales, syntaxiques et sémantiques.
- Construction et visualisation de l'arbre abstrait.
- Génération de code assembleur ARM.
- Support des fonctionnalités clés du langage canAda :
  - Procédures et fonctions.
  - Structures (enregistrements).
  - Boucles et conditionnelles.
  - Entrées/sorties limitées (`put`).
  
## Organisation des fichiers
- **`lexical_analyzer.py`** : Analyseur lexical.
- **`syntax_analyzer.py`** : Analyseur syntaxique.
- **`semantic_checker.py`** : Contrôles sémantiques.
- **`code_generator.py`** : Génération de code assembleur ARM.
- **`test_programs/`** : Exemples de programmes canAda pour tester le compilateur.

## Instructions
### Cloner le dépôt
```bash
git clone <URL_DU_DEPOT>
```
### Exécuter le compilateur
```bash
python main.py --input program.canada
```
### Visualiser l'arbre abstrait
Le compilateur génère un fichier graphique représentant l'arbre abstrait (format `.png`).

### Modifier la grammaire ou les règles
Les règles grammaticales sont définies dans le fichier `grammar.txt`.

## Exemple de Programme canAda
```ada
with Ada.Text_IO ; use Ada.Text_IO ;

procedure unDebut is

function aireRectangle(larg : integer; long : integer) return integer is
begin
   return larg * long;
end aireRectangle;

begin
   put(aireRectangle(3, 4));
end unDebut ;
```

## Documentation
- [Dragon Book](https://example.com/dragon-book) : Théorie des analyseurs lexicaux et syntaxiques.
- [Guide Ada](https://example.com/ada-guide) : Introduction au langage Ada.


