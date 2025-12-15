# 🚀 Installation Simple - Pas à Pas

## ✅ Méthode la plus simple (copier-coller)

Ouvrez un terminal et **copiez-collez cette commande complète** :

```bash
cd "/Users/martinemenguy/Desktop/for facefusion" && \
ls facefusion/install.py && \
echo "✅ Fichier install.py trouvé !" && \
cd facefusion && \
python3 install.py && \
cd .. && \
pip3 install gradio gradio-rangeslider && \
echo "🎉 Installation terminée !" && \
python3 actor_faceswap_studio.py
```

**Cette commande fait TOUT automatiquement** :
1. ✅ Va dans le bon dossier
2. ✅ Vérifie que install.py existe
3. ✅ Installe FaceFusion
4. ✅ Installe Gradio
5. ✅ Lance votre application

---

## 📋 Ou étape par étape

Si vous préférez voir ce qui se passe à chaque étape :

### Étape 1: Aller dans le bon dossier

```bash
cd "/Users/martinemenguy/Desktop/for facefusion"
```

Vérifiez que vous êtes au bon endroit :
```bash
pwd
# Doit afficher: /Users/martinemenguy/Desktop/for facefusion
```

### Étape 2: Vérifier que install.py existe

```bash
ls facefusion/install.py
# Doit afficher: facefusion/install.py
```

### Étape 3: Installer FaceFusion

```bash
cd facefusion
python3 install.py
```

**Attendez** que l'installation se termine (2-5 minutes). Vous verrez :
- Téléchargement de packages
- Installation de dépendances
- Messages de succès

### Étape 4: Revenir au dossier parent

```bash
cd ..
```

Vérifiez que vous êtes revenu :
```bash
pwd
# Doit afficher: /Users/martinemenguy/Desktop/for facefusion
```

### Étape 5: Installer Gradio

```bash
pip3 install gradio gradio-rangeslider
```

### Étape 6: Lancer l'application

```bash
python3 actor_faceswap_studio.py
```

**L'interface s'ouvre automatiquement dans votre navigateur à** : http://localhost:7860

---

## 🆘 Si vous avez une erreur "command not found: python3"

Essayez avec `python` au lieu de `python3` :

```bash
cd "/Users/martinemenguy/Desktop/for facefusion/facefusion"
python install.py
cd ..
pip install gradio gradio-rangeslider
python actor_faceswap_studio.py
```

---

## 🔍 Vérifier votre Python

Avant de commencer, vérifiez votre version de Python :

```bash
python3 --version
# ou
python --version
```

**Doit afficher** : `Python 3.10.x` ou `Python 3.11.x` ou `Python 3.12.x`

Si la version est inférieure à 3.10, installez Python 3.11 :
- **macOS** : `brew install python@3.11`
- **Windows** : Téléchargez depuis https://www.python.org/

---

## 📊 Résumé visuel

```
Votre dossier actuel
│
/Users/martinemenguy/Desktop/for facefusion/
│
├── facefusion/                    ← Entrez ici avec "cd facefusion"
│   ├── install.py                ← Exécutez "python3 install.py"
│   ├── requirements.txt
│   └── facefusion/
│
├── actor_faceswap_studio.py      ← Votre app (lancez après installation)
├── START_HERE.md
└── ... (autres fichiers)
```

---

## ✅ Checklist rapide

- [ ] Terminal ouvert
- [ ] Python 3.10+ installé (`python3 --version`)
- [ ] Copié-collé la commande complète ci-dessus
- [ ] Attendu que l'installation se termine
- [ ] Application lancée (navigateur ouvert automatiquement)

---

## 🎯 Une fois l'installation terminée

1. **L'interface web s'ouvre** à http://localhost:7860
2. **Uploadez** une photo de votre acteur
3. **Uploadez** une vidéo courte (test)
4. **Sélectionnez** le preset "Rapide"
5. **Cliquez** sur "Lancer le Face Swap"
6. **Admirez** le résultat !

---

## 💡 Conseil

La **première fois**, l'application va télécharger les modèles d'IA (~500 MB).
Cela peut prendre 5-10 minutes selon votre connexion internet.

Les fois suivantes, le lancement sera instantané !

---

**Besoin d'aide ?** Copiez-collez simplement l'erreur que vous voyez et je vous aiderai !
