# FaceFusion CLI - Référence des Valeurs Valides

## Extrait directement de `python3 facefusion.py run --help`

### Face Swapper

**--face-swapper-model**
```
{blendswap_256, ghost_1_256, ghost_2_256, ghost_3_256, hififace_unofficial_256,
hyperswap_1a_256, hyperswap_1b_256, hyperswap_1c_256, inswapper_128,
inswapper_128_fp16, simswap_256, simswap_unofficial_512, uniface_256}
```

**--face-swapper-pixel-boost**
```
{256x256, 512x512, 768x768, 1024x1024}
```

**Note**: PAS de `128x128` ou `384x384` contrairement à ce qui était dans la recherche!

### Face Detector

**--face-detector-size**
```
{640x640}
```

**IMPORTANT**: Une seule valeur! Pas de 1024x1024!

### Face Enhancer

**--face-enhancer-model**
```
{codeformer, gfpgan_1.2, gfpgan_1.3, gfpgan_1.4, gpen_bfr_256, gpen_bfr_512,
gpen_bfr_1024, gpen_bfr_2048, restoreformer_plus_plus}
```

**--face-enhancer-blend**
```
[0..100:1]
```

### Lip Syncer

**--lip-syncer-model**
```
{edtalk_256, wav2lip_96, wav2lip_gan_96}
```

**IMPORTANT**:
- ❌ `wav2lip_gan` n'existe PAS!
- ✅ C'est `wav2lip_gan_96`!

**--lip-syncer-weight**
```
[0.0..1.0:0.05]
```

### Execution

**--execution-providers**
```
Multiples: cpu, cuda, coreml, etc.
```

**--execution-thread-count**
```
[1..32:1]
```

### Output

**--output-video-quality**
```
[0..100:1]
```

**--output-video-encoder**
```
{libx264, libx264rgb, libx265, libvpx-vp9, h264_videotoolbox, hevc_videotoolbox, rawvideo}
```

---

## Valeurs Utilisées dans l'App (Corrigées)

### Presets

**Rapide**:
- face_swapper_model: `inswapper_128`
- pixel_boost: `256x256` ✅
- face_enhancer: `gfpgan_1.4` ✅
- face_detector_size: `640x640` ✅
- lip_sync_model: `wav2lip_gan_96` ✅ (corrigé)

**Optimal**:
- face_swapper_model: `inswapper_128_fp16` ✅
- pixel_boost: `512x512` ✅
- face_enhancer: `codeformer` ✅
- face_detector_size: `640x640` ✅
- lip_sync_model: `wav2lip_gan_96` ✅ (corrigé)

**Haute Qualité**:
- face_swapper_model: `inswapper_128_fp16` ✅
- pixel_boost: `1024x1024` ✅
- face_enhancer: `codeformer` ✅
- face_detector_size: `640x640` ✅
- lip_sync_model: `wav2lip_gan_96` ✅ (corrigé)

---

## Erreurs Corrigées

1. ❌ `wav2lip_gan` → ✅ `wav2lip_gan_96`
2. ❌ `wav2lip` → ✅ `wav2lip_96`
3. ❌ `face_detector_size: 1024x1024` → ✅ `640x640`
4. ❌ `pixel_boost: 512` → ✅ `512x512`

---

Date: 2024-12-16
Version FaceFusion: 3.3.2
