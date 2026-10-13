# Changelog

Todas as mudanças notáveis no projeto **Nexus Content Engine** serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere estritamente ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

---

## [Unreleased]

### Added
- Motor de síntese de voz e alinhamento temporal (`TTSEngine` em `src/core/tts_engine.py`).
- Renderizador de vídeo vertical 9:16 (`VideoAssembler` em `src/core/video_assembler.py`) com suporte a aceleração por hardware Apple Silicon (`h264_videotoolbox`) e FFmpeg embutido via `imageio-ffmpeg`.
- Interface CLI de comando único para o operador (`run_operator.py`).
- Script de instalação automática de 1-clique para o operador (`scripts/setup_jayp.sh`).
- Preset flagship de GTA 6 (`presets/gta6/prompts.yaml` e `presets/gta6/affiliate_links.txt`).
- Registro arquitetural ADR-001 (`docs/adr/ADR-001-turnkey-pipeline-architecture.md`).
- Suíte de 9 testes unitários automatizados passando 100% verde (`python3 -m unittest discover tests`).
- Tratado acadêmico formal e especificação EARS em `/documentation`.

### Changed
- Dependências atualizadas com `imageio-ffmpeg` e `gTTS` para empacotamento turnkey autossuficiente sem necessidade de compilação de código nativo.
