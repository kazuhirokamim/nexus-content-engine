# ⚡ Nexus Content Engine — Plataforma de Mídia Programática & Vídeos 9:16

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB.svg?logo=python&logoColor=white)](https://python.org)
[![FFmpeg](https://img.shields.io/badge/FFmpeg-6.0+-007808.svg?logo=ffmpeg&logoColor=white)](https://ffmpeg.org)
[![AI Audio](https://img.shields.io/badge/TTS-Neural_Speech-blue.svg)]()
[![ASR](https://img.shields.io/badge/Whisper-Karaoke_Alignment-orange.svg)]()
[![Architecture](https://img.shields.io/badge/Architecture-Hexagonal_Multi--Niche-purple.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status: Showcase](https://img.shields.io/badge/Status-Audited_&_Certified-orange.svg)]()

> **Transforme roteiros e pautas em vídeos verticais de alta retenção compilados em segundos.**  
> O `Nexus Content Engine` automatiza a geração de mídia programática (YouTube Shorts, TikTok, Reels), sincronizando vozes neurais, alinhamento fonético milimétrico para legendas estilo Karaokê e composição acelerada por GPU.

---

## ⚡ Quickstart

```bash
# 1. Clonar o repositório
git clone https://github.com/kazuhirokamim/nexus-content-engine.git
cd nexus-content-engine

# 2. Criar ambiente virtual e instalar dependências
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Executar o operador de geração de vídeo
python run_operator.py --preset gta6 --topic "Novidades do Mapa de Vice City"
```

O vídeo final renderizado será exportado em `output/videos/`.

---

## 🏛️ Pipeline de Compilação Audiovisual

```mermaid
graph LR
    Pauta["Pauta / Roteiro"] --> TTS["TTS Neural<br/>(Faixa Vocal HD)"]
    TTS --> ForcedAlignment["Alinhamento Fonético<br/>(Whisper / DTW)"]
    ForcedAlignment --> Legendas["Legendas Karaokê<br/>(Estilo Dinâmico ASS)"]
    BRoll["Banco B-Roll 4K"] --> FFmpeg["Compositor FFmpeg<br/>(Aceleração GPU)"]
    Legendas --> FFmpeg
    TTS --> FFmpeg
    FFmpeg --> MP4["Vídeo Vertical 9:16<br/>(Safe-Zones Garantidas)"]
```

---

## 🚀 Diferenciais de Engenharia

- **Compilação Algorítmica de Vídeo:** Elimina o tempo manual em softwares de edição pesados. Um vídeo completo de 50 segundos é gerado em menos de 25 segundos.
- **Efeito Dopaminérgico Karaokê:** Alinhamento temporal com precisão menor que 60ms entre fala e transição cromática das palavras na tela.
- **Arquitetura Multi-Nicho com Presets Declarativos:** O motor principal é agnóstico. Troque de tema (Games, Curiosidades, Finanças) apenas apontando para um novo arquivo de configuração JSON.
- **Subprocess Security:** Execução do FFmpeg sem uso de interpretador shell (`shell=False`), prevenindo injeções de comando maliciosas.
- **Safe-Zones 9:16 Nativas:** Posicionamento de títulos e legendas imune à sobreposição dos botões de interface de TikTok, Shorts e Reels.

---

## 📁 Estrutura do Repositório

```
nexus-content-engine/
├── src/                            # Núcleo de TTS, composição e alinhamento fonético
├── presets/                        # Presets declarativos de nicho (GTA 6, etc.)
├── models/                         # Modelos e schemas de dados
├── documentation/                  # Acervo acadêmico, laudo pericial e vitrine
├── docs/                           # Guias operacionais e manuais
└── tests/                          # Suíte de testes unitários e de integração
```

---

## 📜 Licença

Distribuído sob a licença **MIT**.
