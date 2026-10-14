# ⚡ Nexus Content Engine — Plataforma de Mídia Programática & Vídeos Verticais

Sistema modular e automatizado de curadoria, roteirização neural, renderização 9:16 e distribuição em escala de vídeos curtos para YouTube Shorts, TikTok e Instagram Reels.

---

## 🏛️ Governança Institucional & Padrão Tear

O **Nexus Content Engine** segue os mesmos rigorosos princípios de engenharia de software, auditorias de 4 lanes, orçamentos assintóticos e documentação viva que regem os projetos **Pulsense**, **Doc2Fill** e **Call-in**:

* **Documentação Canônica Viva:** Disponível em [`/documentation`](documentation/).
* **Ponteiro do Cânone:** [GEMINI.md](GEMINI.md).
* **Histórico de Mudanças:** [CHANGELOG.md](CHANGELOG.md).

---

## 🎯 1. Visão Geral da Plataforma

O **Nexus Content Engine** foi projetado para atuar como uma infraestrutura agnóstica de mídia vertical, capaz de transformar qualquer tema ou pauta em vídeos de alta retenção sem necessidade de gravação manual ou edição tradicional.

* **Nicho Flagship Inicial (Preset #1):** **GTA 6 (Grand Theft Auto VI)** — focado em capturar a maior onda de atenção e demanda reprimida da história dos games.
* **Arquitetura Multi-Nicho:** O motor é 100% genérico. Novos nichos (tecnologia, curiosidades, finanças, cinema) podem ser ativados apenas apontando para novas pastas de B-Roll e templates de prompts.
* **Foco Estratégico:** **Via A (Crescimento de Ativos Próprios)** com monetização híbrida imediata (afiliados gamer + patrocínios) enquanto constrói audiência proprietária.
* **Governança Operacional:** Divisão clara entre infraestrutura de código (**Kazu**) e operação/distribuição diária de conteúdo (**Jayp**), mantendo o tempo do Kazu protegido para o *Pulsense* e *Call-in*.

---

## 🏗️ 2. Arquitetura da Máquina de Conteúdo

```
┌──────────────────┐       ┌──────────────────┐       ┌──────────────────┐
│   1. CURADORIA   │       │  2. ROTEIRO IA   │       │  3. ÁUDIO & TTS  │
│  Reddit / X /    │ ────> │  Gemini Flash    │ ────> │ Edge-TTS neural  │
│  Fontes Oficiais │       │  Hooks de 3 seg  │       │ ou ElevenLabs    │
└──────────────────┘       └──────────────────┘       └──────────────────┘
                                                               │
                                                               ▼
┌──────────────────┐       ┌──────────────────┐       ┌──────────────────┐
│ 5. DISTRIBUIÇÃO  │       │ 4. RENDERIZAÇÃO  │       │ B-ROLL 4K GAME   │
│ Shorts / Reels   │ <──── │ FFmpeg + Whisper │ <──── │ Clipes sem HUD   │
│ TikTok diário    │       │ Legenda Karaoke  │       │ Gameplay / RDR2  │
└──────────────────┘       └──────────────────┘       └──────────────────┘
```

---

## 📚 3. Documentação Técnica & Registro Acadêmico

Toda a fundamentação formal do projeto está versionada no repositório:

* 📜 **[Tratado Acadêmico de Síntese Neural de Vídeo](documentation/TRATADO-ENGENHARIA-ESTEIRAS-VIDEO-NEURAL.md):** Fundamentação matemática da curva de retenção de dopamina, alinhamento fonético temporal via DTW e análise de complexidade.
* ⚡ **[Nexus Suite: Especificação & Análise Comparativa](documentation/BENCHMARK-COMPETITIVO-E-ESPECIFICACAO-NEXUS.md):** Arquitetura proprietária dos 8 módulos Nexus (NexusScale, NexusScrap, NexusRepost, etc.), estratégia multi-nicho e viabilidade econômica.
* 🏛️ **[Manual de Arquitetura de Software](documentation/ARCHITECTURE.md):** Arquitetura Hexagonal, orçamentos técnicos de latência, SLAs e separação Core vs. Presets.
* 📋 **[Especificação Formal de Requisitos (EARS)](documentation/REQUIREMENTS.md):** Declarações formais de comportamento do sistema.
* 📖 **[Playbook de Prospecção & Crescimento da Via A (Nicho GTA 6)](docs/PROSPECCAO-VIA-A-GTA6.md):** Estratégia de atração de tráfego, ganchos e afiliados gamer.
* 🕹️ **[Manual de Operação Diária do Jayp](docs/MANUAL-OPERACAO-JAYP.md):** A rotina de 25 min/dia de operação.
* 🌿 **[Guia Prático de Git Worktree](docs/WORKTREE-GUIDE.md):** Isolamento de branches para trabalho concorrente.

---

## 👥 4. Divisão de Papéis (Kazu & Jayp)

| Frente | Responsável | Carga de Tempo | Missão Principal |
| :--- | :--- | :--- | :--- |
| **Infraestrutura & Código** | **Kazu** | ~1h a 2h / semana | Manter a engine técnica, otimizar renderizadores, prompts e novas integrações. |
| **Operação & Audiência** | **Jayp** | ~20 a 30 min / dia | Curadoria de pautas, disparo da esteira, revisão final de vídeo e postagem nos canais. |

---

## 🚀 5. Primeiros Passos

1. Navegar até o diretório do projeto:
   ```bash
   cd ~/Projetos/nexus-content-engine
   ```
2. Instalar dependências Python:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Rodar a esteira de teste:
   ```bash
   # Geração no nicho flagship (GTA 6)
   python3 src/main.py --topic "física de água do gta 6" --niche gta6

   # Geração em nicho genérico
   python3 src/main.py --topic "modelos locais de inteligência artificial" --niche tech
   ```
4. Executar os testes automatizados:
   ```bash
   python3 -m unittest discover tests
   ```
