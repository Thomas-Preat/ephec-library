# ephec-library

Bibliotheque de modules MicroPython pour le cours, avec documentation web generee automatiquement a partir de l'arborescence `docs/elements`.

## Objectif de ce README

Ce guide permet a une autre personne (ex: un autre professeur) de:

1. Comprendre comment le depot est organise.
2. Ajouter un nouvel element (capteur, afficheur, actionneur, etc.).
3. Mettre a jour l'index de documentation sans casser le site.

## Structure du projet

- `docs/elements/<categorie>/<element>/` contient les modules documentes.
- `generate.py` scanne cette arborescence et regenere `docs/files.json`.
- `docs/index.html`, `docs/script.js`, `docs/style.css` affichent la doc cote web.
- `docs/template.md` est un modele de fiche markdown.

Categories deja presentes:

- `actuators`
- `audio`
- `display`
- `input`
- `sensors`

## Convention minimale pour un element

Pour un element standard nomme `my_sensor` dans la categorie `sensors`:

1. Creer le dossier:
	 - `docs/elements/sensors/my_sensor/`
2. Ajouter les fichiers:
	 - `my_sensor.py` (bibliotheque)
	 - `my_sensor.md` (fiche de documentation)
	 - `my_sensor_example.py` (optionnel mais recommande)

Arborescence attendue:

```text
docs/
	elements/
		sensors/
			my_sensor/
				my_sensor.py
				my_sensor.md
				my_sensor_example.py   # optionnel
```

## Regles detectees par generate.py

Le script `generate.py` applique les regles suivantes:

1. Le fichier `.py` principal est prioritairement `<nom_dossier>.py`.
2. Si ce fichier n'existe pas, le premier `.py` non suffixe `_example.py` est pris.
3. Le markdown principal est prioritairement `<nom_dossier>.md`.
4. L'exemple est prioritairement `<nom_dossier>_example.py`.
5. Les noms affiches dans le site remplacent `_` et `-` par des espaces.

Conseil: respecter strictement le schema `<nom_dossier>.<ext>` pour eviter toute ambiguite.

## Cas avance: groupe avec variantes

Le generateur supporte aussi un niveau supplementaire de dossier (bundle):

```text
docs/elements/<categorie>/<groupe>/<variante>/...
```

Exemple:

```text
docs/elements/sensors/temperature/
	temperature.md
	analog/
		analog.py
		analog.md
	i2c/
		i2c.py
		i2c.md
```

Dans ce cas:

- la description du groupe est prise dans `temperature.md`, `index.md` ou `README.md` (dans cet ordre);
- chaque variante doit contenir au minimum un `.py` principal.

## Procedure d'ajout (pas a pas)

1. Choisir la categorie cible (`sensors`, `display`, etc.).
2. Creer le dossier de l'element.
3. Ajouter le module `.py` principal.
4. Rediger la fiche `.md` en s'aidant de `docs/template.md`.
5. Ajouter un `_example.py` si pertinent.
6. Regenerer l'index JSON:

```bash
python generate.py
```

7. Verifier que `docs/files.json` contient bien la nouvelle entree.
8. Committer au minimum:
	 - le nouveau dossier d'element;
	 - `docs/files.json` regenere.

## Checklist rapide avant commit

- Le dossier est dans la bonne categorie.
- Les noms de fichiers suivent le nom du dossier.
- Le `.md` explique role, pinout, fonctions, remarques et references.
- Le script `python generate.py` s'execute sans erreur.
- Le nouvel element apparait dans `docs/files.json`.

## Exemple concret

Ajouter `pmod_tmp` dans `sensors`:

```text
docs/elements/sensors/pmod_tmp/
	pmod_tmp.py
	pmod_tmp.md
	pmod_tmp_example.py
```

Puis:

```bash
python generate.py
```

Le generateur ajoutera automatiquement une entree dans `docs/files.json` avec:

- `path`: vers `pmod_tmp.py`
- `descriptionPath`: vers `pmod_tmp.md`
- `examplePath`: vers `pmod_tmp_example.py` (si present)

## Remarques de maintenance

- `docs/files.json` est un fichier genere: ne pas l'editer manuellement.
- En cas de renommage de dossier/fichier, relancer `python generate.py` immediatement.
- Garder un style homogene entre fiches markdown pour faciliter l'usage pedagogique.