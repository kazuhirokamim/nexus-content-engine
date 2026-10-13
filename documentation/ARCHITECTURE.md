# 🏛️ Arquitetura do Sistema — Nexus Content Engine

**Documento:** `/documentation/ARCHITECTURE.md`  
**Governança:** Cânone Tear & Noesis Architecture Swarm  
**Status:** Documento Vivo (Rule #1 & #13)  
**Autor:** Philip Kazuhiro Kamimura (Kazu) & Conselho Técnico

---

## 🧭 1. Princípios de Engenharia e Visão Arquitetural

O **Nexus Content Engine** é uma plataforma de mídia programática desenhada sob o padrão de **Arquitetura Hexagonal (Ports and Adapters)**, garantindo desacoplamento estrito entre a lógica pura de retenção algorítmica e os adaptadores de infraestrutura (motores de áudio, renderizadores de vídeo e APIs sociais).

```
                      ┌─────────────────────────────────────────┐
                      │             PRESETS (NICHOS)            │
                      │  [gta6]  [tech]  [finance]  [cinema]    │
                      └────────────────────┬────────────────────┘
                                           │
                                           ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                   NEXUS CORE (DOMÍNIO PURO)                             │
│                                                                                         │
│   ┌────────────────────────┐   ┌────────────────────────┐   ┌───────────────────────┐   │
│   │   ScriptGenerator      │   │   PsychologyEngine     │   │   DynamicLoopEngine   │   │
│   │   (Hooks de 3 segundos)│   │   (Retenção Dopamina)  │   │   (Continuidade Vídeo)│   │
│   └────────────────────────┘   └────────────────────────┘   └───────────────────────┘   │
└──────────────┬───────────────────────────┬──────────────────────────┬───────────────────┘
               │                           │                          │
               ▼                           ▼                          ▼
      [PORT: AudioSynthesizer]     [PORT: VideoAssembler]     [PORT: SocialPublisher]
               │                           │                          │
               ▼                           ▼                          ▼
   ┌──────────────────────┐    ┌──────────────────────┐   ┌───────────────────────┐
   │ ADAPTER: Edge-TTS /  │    │ ADAPTER: FFmpeg      │   │ ADAPTER: Meta Graph / │
   │ ElevenLabs           │    │ (VideoToolbox/NVENC) │   │ TikTok Business API   │
   └──────────────────────┘    └──────────────────────┘   └───────────────────────┘
```

---

## 🧩 2. Separação de Camadas (Core vs. Presets)

1. **Camada Core (`src/core/`):**
   * Totalmente agnóstica a qualquer tema ou jogo específico.
   * Contém contratos de interface, orquestrador de renderização, gerador de legendas e cálculos de alinhamento temporal.
2. **Camada de Presets (`presets/<nicho>/`):**
   * Configurações de vocabulário, prompts especializados, biblioteca de B-roll (clipes brutos) e links de monetização/afiliados.
   * O preset flagship **`presets/gta6`** opera como o primeiro módulo de alta demanda.
3. **Camada de Aplicação / CLI (`src/`):**
   * Pontos de entrada para operadores humanos (Jayp) e ferramentas de automação (MCP, cron jobs, filas assíncronas).

---

## ⚡ 3. Orçamentos Técnicos & SLAs (Noesis Budget Controller)

* **Orçamento de Linhas de Código (Regra Tear #24):** Máximo de **700 linhas por arquivo** de produção. Ao atingir 600 linhas, modularização imediata.
* **Orçamento de Latência de Renderização:**
  * Vídeo vertical de 45 segundos em 1080x1920 @ 60 FPS: $\le 30$ segundos de renderização no macOS via aceleração de hardware `h264_videotoolbox`.
* **Complexidade Assintótica:**
  * Alinhamento fonético de legendas: $\mathcal{O}(N)$ onde $N$ é o número de tokens do roteiro.
  * Composição de vídeo: $\mathcal{O}(M)$ onde $M$ é a contagem de frames lineares, sem re-encoding redundante de streams estáticos.
* **Consumo de Memória:** Teto de 512 MB de RAM por processo de renderização em lote.

---

## 🛡️ 4. Segurança, LGPD & Integridade (Regras #8 & #28)

1. **Minimização de Dados:** Nenhum dado pessoal identificável (PII) é coletado ou armazenado na geração de vídeo.
2. **Isolamento de Credenciais:** Proibido credenciais ou tokens em código-fonte. Chaves de API (`GEMINI_API_KEY`, tokens sociais) são injetadas estritamente via variáveis de ambiente (`.env`).
3. **Sandbox de Execução:** Execução de subprocessos de sistema (`ffmpeg`) com validação estrita de argumentos e escapes para evitar injeção de comandos.
