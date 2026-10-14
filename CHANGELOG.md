# Changelog

Todas as mudanças notáveis no projeto **Nexus Content Engine** serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere estritamente ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

---

## [0.3.0] - 2026-10-14

### Added
- Motor combinatório cartesiano `NexusScale` (`src/core/scale_matrix.py`) com decomposição em ganchos $\times$ B-rolls $\times$ CTAs para testes A/B em massa.
- Modo de execução em lote `--scale` no ponto de entrada CLI `src/main.py` com salvamento automático de manifesto de variações JSON.
- Especificação técnica soberana e arquitetura multi-nicho em `documentation/BENCHMARK-COMPETITIVO-E-ESPECIFICACAO-NEXUS.md`.
- Registro arquitetural ADR-003 e plano formal SDD 2.0 PLAN-003.
- Suíte de testes unitários TDD cobrindo caminhos felizes, casos de borda e caminhos de erro (`tests/test_scale_matrix.py`), totalizando 20 testes 100% verdes.

### Changed
- Padronização soberana de todas as nomenclaturas da suíte funcional sob a marca proprietária Nexus (NexusScale, NexusScrap, NexusRepost, NexusTemplates, NexusEditor, NexusPack, NexusAcademy, NexusMCP).
- Limpeza e abstração de qualquer dependência ou menção externa no código-fonte de produção.
- Motor de síntese de voz neural local com Piper-TTS (`pt_BR-faber-medium.onnx`) com cadência acelerada (`length_scale: 0.85`) e cadeia de masterização broadcast (`acompressor`, `highpass`, `loudnorm`).
- Alinhador acústico neural com Faster-Whisper (`tiny` int8) extraindo timestamps com precisão de milissegundos por palavra para legendas karaokê.
- Suporte a clipes reais de gameplay em B-roll (`presets/gta6/b_roll/`) e mixagem com ducking de trilha synthwave de fundo (-22dB).
- Registro arquitetural ADR-002 e plano formal SDD 2.0 PLAN-002.
- Motor de síntese de voz e alinhamento temporal (`TTSEngine` em `src/core/tts_engine.py`).
- Renderizador de vídeo vertical 9:16 (`VideoAssembler` em `src/core/video_assembler.py`) com suporte a aceleração por hardware Apple Silicon (`h264_videotoolbox`) e FFmpeg embutido via `imageio-ffmpeg`.
- Interface CLI de comando único para o operador (`run_operator.py`).
- Script de instalação automática de 1-clique para o operador (`scripts/setup_jayp.sh`).
- Preset flagship de GTA 6 (`presets/gta6/prompts.yaml` e `presets/gta6/affiliate_links.txt`).
- Registro arquitetural ADR-001 (`docs/adr/ADR-001-turnkey-pipeline-architecture.md`).
- Suíte de 10 testes unitários automatizados passando 100% verde (`python3 -m unittest discover tests`).
- Tratado acadêmico formal e especificação EARS em `/documentation`.

### Changed
- Substituição do cálculo heurístico de legendas por alinhamento acústico real de espectro via Faster-Whisper.
- Substituição da narração sintética do tradutor por voz neural VITS local de criador gamer.
