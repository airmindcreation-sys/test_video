# 🎤 Feature: Synchronisation Labiale (Lip Sync)

## ✨ Nouvelle fonctionnalité ajoutée !

L'application intègre maintenant la **synchronisation labiale automatique** pour que les lèvres de l'acteur swappé bougent en parfaite synchronisation avec l'audio de la vidéo.

---

## 🎯 Pourquoi le Lip Sync ?

Quand vous faites un face swap sur une vidéo où l'acteur parle :
- ❌ **Sans lip sync** : Les lèvres du visage swappé ne correspondent pas aux paroles
- ✅ **Avec lip sync** : Les lèvres sont parfaitement synchronisées avec l'audio

**Résultat** : Un rendu beaucoup plus naturel et crédible !

---

## 🎛️ Contrôles dans l'interface

### Section "Synchronisation labiale (Lip Sync)"

#### 1. ✅ Activer le Lip Sync
- **Par défaut** : ✅ Activé
- **Recommandé** : Toujours activé si l'acteur parle dans la vidéo
- **Désactiver** : Seulement si la vidéo n'a pas de dialogue

#### 2. Modèle de Lip Sync
**Options disponibles** :
- **`wav2lip_gan`** (par défaut) - Wav2Lip GAN
  - ✅ Meilleure qualité
  - ✅ Synchronisation très précise
  - ❌ Plus lent (~20-30% plus long)

- **`wav2lip`** - Wav2Lip Standard
  - ✅ Plus rapide
  - ✅ Bonne synchronisation
  - ⚠️ Qualité légèrement inférieure

**Recommandation** : Utilisez `wav2lip_gan` pour la production finale

#### 3. Intensité du Lip Sync
- **Plage** : 0.5 - 1.0
- **Par défaut** : 0.9
- **0.5-0.7** : Synchronisation subtile (conserve plus du visage original)
- **0.8-0.9** : Équilibré (recommandé)
- **1.0** : Synchronisation maximale

---

## 🔄 Ordre de traitement

L'application traite la vidéo dans cet ordre :

```
1. Face Swap (remplacement du visage)
         ↓
2. Face Enhancer (amélioration qualité) [optionnel]
         ↓
3. Lip Syncer (synchronisation lèvres) [optionnel]
         ↓
4. Encodage vidéo final
```

**Important** : Le lip sync se fait APRÈS le face swap pour synchroniser le nouveau visage avec l'audio.

---

## ⚡ Impact sur les performances

### Temps de traitement avec Lip Sync

**Avec GPU CUDA (RTX A6000)** :

| Vidéo | Sans Lip Sync | Avec Lip Sync (wav2lip_gan) |
|-------|---------------|----------------------------|
| 1080p, 1 min | ~2-3 min | ~3-4 min (+30%) |
| 1080p, 5 min | ~10-15 min | ~13-20 min (+30%) |
| 1080p, 10 min | ~20-30 min | ~26-40 min (+30%) |

**Avec CPU uniquement** :
- Ajoutez ~50-70% de temps supplémentaire

**Conclusion** : Le lip sync ajoute environ 30% de temps de traitement, mais le résultat en vaut la peine !

---

## 💡 Conseils d'utilisation

### Quand utiliser le Lip Sync ?

✅ **Activez le Lip Sync si** :
- L'acteur parle dans la vidéo
- Il y a des dialogues
- Vous voulez un résultat ultra-réaliste

❌ **Désactivez le Lip Sync si** :
- La vidéo est muette
- L'acteur ne parle pas (plan large, action, etc.)
- Vous faites juste des tests rapides

### Optimiser la qualité

1. **Utilisez `wav2lip_gan`** pour la meilleure qualité
2. **Intensité à 0.9** pour un bon équilibre
3. **Activez Face Enhancer** pour améliorer le rendu des lèvres
4. **Audio clair** : Le lip sync fonctionne mieux avec un audio net

### Si le résultat n'est pas satisfaisant

1. **Réduisez l'intensité** à 0.7-0.8 (plus subtil)
2. **Essayez wav2lip standard** (parfois meilleur sur certaines vidéos)
3. **Vérifiez la qualité audio** de la vidéo source
4. **Testez sur un court extrait** avant de traiter la vidéo complète

---

## 🎨 Exemple de configuration recommandée

### Pour dialogues avec GPU :
```
Preset: Haute Qualité
Face Swapper Model: hyperswap_1a_256
Pixel Boost: 1024
Face Enhancer: ✅ Activé
Lip Sync: ✅ Activé
Lip Sync Model: wav2lip_gan
Lip Sync Weight: 0.9
```

### Pour tests rapides :
```
Preset: Rapide
Face Swapper Model: inswapper_128
Pixel Boost: 512
Face Enhancer: ❌ Désactivé
Lip Sync: ✅ Activé
Lip Sync Model: wav2lip
Lip Sync Weight: 0.8
```

---

## 🔧 Configuration technique

Les paramètres sont passés à FaceFusion via :

```python
config['processors'].append('lip_syncer')
config['lip_syncer_model'] = 'wav2lip_gan'  # ou 'wav2lip'
config['lip_syncer_weight'] = 0.9  # 0.5 - 1.0
```

Le processeur `lip_syncer` de FaceFusion :
- Analyse l'audio de la vidéo
- Détecte les mouvements de lèvres nécessaires
- Modifie les frames pour synchroniser les lèvres
- Préserve le reste du visage

---

## 📊 Comparaison des modèles

| Caractéristique | wav2lip | wav2lip_gan |
|----------------|---------|-------------|
| **Qualité** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Vitesse** | ⚡⚡⚡⚡⚡ | ⚡⚡⚡⚡ |
| **Précision sync** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Taille modèle** | ~50 MB | ~100 MB |
| **VRAM requise** | ~2 GB | ~3 GB |
| **Usage recommandé** | Tests, aperçus | Production finale |

---

## 🎬 Workflow recommandé

### Étape 1 : Test rapide (2-3 min)
```
- Extrait de 10 secondes de la vidéo
- Preset: Rapide
- Lip Sync: wav2lip (rapide)
- Valider que ça fonctionne
```

### Étape 2 : Ajustement (5-10 min)
```
- Extrait de 30 secondes
- Preset: Équilibré
- Lip Sync: wav2lip_gan
- Tester différentes intensités (0.8, 0.9, 1.0)
- Choisir la meilleure
```

### Étape 3 : Production (temps variable)
```
- Vidéo complète
- Preset: Haute Qualité
- Lip Sync: wav2lip_gan
- Intensité validée à l'étape 2
- Traiter la vidéo finale
```

---

## 🆘 Dépannage

### "Lip sync looks weird"
- Réduisez l'intensité à 0.7
- Essayez l'autre modèle (wav2lip vs wav2lip_gan)
- Vérifiez que l'audio est de bonne qualité

### "Processing is very slow"
- Le lip sync ajoute du temps (normal)
- Utilisez wav2lip au lieu de wav2lip_gan
- Vérifiez que CUDA est activé (GPU)

### "Lips don't match perfectly"
- Aucun lip sync n'est parfait à 100%
- wav2lip_gan donne les meilleurs résultats
- Augmentez l'intensité à 1.0 pour plus de précision

---

## ✅ Résumé

**Lip Sync** :
- ✅ **Activé par défaut** dans l'interface
- ✅ **Modèle par défaut** : wav2lip_gan (meilleure qualité)
- ✅ **Intensité par défaut** : 0.9 (bon équilibre)
- ✅ **Ajustable** : 2 modèles, intensité variable
- ✅ **Résultat** : Lèvres synchronisées avec l'audio pour un rendu ultra-réaliste

**Utilisez-le pour tous vos face swaps avec dialogues !** 🎤✨
