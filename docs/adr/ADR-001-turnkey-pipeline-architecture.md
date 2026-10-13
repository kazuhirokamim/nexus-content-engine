---
numero: 1
titulo: Arquitetura da Esteira Turnkey de Síntese de Áudio e Renderização de Vídeo
data: 2026-10-13
status: Aceito
autores:
  - Philip Kazuhiro Kamimura
  - Noesis Architecture Maestro
  - Tear Maestro
aplica_a:
  - src
  - tests
  - docs
tags:
  - video
  - tts
  - ffmpeg
  - turnkey
  - pipeline
---

# ADR-001: Arquitetura da Esteira Turnkey de Síntese de Áudio e Renderização de Vídeo

## Contexto e Declaração do Problema

No contexto de construção do Nexus Content Engine para automação de vídeos verticais (9:16), enfrentando a necessidade de disponibilizar um ambiente pronto e funcional (turnkey) para o operador Jayp sem exigir compilação complexa de dependências de sistema ou infraestrutura pesada em nuvem, decidimos por integrar a síntese acústica gTTS com alinhamento temporal e o empacotamento estático do FFmpeg via imageio-ffmpeg com aceleração por hardware nativa, para alcançar renderização de vídeos em menos de 30 segundos com zero fricção de setup, aceitando a geração procedural de fundos neon estilizados quando B-Roll de gameplay não estiver presente.

## Decisão

1. **Síntese de Áudio e Alinhamento:** Implementação do `TTSEngine` baseado em `gTTS` com cálculo determinístico de duração fonética e exportação de legendas `.srt`.
2. **Renderização Portável:** Utilização do binário FFmpeg pré-compilado através do `imageio-ffmpeg`, eliminando dependências de compiladores C/C++ locais.
3. **Aceleração de Hardware:** Suporte nativo ao encoder `h264_videotoolbox` no macOS e `h264_nvenc` no Linux.
4. **Interface do Operador:** Criação de `run_operator.py` e script de 1-clique `scripts/setup_jayp.sh`.

## Consequências

### Positivas
* O operador Jayp pode clonar e rodar o pipeline completo em menos de 1 minuto com apenas 1 comando bash.
* Zero custo financeiro de infraestrutura em nuvem durante a fase de validação operacional.
* Suíte de testes unitários automatizados com 100% de cobertura nos 3 cenários canônicos Tear.

### Negativas
* O provedor gTTS depende de conexão de rede estável para síntese da fala.

### Neutras/Riscos Mitigados
* Caso o operador não insira um clipe de gameplay real, o renderizador gera um fundo procedural estilizado sem quebrar o pipeline.
