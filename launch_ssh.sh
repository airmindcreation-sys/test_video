#!/bin/bash

# 🎬 Actor Face Swap Studio - Lancement pour connexion SSH
# Pour accès distant depuis une autre machine

echo "=================================="
echo "🎬 Actor Face Swap Studio (SSH)"
echo "=================================="
echo ""

# Vérifier que Python est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé"
    exit 1
fi

echo "✅ Python détecté"

# Détecter l'adresse IP locale
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    IP_ADDRESS=$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || echo "localhost")
else
    # Linux
    IP_ADDRESS=$(hostname -I | awk '{print $1}' || echo "localhost")
fi

echo "🌐 Adresse IP de cette machine: $IP_ADDRESS"
echo ""
echo "📡 L'application sera accessible sur:"
echo "   • Depuis cette machine: http://localhost:7860"
echo "   • Depuis le réseau local: http://$IP_ADDRESS:7860"
echo "   • Depuis SSH (tunnel): http://localhost:7860 (voir instructions ci-dessous)"
echo ""
echo "=================================="
echo ""

# Lancer l'application en mode SSH (sans ouvrir le navigateur)
python3 -c "
import sys
import os

# Ajouter le chemin de FaceFusion
sys.path.insert(0, 'facefusion')
os.environ['OMP_NUM_THREADS'] = '1'

from pathlib import Path
from facefusion import state_manager, logger
from facefusion.execution import get_available_execution_providers

# Import de l'application
exec(open('actor_faceswap_studio.py').read())

# Modifier le lancement pour SSH
import actor_faceswap_studio as app_module

# Créer l'interface
app = app_module.create_gradio_interface()

print('\n' + '='*60)
print('✅ Application lancée en mode SSH !')
print('='*60)
print('')
print('🔗 ACCÈS DEPUIS VOTRE MACHINE LOCALE (via tunnel SSH):')
print('')
print('   Sur votre machine locale, ouvrez un terminal et tapez:')
print('   ssh -L 7860:localhost:7860 votre_utilisateur@$IP_ADDRESS')
print('')
print('   Puis ouvrez dans votre navigateur:')
print('   http://localhost:7860')
print('')
print('='*60)
print('📊 Logs en direct ci-dessous...')
print('='*60)
print('')

# Lancer sans ouvrir le navigateur
app.launch(
    server_name='0.0.0.0',
    server_port=7860,
    share=False,
    inbrowser=False,  # Ne pas ouvrir le navigateur en SSH
    show_error=True
)
"
