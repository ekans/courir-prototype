# courir-prototype

Prototype du site de Courir Fonsegrives, club de course à pied de Quint-Fonsegrives.

En ligne : https://ekans.github.io/courir-prototype/

## Modifier un texte

Chaque rubrique du site a son fichier dans [`_rubriques/`](_rubriques) :

| Fichier | Rubrique |
|---|---|
| `accueil.md` | La grande photo, le titre et le bouton du haut |
| `presentation.md` | « Course à pied, plaisir et convivialité… » |
| `lieux.md` | Les lieux et les quatorze parcours |
| `semaine.md` | Les trois sorties de la semaine |
| `balade.md` | La Balade de la Saune |
| `adhesion.md` | Les tarifs et comment adhérer |
| `bureau.md` | Les membres du bureau, l'adresse mail du club |

Pour modifier un texte sur GitHub :

1. Ouvrir le fichier, puis cliquer sur le crayon (« Edit this file »).
2. Changer le texte.
3. Cliquer sur « Commit changes ».
4. Le site est à jour environ une minute plus tard.

Un fichier a deux parties :

- **En haut, entre les deux lignes `---`** : les titres, les listes et les petits textes. Chaque texte est entre guillemets droits (`"…"`). Gardez ces guillemets. Pour citer quelque chose dans un texte, utilisez les guillemets français « ».
- **En bas, après le second `---`** : les paragraphes, en Markdown. Laissez une ligne vide entre deux paragraphes. Un lien s'écrit `[texte du lien](https://adresse)`.

Ajouter un parcours : copier un bloc qui commence par `- km:` dans `lieux.md` et changer ses valeurs. Le nombre après `openrunner:` est le numéro du parcours sur OpenRunner. Un lieu cité dans `passe_par` mais absent de la liste `lieux` s'ajoute tout seul à la fin.

Si le haut d'un fichier contient une erreur, le site n'est pas mis à jour et la version précédente reste en ligne. GitHub l'indique par une croix rouge à côté du commit.

## Le reste du dépôt

- `index.html` : la mise en page, les couleurs et le code de la page. Il assemble les rubriques, dans l'ordre de la page.
- `_config.yml` : les réglages de Jekyll, qui fabrique le site.
- `photos/` : les photos servies avec le site (pour l'instant, le trombinoscope).
- Les autres images et le PDF sont chargés depuis [courir-fonsegrives.fr](https://courir-fonsegrives.fr).

## Voir en local

Le site passe par [Jekyll](https://jekyllrb.com), comme sur GitHub Pages. Ouvrir `index.html` directement dans un navigateur ne montre plus le contenu.

Avec Podman ou Docker, depuis la racine du dépôt :

```sh
podman run --rm -it -p 4000:4000 -v "$PWD:/srv:Z" -w /srv docker.io/library/ruby:3.3 \
  bash -c 'gem install github-pages -v 232 --no-document && jekyll serve --host 0.0.0.0'
```

Puis ouvrir http://localhost:4000.

## Publier

GitHub Pages sert la racine de `main` et la passe par Jekyll.
Chaque push sur `main` relance la publication (environ une minute).
