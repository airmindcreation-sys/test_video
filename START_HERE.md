# ⭐ COMMENCEZ ICI - Actor Face Swap Studio

Bienvenue dans votre application de face swap personnalisée pour acteurs ! 🎬

---

## 🎯 Ce que vous avez maintenant

Une application **complète, intuitive et professionnelle** pour remplacer le visage d'un acteur dans vos vidéos en quelques clics.

### ✨ Fonctionnalités clés:
- ✅ Interface web simple (pas de ligne de commande)
- ✅ 3 presets de qualité (Rapide/Équilibré/Haute qualité)
- ✅ 13 modèles d'IA différents
- ✅ Support GPU pour traitement rapide
- ✅ Amélioration automatique du visage
- ✅ Paramètres avancés pour contrôle fin

---

## 🚀 Démarrage en 3 étapes (15 minutes)

### ⚡ Installation Express (RECOMMANDÉE)

```bash
# 1. Installer FaceFusion (inclut toutes les dépendances)
cd facefusion
python install.py
cd ..

# 2. Installer Gradio pour l'interface
pip install gradio gradio-rangeslider

# 3. Lancer !
./launch.sh          # macOS/Linux
# ou
launch.bat           # Windows
```

**L'interface s'ouvre automatiquement dans votre navigateur !** 🌐

> **Note**: Si vous avez des erreurs, consultez [INSTALLATION_ALTERNATIVE.md](INSTALLATION_ALTERNATIVE.md)

---

## 📚 Documentation disponible

### Pour démarrer rapidement:
👉 **[GUIDE_DEMARRAGE_RAPIDE.md](GUIDE_DEMARRAGE_RAPIDE.md)** - Guide complet en 10 minutes

### Pour tout comprendre:
📖 **[README_APP.md](README_APP.md)** - Documentation complète
- Installation détaillée
- Guide d'utilisation complet
- Tous les paramètres expliqués
- Conseils pro
- Dépannage
- FAQ

### Pour les développeurs:
🔧 **[STRUCTURE_DU_PROJET.md](STRUCTURE_DU_PROJET.md)** - Architecture technique
- Structure des fichiers
- Flux de traitement
- Personnalisation
- Intégration FaceFusion

---

## 🎬 Votre premier face swap en 5 minutes

1. **Lancez l'application**:
   ```bash
   ./launch.sh  # ou launch.bat sur Windows
   ```

2. **Dans votre navigateur** (http://localhost:7860):
   - Uploadez une **photo** de votre acteur (portrait clair)
   - Uploadez une **vidéo courte** (5-10 sec pour tester)
   - Sélectionnez le preset **"⚡ Rapide"**
   - Cliquez sur **"🚀 Lancer le Face Swap"**

3. **Attendez** 30 secondes à 2 minutes

4. **Résultat** : Visionnez et téléchargez votre vidéo !

---

## 📁 Structure de vos fichiers

```
for facefusion/
├── actor_faceswap_studio.py      ← Votre application
├── launch.sh / launch.bat         ← Scripts de lancement
├── facefusion/                    ← Moteur FaceFusion
├── outputs/                       ← VOS RÉSULTATS SONT ICI ! 🎉
└── Documentation...
```

**Vos vidéos traitées** sont sauvegardées dans `outputs/`

---

## ⚙️ Configuration système recommandée

### Minimum (CPU uniquement):
- Python 3.10+
- 8 GB RAM
- Temps: ~5-10 min par minute de vidéo

### Recommandé (avec GPU):
- Python 3.10+
- 16 GB RAM
- GPU NVIDIA avec CUDA
- Temps: ~1-5 min par minute de vidéo ⚡

### Installation GPU (si vous avez NVIDIA):
```bash
pip uninstall onnxruntime
pip install onnxruntime-gpu
```

**Gain de performance: 5-10x plus rapide !**

---

## 🎯 Presets de qualité

| Preset | Usage | Temps (GPU) | Temps (CPU) |
|--------|-------|-------------|-------------|
| ⚡ **Rapide** | Tests et aperçus | ~1-2 min/min | ~5-10 min/min |
| ⚖️ **Équilibré** | Production (recommandé) | ~3-5 min/min | ~15-25 min/min |
| 💎 **Haute Qualité** | Qualité maximale | ~10-15 min/min | ~30-60 min/min |

---

## 💡 Workflow recommandé

1. **Test rapide**: Utilisez "Rapide" sur 5-10 secondes de vidéo
2. **Validation**: Si OK, passez à "Équilibré" pour un extrait de 30 sec
3. **Production**: Traitez la vidéo complète avec "Équilibré" ou "Haute Qualité"

---

## 🆘 Aide rapide

### L'application ne démarre pas ?
```bash
# Vérifiez Python
python --version  # Doit être 3.10+

# Réinstallez les dépendances
pip install -r requirements_app.txt --force-reinstall
```

### Erreur "No faces detected" ?
- ✅ Utilisez une photo avec visage clair et net
- ✅ Assurez-vous que le visage est bien visible

### Traitement trop lent ?
- ✅ Utilisez le preset "Rapide"
- ✅ Installez `onnxruntime-gpu` si vous avez un GPU NVIDIA
- ✅ Testez sur des vidéos courtes d'abord

### Résultat pas naturel ?
- ✅ Réduisez l'intensité du swap (0.7-0.8)
- ✅ Activez l'amélioration du visage
- ✅ Augmentez le flou du masque

**Plus de solutions** → [README_APP.md](README_APP.md#-dépannage)

---

## 🎓 Prochaines étapes

### Débutant:
1. ✅ Lisez le [GUIDE_DEMARRAGE_RAPIDE.md](GUIDE_DEMARRAGE_RAPIDE.md)
2. ✅ Faites votre premier test avec le preset "Rapide"
3. ✅ Expérimentez avec les différents presets

### Intermédiaire:
1. ✅ Explorez les paramètres avancés
2. ✅ Testez différents modèles de swap
3. ✅ Optimisez avec GPU si disponible
4. ✅ Lisez les conseils pro dans [README_APP.md](README_APP.md)

### Avancé:
1. ✅ Personnalisez les presets dans le code
2. ✅ Ajoutez vos propres fonctionnalités
3. ✅ Consultez [STRUCTURE_DU_PROJET.md](STRUCTURE_DU_PROJET.md)

---

## 📞 Support et ressources

### Documentation de cette app:
- 📘 Guide rapide: [GUIDE_DEMARRAGE_RAPIDE.md](GUIDE_DEMARRAGE_RAPIDE.md)
- 📖 Documentation complète: [README_APP.md](README_APP.md)
- 🏗️ Architecture: [STRUCTURE_DU_PROJET.md](STRUCTURE_DU_PROJET.md)

### FaceFusion (moteur):
- 🌐 Site officiel: https://docs.facefusion.io
- 💻 GitHub: https://github.com/facefusion/facefusion

---

## ✅ Checklist avant de commencer

Vérifiez que vous avez:

- [ ] Python 3.10+ installé
- [ ] ffmpeg installé (`brew install ffmpeg` sur macOS)
- [ ] FaceFusion installé (`cd facefusion && python install.py`)
- [ ] Dépendances installées (`pip install -r requirements_app.txt`)
- [ ] Une photo claire de votre acteur
- [ ] Une vidéo de test (commencez court: 5-10 sec)

**Tout est coché ?** 🎉

---

## 🚀 C'est parti !

```bash
# Lancez l'application
./launch.sh          # macOS/Linux
# ou
launch.bat           # Windows
```

**L'interface s'ouvre à**: http://localhost:7860

---

<center>

# 🎬 Bon Face Swapping ! ✨

**Des questions ?** → Consultez [README_APP.md](README_APP.md)

**Problème technique ?** → Section dépannage dans [README_APP.md](README_APP.md#-dépannage)

---

**Créé avec ❤️ pour simplifier le face swapping d'acteurs**

</center>
