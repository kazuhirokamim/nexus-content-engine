---
numero: 2
titulo: Síntese Neural Acústica Local, Alinhamento Milissegundo e Dynamic B-Roll
data: 2026-10-13
status: Aceito
autores:
  - Philip Kazuhiro Kamimura
  - Noesis Architecture Maestro
  - Tear Maestro
aplica_a:
  - src/core
  - tests
  - presets
tags:
  - video
  - piper-tts
  - whisper
  - b-roll
  - karaoke
---

# ADR-002: Síntese Neural Acústica Local, Alinhamento Milissegundo e Dynamic B-Roll

## Contexto e Declaração do Problema

No contexto de evolução do Nexus Content Engine para competir diretamente com o padrão comercial do ViceScale, enfrentando as limitações do protótipo inicial onde a voz gTTS soava lenta e robotizada, as legendas apresentavam descompasso temporal por estimativa heurística e o fundo de vídeo carecia de dinamismo e gameplay real de GTA 6, decidimos por integrar o motor neural VITS local Piper-TTS com cadência acelerada gamer, o alinhador acústico Faster-Whisper para timestamps por palavra com precisão de milissegundos e um montador dinâmico de múltiplos clipes de B-Roll com trilha sonora ducked, para alcançar vídeos de alto engajamento visual com custo marginal zero e renderização abaixo de 10 segundos, aceitando o download inicial idempotente de modelos locais ONNX.

## Decisão

1. **Voz Neural Local com Piper-TTS:** Utilização do modelo VITS `pt_BR-faber-medium.onnx` com `length_scale: 0.85` e filtros FFmpeg de compressão broadcast (`compand`, `highpass`, `loudnorm`), com fallback defensivo para gTTS.
2. **Alinhamento Acústico por Palavra via Faster-Whisper:** Extração dos timestamps reais (`word.start`, `word.end`) através do modelo `tiny` quantizado em int8, gerando legendas estilo karaokê em blocos de 2 a 3 palavras com alto contraste visual.
3. **Dynamic B-Roll e Trilha Gamer:** Suporte à seleção e corte dinâmico de clipes reais de gameplay em proporção 9:16 vertical (1080x1920) a cada 3 a 5 segundos com trilha sonora ambiente atenuada a -20dB.

## Consequências

### Positivas
* Eliminação completa da voz robótica, atingindo cadência energética e natural de criador gamer.
* Sincronização milissegundo perfeita das legendas com a forma de onda do áudio falado.
* Vídeos visualmente ricos com gameplay real de GTA 6 e Vice City.
* Custo marginal de R$ 0,00 por vídeo e operação 100% offline e soberana.

### Negativas
* Requer o download inicial dos pesos dos modelos (~60MB para Piper-TTS e ~39MB para Whisper).

### Neutras/Riscos Mitigados
* Caso os modelos ONNX não estejam acessíveis, o motor reverte automaticamente para o fallback resiliente gTTS sem interromper o pipeline.
