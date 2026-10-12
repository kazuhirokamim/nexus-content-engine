# 🌴 GTA 6 Content Engine — Máquina de Conteúdo & Perfis Dark

Sistema automatizado de curadoria, roteirização neural, renderização 9:16 e distribuição em escala de vídeos curtos sobre o universo de **Grand Theft Auto VI**.

---

## 🎯 1. Visão Geral do Projeto

O **GTA 6 Content Engine** foi projetado para capturar a maior onda de atenção orgânica da história dos videogames. Em vez de produzir vídeos manualmente ou assinar ferramentas caras e engessadas (como ViceScale), este projeto utiliza uma esteira em código aberta, customizável e de baixíssimo custo.

* **Foco Estratégico:** **Via A (Crescimento de Ativos Próprios)** com monetização híbrida imediata (afiliados gamer + parcerias orgânicas) enquanto constrói audiência massiva até o lançamento do jogo.
* **Governança Operacional:** Divisão clara entre infraestrutura de código (**Kazu**) e operação/distribuição diária de conteúdo (**Jayp**), mantendo o tempo do Kazu protegido para o *Pulsense* e *Call-in*.

---

## 🏗️ 2. Arquitetura da Máquina de Conteúdo

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│   1. CURADORIA  │       │  2. ROTEIRO IA  │       │  3. ÁUDIO & TTS │
│  Reddit / X /   │ ────> │  Gemini Flash   │ ────> │ Edge-TTS neural │
│  Fontes Oficiais│       │  Hooks de 3 seg │       │ ou ElevenLabs   │
└─────────────────┘       └─────────────────┘       └─────────────────┘
                                                             │
                                                             ▼
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│ 5. DISTRIBUIÇÃO │       │ 4. RENDERIZAÇÃO │       │ B-ROLL 4K GAME  │
│ Shorts / Reels  │ <──── │ FFmpeg + Whisper│ <──── │ Clipes sem HUD  │
│ TikTok diário   │       │ Legenda Karaoke │       │ Gameplay / RDR2 │
└─────────────────┘       └─────────────────┘       └─────────────────┘
```

---

## 👥 3. Divisão de Papéis (Kazu & Jayp)

| Frente | Responsável | Carga de Tempo | Missão Principal |
| :--- | :--- | :--- | :--- |
| **Infraestrutura & Código** | **Kazu** | ~1h a 2h / semana | Manter os scripts de automação, renderizador FFmpeg e integrações de IA funcionando. |
| **Operação & Audiência** | **Jayp** | ~20 a 30 min / dia | Curadoria de pautas, disparo da esteira, revisão final de vídeo e postagem nos canais. |

Consulte o [Manual de Operação do Jayp](docs/MANUAL-OPERACAO-JAYP.md) para o passo a passo detalhado da rotina diária.

---

## 📚 4. Documentação de Apoio

* 📖 [Playbook de Prospecção & Crescimento da Via A](docs/PROSPECCAO-VIA-A-GTA6.md)
* 📋 [Manual de Operação Diária do Jayp](docs/MANUAL-OPERACAO-JAYP.md)
* 🌿 [Guia Prático de Git Worktree para Trabalho Paralelo](docs/WORKTREE-GUIDE.md)

---

## 🚀 5. Primeiros Passos

1. Clonar ou navegar até o diretório do projeto:
   ```bash
   cd ~/Projetos/gta6-content-engine
   ```
2. Instalar dependências Python:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Rodar a esteira de teste:
   ```bash
   python3 src/main.py --topic "física de água do gta 6"
   ```
