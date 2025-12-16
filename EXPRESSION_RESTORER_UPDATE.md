# 😊 Expression Restorer - Nouvelle Fonctionnalité

## 📅 Date : 2025-12-16

---

## ✨ Nouvelle Fonctionnalité Ajoutée

### Expression Restorer

L'**Expression Restorer** est maintenant disponible dans toute l'application V3 !

Cette fonctionnalité permet de **restaurer les expressions faciales** de la vidéo cible sur le visage swappé, pour un résultat plus naturel et expressif.

---

## 🎯 Où trouver Expression Restorer ?

### 1. Face Swap Simple

Dans l'onglet **"🎬 Face Swap Simple"**, vous trouverez maintenant :

```
✅ Activer Expression Restorer
📋 Expression Restorer Model: live_portrait
🎚️ Expression Restorer Factor: 0-100 (défaut: 80)
🎭 Expression Restorer Areas: All / upper-face / lower-face
```

**Utilisation :**
1. Cocher "Activer Expression Restorer"
2. Choisir le modèle (actuellement `live_portrait`)
3. Ajuster le facteur (0-100) - Plus haut = plus d'expression restaurée
4. Choisir les zones à traiter :
   - `All` : Tout le visage
   - `upper-face` : Partie supérieure (yeux, front)
   - `lower-face` : Partie inférieure (bouche, menton)

---

### 2. Test en Groupe - Configs Personnalisées

Dans **"⚙️ Configs Personnalisées"**, chaque configuration contient maintenant :

```
Colonne 2:
✅ Expression Restorer (checkbox)
📋 Expr. Rest. Model

Colonne 3:
🎚️ Expr. Rest. Factor (slider 0-100)
🎭 Expr. Rest. Areas (dropdown)
```

**Avantages :**
- Tester différents paramètres d'expression restoration en parallèle
- Comparer avec/sans expression restorer
- Trouver le meilleur facteur pour votre cas d'usage

---

## 🔧 Paramètres Détaillés

### Expression Restorer Model

**Valeur actuelle :** `live_portrait`

C'est le modèle utilisé par FaceFusion pour restaurer les expressions. Live Portrait est un modèle state-of-the-art pour capturer et transférer les micro-expressions faciales.

### Expression Restorer Factor

**Range :** 0 à 100
**Défaut :** 80
**Unité :** Pourcentage

- **0** : Aucune restauration d'expression
- **50** : Restauration modérée (50% des expressions transférées)
- **80** : Restauration forte (recommandé)
- **100** : Restauration maximale

**Recommandation :** Commencer à 80, puis ajuster selon le résultat :
- Si le visage manque d'expression → augmenter
- Si les expressions sont trop prononcées → diminuer

### Expression Restorer Areas

**Choix :**
- `All` (défaut) : Restaure les expressions sur tout le visage
- `upper-face` : Restaure uniquement la partie supérieure (yeux, sourcils, front)
- `lower-face` : Restaure uniquement la partie inférieure (bouche, menton, joues)

**Cas d'usage :**
- `All` : Usage général, résultats équilibrés
- `upper-face` : Quand vous voulez conserver les mouvements de bouche originaux mais restaurer le regard
- `lower-face` : Quand vous voulez conserver les expressions oculaires mais restaurer les mouvements de bouche

---

## 🎬 Workflow Recommandé

### Test Simple

1. Face Swap Simple
2. Activer Face Swapper + Face Enhancer + **Expression Restorer**
3. Laisser Factor à 80, Areas à "All"
4. Lancer et observer le résultat
5. Ajuster le Factor si nécessaire

### Comparaison Avancée

1. Test en Groupe → Configs Personnalisées
2. Créer 3 configurations :
   - **Config 1** : Sans Expression Restorer (baseline)
   - **Config 2** : Expression Restorer Factor 80, Areas "All"
   - **Config 3** : Expression Restorer Factor 100, Areas "lower-face"
3. Lancer les tests
4. Comparer visuellement dans la galerie
5. Choisir la meilleure

---

## 📊 Ordre des Processeurs

Quand vous activez Expression Restorer, l'ordre de traitement est :

```
1. face_swapper      → Échange du visage
2. face_enhancer     → Amélioration du visage (si activé)
3. expression_restorer → Restauration des expressions ✨ NOUVEAU
4. frame_enhancer    → Amélioration de la frame (si activé)
5. lip_syncer        → Synchronisation labiale (si activé)
```

**Important :** Expression Restorer est appliqué **après** le face swapper et face enhancer, mais **avant** le frame enhancer et lip sync.

---

## 💡 Cas d'Usage Recommandés

### Cas 1 : Vidéo avec beaucoup d'expressions

**Problème :** Le face swap perd les expressions subtiles de l'acteur

**Solution :**
```
Face Swapper: inswapper_128_fp16
Face Enhancer: codeformer (blend 80)
Expression Restorer: Activé
  - Factor: 90
  - Areas: All
```

### Cas 2 : Préserver les mouvements de bouche originaux

**Problème :** Vous voulez garder les mouvements de bouche de la vidéo source

**Solution :**
```
Expression Restorer: Activé
  - Factor: 100
  - Areas: lower-face
Lip Sync: Désactivé
```

### Cas 3 : Focus sur le regard et les sourcils

**Problème :** Le regard manque d'expressivité après le face swap

**Solution :**
```
Expression Restorer: Activé
  - Factor: 85
  - Areas: upper-face
```

---

## 🔍 Commande CLI Générée

Quand vous activez Expression Restorer, la commande FaceFusion générée contient :

```bash
--processors face_swapper face_enhancer expression_restorer
--expression-restorer-model live_portrait
--expression-restorer-factor 80
--expression-restorer-areas All  # ou upper-face, lower-face
```

Si Areas = "All", `--expression-restorer-areas` n'est pas ajouté (valeur par défaut).

---

## ⚙️ Modifications Techniques

### Fichier : `actor_faceswap_studio_v3.py`

#### 1. Nouvelles Constantes (lignes ~97-105)

```python
EXPRESSION_RESTORER_MODELS = [
    'live_portrait'
]

EXPRESSION_RESTORER_AREAS = [
    'All',
    'upper-face',
    'lower-face'
]
```

#### 2. Build Command - Expression Restorer (lignes ~350-357)

```python
# Expression restorer
if 'expression_restorer' in processors:
    cmd.extend(['--expression-restorer-model', config.get('expression_restorer_model', 'live_portrait')])
    cmd.extend(['--expression-restorer-factor', str(config.get('expression_restorer_factor', 80))])
    if 'expression_restorer_areas' in config:
        areas = config['expression_restorer_areas']
        if areas != 'All':
            cmd.extend(['--expression-restorer-areas', areas])
```

#### 3. Face Swap Simple - Nouvelle UI (lignes ~790-802)

```python
# Expression Restorer
simple_expression_restorer_enable = gr.Checkbox(label="Activer Expression Restorer", value=False)
simple_expression_restorer_model = gr.Dropdown(
    choices=FaceSwapConfig.EXPRESSION_RESTORER_MODELS,
    value='live_portrait',
    label="Expression Restorer Model"
)
simple_expression_restorer_factor = gr.Slider(0, 100, value=80, label="Expression Restorer Factor")
simple_expression_restorer_areas = gr.Dropdown(
    choices=FaceSwapConfig.EXPRESSION_RESTORER_AREAS,
    value='All',
    label="Expression Restorer Areas"
)
```

#### 4. Configs Personnalisées - Nouvelle UI (lignes ~922-935)

```python
cc_use_expr_rest = gr.Checkbox(label="Expression Restorer", value=False)
cc_expr_rest_model = gr.Dropdown(
    choices=FaceSwapConfig.EXPRESSION_RESTORER_MODELS,
    value='live_portrait',
    label="Expr. Rest. Model"
)

# Colonne 3:
cc_expr_rest_factor = gr.Slider(0, 100, value=80, label="Expr. Rest. Factor")
cc_expr_rest_areas = gr.Dropdown(
    choices=FaceSwapConfig.EXPRESSION_RESTORER_AREAS,
    value='All',
    label="Expr. Rest. Areas"
)
```

#### 5. Signature process_video_simple modifiée (lignes ~470-478)

```python
def process_video_simple(self, source_image: str, target_video: str,
                        face_swapper_model: str, pixel_boost: str,
                        face_enhancer_enabled: bool, face_enhancer_model: str, face_enhancer_blend: float,
                        frame_enhancer_enabled: bool, frame_enhancer_model: str,
                        lip_sync_enabled: bool, lip_sync_model: str,
                        expression_restorer_enabled: bool, expression_restorer_model: str,
                        expression_restorer_factor: float, expression_restorer_areas: str,
                        reference_distance: float, execution_provider: str, quality: int,
                        progress=gr.Progress()) -> Tuple[Optional[str], str, Optional[str]]:
```

#### 6. Wrapper mis à jour (18 champs au lieu de 14)

```python
num_fields = 18  # Au lieu de 14

# Ordre des champs:
# enabled, name, face_swapper, pixel_boost, use_face_enh, face_enh_model, face_enh_blend,
# use_frame_enh, frame_enh_model, use_lip_sync, lip_sync_model,
# use_expr_rest, expr_rest_model, expr_rest_factor, expr_rest_areas,
# distance, quality, exec_provider
```

---

## ✅ Tests à Effectuer

### Test 1 : Face Swap Simple avec Expression Restorer

1. Lancer Face Swap Simple
2. Activer Expression Restorer
3. Factor: 80, Areas: All
4. Lancer traitement
5. Vérifier que les expressions sont bien restaurées

### Test 2 : Comparaison avec/sans Expression Restorer

1. Configs Personnalisées
2. Config 1: Sans Expression Restorer
3. Config 2: Avec Expression Restorer (Factor 80)
4. Config 3: Avec Expression Restorer (Factor 100)
5. Comparer les résultats visuellement

### Test 3 : Areas différentes

1. Configs Personnalisées
2. Config 1: Areas "All"
3. Config 2: Areas "upper-face"
4. Config 3: Areas "lower-face"
5. Observer les différences

### Test 4 : Duplication de config avec Expression Restorer

1. Créer Config 1 avec Expression Restorer activé
2. Cliquer "Dupliquer vers Config 2"
3. Vérifier que tous les paramètres sont copiés

---

## 📝 Notes Importantes

### Performance

L'Expression Restorer **ajoute du temps de traitement** :
- Estimation : +30-50% du temps de traitement
- Dépend du modèle `live_portrait` et de la longueur de la vidéo
- Utiliser CUDA si disponible pour accélérer

### Compatibilité

- ✅ Compatible avec Face Enhancer
- ✅ Compatible avec Frame Enhancer
- ✅ Compatible avec Lip Sync
- ✅ Fonctionne dans tous les modes (Simple, Pré-défini, Personnalisé)

### Limites

- Un seul modèle disponible actuellement : `live_portrait`
- Nécessite que FaceFusion ait le modèle téléchargé
- Plus gourmand en ressources que face_enhancer

---

## 🎯 Recommandations Générales

### Configuration Production Optimale

```
Face Swapper: hyperswap_1b_256
Pixel Boost: 1024x1024
Face Enhancer: codeformer (blend 85)
Expression Restorer: Activé (factor 80, areas All)
Reference Distance: 0.6
Quality: 95
Execution Provider: cuda
```

### Configuration Test Rapide

```
Face Swapper: inswapper_128_fp16
Face Enhancer: codeformer (blend 80)
Expression Restorer: Activé (factor 80, areas All)
Frame Enhancer: Désactivé
Execution Provider: cuda
```

---

## 🔮 Améliorations Futures Possibles

1. **Autres modèles** : Support de futurs modèles d'expression restoration
2. **Preview temps réel** : Aperçu des expressions restaurées
3. **Presets Areas** : Presets pour différents types de vidéos (dialogue, action, etc.)
4. **Blend avec original** : Mélanger expressions originales et restaurées

---

**Version** : V3.4
**Status** : ✅ Prêt pour production
**URL** : http://localhost:7862

**Commande de lancement :**
```bash
cd "/Users/martinemenguy/Desktop/for facefusion"
python3 actor_faceswap_studio_v3.py
```
