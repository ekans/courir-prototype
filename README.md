# courir-prototype

Prototype du site de Courir Fonsegrives, club de course à pied de Quint-Fonsegrives.

En ligne : https://ekans.github.io/courir-prototype/

## Modifier le contenu

Le texte de chaque rubrique est dans un fichier de `_data/`.
Pour le modifier, ouvrir le fichier sur GitHub, cliquer sur le crayon, puis valider le commit sur `main`.
Le site se met à jour environ une minute plus tard.

Si un texte contient « : » ou commence par un caractère spécial, le mettre entre guillemets droits (`"…"`).
Sinon le fichier YAML est invalide et la publication échoue.

## Organisation

- `index.html` : la mise en page. Le texte vient des fichiers de `_data/`.
- `_data/` : un fichier YAML par rubrique de la page (accueil, présentation, lieux, parcours, semaine, Balade, adhésion, bureau).
- `photos/` : les images servies avec le site.
- `documents/` : le bulletin d'adhésion.

Un parcours indique les lieux qu'il traverse. Le mur des lieux et la liste des parcours de chaque lieu en sont déduits dans le navigateur.

## Voir en local

GitHub Pages construit le site avec Jekyll.
Pour le voir en local, avec Ruby et Jekyll installés :

```sh
jekyll serve
```

Puis ouvrir http://localhost:4000/courir-prototype/.

## Publier

GitHub Pages construit et sert la racine de `main`.
Chaque push sur `main` relance la publication (environ une minute).
