# ephec-library

Bibliothèque de modules MicroPython pour le cours, avec documentation web générée automatiquement à partir de l'arborescence `docs/elements`.

## Objectif de ce README

Ce guide permet à une autre personne (ex: un autre professeur) de:

1. Comprendre comment le dépôt est organisé.
2. Ajouter un nouvel élément (capteur, afficheur, actionneur, etc.).
3. Mettre à jour l'index de documentation sans casser le site.

## Structure du projet

- `docs/elements/<categorie>/<element>/` contient les modules documentés.
- `generate.py` scanne cette arborescence et régénère `docs/files.json`.
- `docs/index.html`, `docs/script.js`, `docs/style.css` affichent la doc côté web.
- `docs/template.md` est un modèle de fiche markdown.

Catégories déjà présentes:

- `actuators`
- `audio`
- `display`
- `input`
- `sensors`

## Convention minimale pour un élément

Pour un élément standard nommé `my_sensor` dans la catégorie `sensors`:

1. Créer le dossier:
	 - `docs/elements/sensors/my_sensor/`
2. Ajouter les fichiers:
	 - `my_sensor.py` (bibliothèque)
	 - `my_sensor.md` (fiche de documentation)
	 - `my_sensor_example.py` (optionnel mais recommandé)

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

## Règles détectées par generate.py

Le script `generate.py` applique les règles suivantes:

1. Le fichier `.py` principal est prioritairement `<nom_dossier>.py`.
2. Si ce fichier n'existe pas, le premier `.py` non suffixe `_example.py` est pris.
3. Le markdown principal est prioritairement `<nom_dossier>.md`.
4. L'exemple est prioritairement `<nom_dossier>_example.py`.
5. Les noms affichés dans le site remplacent `_` et `-` par des espaces.

Conseil: respecter strictement le schéma `<nom_dossier>.<ext>` pour éviter toute ambiguïté.

## Cas avancé: groupe avec variantes

Le générateur supporte aussi un niveau supplémentaire de dossier (bundle):

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

## Procédure d'ajout (pas à pas)

1. Choisir la catégorie cible (`sensors`, `display`, etc.).
2. Créer le dossier de l'élément.
3. Ajouter le module `.py` principal.
4. Rédiger la fiche `.md` en s'aidant de `docs/template.md`.
5. Ajouter un `_example.py` si pertinent.
6. Régénérer l'index JSON:

```bash
python generate.py
```

7. Vérifier que `docs/files.json` contient bien la nouvelle entrée.
8. Committer au minimum:
	 - le nouveau dossier d'élément;
	 - `docs/files.json` régénéré.

## Checklist rapide avant commit

- Le dossier est dans la bonne catégorie.
- Les noms de fichiers suivent le nom du dossier.
- Le `.md` explique rôle, pinout, fonctions, remarques et références.
- Le script `python generate.py` s'exécute sans erreur.
- Le nouvel élément apparaît dans `docs/files.json`.

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

Le générateur ajoutera automatiquement une entrée dans `docs/files.json` avec:

- `path`: vers `pmod_tmp.py`
- `descriptionPath`: vers `pmod_tmp.md`
- `examplePath`: vers `pmod_tmp_example.py` (si présent)

## Remarques de maintenance

- `docs/files.json` est un fichier généré: ne pas l'éditer manuellement.
- En cas de renommage de dossier/fichier, relancer `python generate.py` immédiatement.
- Garder un style homogène entre fiches markdown pour faciliter l'usage pédagogique.