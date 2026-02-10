# 🎵 MP3 to MIDI Converter

Outil de transcription audio permettant de convertir des fichiers MP3 en MIDI avec extraction détaillée des notes et affichage des touches de piano.

## 📋 Description

Ce projet utilise l'intelligence artificielle (modèle **basic-pitch** de Spotify) pour transcrire automatiquement des fichiers audio MP3 en fichiers MIDI. L'outil offre également des fonctionnalités avancées :

- 🎹 Conversion MP3 → MIDI
- 📊 Extraction détaillée des notes avec timing précis
- 🎼 Affichage des notes en notation anglaise et française (solfège)
- 📈 Visualisation du piano roll en mode texte
- ⚡ Interface en ligne de commande simple et rapide

## 🚀 Installation

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Dépendances

Installez les bibliothèques nécessaires :

```bash
pip install basic-pitch pretty-midi
```

## 💻 Utilisation

### Utilisation basique

```bash
python mp3_to_midi.py <fichier_entree.mp3>
```

Exemple :
```bash
python mp3_to_midi.py oorumblood.mp3
```

Cette commande va :
1. Transcrire le fichier MP3 en MIDI
2. Créer un fichier `oorumblood.mid` dans le même répertoire
3. Afficher toutes les notes détectées avec leur timing
4. Afficher le piano roll textuel

### Spécifier un fichier de sortie personnalisé

```bash
python mp3_to_midi.py <fichier_entree.mp3> <fichier_sortie.mid>
```

Exemple :
```bash
python mp3_to_midi.py morceau.mp3 resultat.mid
```

### Utilisation en tant que module Python

```python
from mp3_to_midi import process, mp3_to_midi, extract_notes

# Pipeline complet (conversion + analyse + affichage)
notes = process("morceau.mp3")

# Ou conversion seule
midi_path = mp3_to_midi("morceau.mp3", "sortie.mid")

# Ou extraction des notes depuis un MIDI existant
notes = extract_notes("fichier.mid")
```

## 📊 Format des données

Chaque note extraite contient les informations suivantes :

```python
{
    "name_en": "C4",           # Nom en notation anglaise
    "name_fr": "Do4",          # Nom en solfège français
    "midi_number": 60,         # Numéro MIDI (0-127)
    "start": 1.234,            # Temps de début (secondes)
    "duration": 0.500,         # Durée (secondes)
    "velocity": 80,            # Vélocité/intensité (0-127)
    "is_sharp": False          # Indique si c'est un dièse
}
```

## 📋 Fonctionnalités

### Conversion MP3 → MIDI
Utilise le modèle de deep learning **basic-pitch** pour une transcription précise des mélodies et harmonies.

### Extraction des notes
- Détection automatique de toutes les notes présentes
- Timing précis au millième de seconde
- Information de vélocité (intensité de la note)
- Identification des dièses

### Affichage en tableau
```
======================================================================
    Time  Duration  Note (EN)  Note (FR)  MIDI#  Vel
----------------------------------------------------------------------
   0.000s     0.250s         C4        Do4     60   80
   0.250s     0.500s         E4        Mi4     64   75  #
   ...
======================================================================
Total notes: 42
```

### Piano Roll textuel
Visualisation temporelle des notes actives :
```
Piano Roll (step=0.5s):
------------------------------------------------------------
    0.00s | Do4
    0.50s | Mi4, Sol4
    1.00s | Do5
------------------------------------------------------------
```

## 🎼 Notation musicale

Le projet supporte la notation française (solfège) :

| Anglais | Français |
|---------|----------|
| C       | Do       |
| D       | Ré       |
| E       | Mi       |
| F       | Fa       |
| G       | Sol      |
| A       | La       |
| B       | Si       |

Les dièses sont notés avec le symbole `#` (ex: Do#, Ré#).

## 🛠️ Architecture du code

- `mp3_to_midi()` : Convertit un MP3 en MIDI
- `extract_notes()` : Extrait les notes d'un fichier MIDI
- `midi_note_to_name()` : Convertit un numéro MIDI en nom de note
- `display_notes()` : Affiche les notes en format tableau
- `display_piano_roll()` : Génère une visualisation du piano roll
- `process()` : Pipeline complet de traitement

## ⚠️ Limitations

- La qualité de transcription dépend de la qualité audio du fichier source
- Les fichiers avec beaucoup de polyphonie (plusieurs notes simultanées) peuvent être plus difficiles à transcrire avec précision
- Le modèle basic-pitch est optimisé pour les mélodies et instruments musicaux standards

## 📝 Exemple de sortie

```
Transcribing 'oorumblood.mp3' ...
MIDI saved to 'oorumblood.mid'

======================================================================
    Time  Duration  Note (EN)  Note (FR)  MIDI#  Vel
----------------------------------------------------------------------
   0.000s     0.234s        C#4       Do#4     61   82
   0.234s     0.156s         E4        Mi4     64   78
   ...
======================================================================
Total notes: 127

Piano Roll (step=0.5s):
------------------------------------------------------------
    0.00s | Do#4
    0.50s | Mi4, Sol4
    ...
------------------------------------------------------------
```

## 📄 Licence

Ce projet est à usage personnel et éducatif.

## 🙏 Remerciements

- [Spotify Basic Pitch](https://github.com/spotify/basic-pitch) - Modèle de transcription audio
- [pretty_midi](https://github.com/craffel/pretty-midi) - Manipulation de fichiers MIDI

---
