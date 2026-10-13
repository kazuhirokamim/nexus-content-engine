#!/usr/bin/env bash
# ==============================================================================
# ⚡ NEXUS CONTENT ENGINE — Script de Instalação Automática (One-Click Setup)
# Feito para o operador: Jayp (JotaDEV661)
# ==============================================================================

set -e

echo ""
echo "============================================================"
echo "🌴 BEM-VINDO AO NEXUS CONTENT ENGINE — OPERAÇÃO GTA 6"
echo "============================================================"
echo "⚡ Configurando seu ambiente de produção em segundos..."
echo ""

# 1. Verifica se o Python 3 está presente
if ! command -v python3 &> /dev/null; then
    echo "❌ Erro: Python 3 não foi encontrado. Por favor, instale o Python 3."
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "✅ Python detectado: $PYTHON_VERSION"

# 2. Criação do Ambiente Virtual (.venv)
if [ ! -d ".venv" ]; then
    echo "📦 Criando ambiente virtual isolado (.venv)..."
    python3 -m venv .venv
else
    echo "✅ Ambiente virtual (.venv) já existente."
fi

# 3. Ativação e Instalação de Dependências
echo "📥 Instalando dependências (Áudio Neural, FFmpeg e IA)..."
source .venv/bin/activate
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet

# 4. Verificação de Integridade do FFmpeg
echo "🔍 Validando executável FFmpeg embutido..."
.venv/bin/python3 -c "import imageio_ffmpeg; print('   ✅ FFmpeg pronto:', imageio_ffmpeg.get_ffmpeg_exe())"

# 5. Criar pastas operacionais caso não existam
mkdir -p output presets/gta6/b_roll

echo ""
echo "============================================================"
echo "🎉 AMBIENTE 100% PRONTO PARA USO!"
echo "============================================================"
echo ""
echo "👉 Como gerar seu primeiro vídeo:"
echo "   source .venv/bin/activate"
echo "   python run_operator.py --topic 'Sua notícia quente do GTA 6 aqui'"
echo ""
echo "👉 Ou use o modo interativo (ele te pede a pauta na tela):"
echo "   python run_operator.py"
echo ""
echo "Seu vídeo cairá pronto para postar na pasta 'output/'."
echo "Boa escala! 🚀"
echo ""
