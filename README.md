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
| `bureau.md` | Les membres du bureau, leurs photos, l'adresse mail du club |
| `membres.md` | Le trombinoscope : la liste des membres et leurs photos |
| `partenaires.md` | Les partenaires du club, leur logo et leur site |

Pour modifier un texte sur GitHub :

1. Ouvrir le fichier, puis cliquer sur le crayon (« Edit this file »).
2. Changer le texte.
3. Cliquer sur « Commit changes ».
4. Le site est à jour environ une minute plus tard.

Un fichier a deux parties :

- **En haut, entre les deux lignes `---`** : les titres, les listes et les petits textes. Chaque texte est entre guillemets droits (`"…"`). Gardez ces guillemets. Pour citer quelque chose dans un texte, utilisez les guillemets français « ».
- **En bas, après le second `---`** : les paragraphes, en Markdown. Laissez une ligne vide entre deux paragraphes. Un lien s'écrit `[texte du lien](https://adresse)`.

Changer la photo d'un membre du bureau : déposer la photo dans `photos/bureau/` (bouton « Add file », puis « Upload files »), puis mettre son chemin après `photo:` dans `bureau.md`. Sans ligne `photo:`, le membre s'affiche sans photo.

Mettre à jour le trombinoscope : la liste des membres et leurs photos viennent du classeur Excel du trombinoscope du club. Depuis la racine du dépôt, `uv run _outils/trombinoscope.py "<classeur>.xls"` remplace la liste dans `membres.md` et les photos de `photos/membres/`. Pour un seul membre, on peut aussi modifier `membres.md` à la main : ajouter un bloc qui commence par `- prenom:` à sa place dans l'ordre des noms, ou en supprimer un, et déposer sa photo dans `photos/membres/`. Sans ligne `photo:`, le membre s'affiche avec ses initiales. Relancer l'outil efface ces modifications à la main.

Ajouter un partenaire : copier un bloc qui commence par `- nom:` dans `partenaires.md` et changer ses valeurs. `logo_largeur` et `logo_hauteur` sont la taille de l'image en pixels. Sans ligne `site:`, le partenaire s'affiche sans lien.

Ajouter un parcours : copier un bloc qui commence par `- km:` dans `lieux.md` et changer ses valeurs. Le nombre après `openrunner:` est le numéro du parcours sur OpenRunner. Un lieu cité dans `passe_par` mais absent de la liste `lieux` s'ajoute tout seul à la fin.

Si le haut d'un fichier contient une erreur, le site n'est pas mis à jour et la version précédente reste en ligne. GitHub l'indique par une croix rouge à côté du commit.

## Le reste du dépôt

- `index.html` : la mise en page, les couleurs et le code de la page. Il assemble les rubriques, dans l'ordre de la page.
- `_config.yml` : les réglages de Jekyll, qui fabrique le site.
- `.github/workflows/` : les deux publications automatiques, celle du site et celle des aperçus de PR.
- `photos/` : les photos servies avec le site : dans `photos/bureau/` celles des membres du bureau, dans `photos/membres/` celles du trombinoscope.
- `_outils/` : l'outil qui fabrique le trombinoscope à partir du classeur Excel. Il ne sert pas à fabriquer le site.
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

Chaque push sur `main` fabrique le site avec Jekyll et le publie dans la branche `gh-pages`, que GitHub Pages sert (environ une minute). Ne modifiez pas `gh-pages` à la main.

Une pull request (PR) reçoit un aperçu du site avec ses changements : un commentaire sur la PR donne le lien. L'aperçu se met à jour à chaque push sur la PR, et disparaît quand la PR est fermée ou fusionnée.

Une croix rouge à côté d'un commit ou d'une PR veut dire que la fabrication a échoué : le site, ou l'aperçu, n'a pas été mis à jour et la version précédente reste en ligne.
