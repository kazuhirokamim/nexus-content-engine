# PLAN-002: Reengenharia Audiovisual do Nexus Content Engine

Status: RATIFICADO  
rev: c3bf7481a  
versao_plano: 2.0  
tipo: feature  
blast_radius: médio  
orcamento_tokens: 50000  

---

## Metadados SDD

- **versao_plano**: 2.0
- **tipo**: feature
- **blast_radius**: médio
- **orcamento_tokens**: 50000
- **autor**: Kazuhiro & Antigravity Swarm
- **data**: 2026-10-13

---

## Não-Objetivos / Fora de Escopo

- Não implementar interface web gráfica nesta sprint (a CLI soberana 100% turnkey é mantida para o operador).
- Não alterar o modelo de monetização ou descontinuar o nicho principal de GTA 6.
- Não realizar postagem ou upload automático em contas de terceiros sem a revisão e aprovação humana do operador.

---

## Requisitos EARS

| ID | Tipo | Texto |
| :--- | :--- | :--- |
| REQ-AV-01 | Ubiquitous | O sistema deve sintetizar áudio utilizando motor neural local Piper-TTS com cadência acelerada e masterização FFmpeg. |
| REQ-AV-02 | Event-driven | Quando o áudio for sintetizado, o sistema deve alinhar acusticamente cada palavra via Faster-Whisper gerando timestamps exatos. |
| REQ-AV-03 | Unwanted | Se o modelo neural Piper-TTS falhar na inicialização, então o sistema deve acionar o fallback acústico seguro sem quebrar o pipeline. |
| REQ-AV-04 | Optional | Onde clipes reais de gameplay estiverem presentes na pasta de presets, o sistema deve aplicar cortes dinâmicos a cada 3 a 5 segundos e trilha sonora ducked. |

---

## Orçamentos Não-Funcionais

- SLA de renderização p95: inferior a 15 segundos para vídeos verticais de 45 segundos.
- Taxa de sincronismo acústico: desvio temporal inferior a 50 milissegundos por palavra falada.
- Orçamento de linhas: nenhum arquivo de código de produção deve exceder 700 linhas (Regra Tear #24).
- Custo operacional marginal: R$ 0,00 por vídeo renderizado (100% local-first e offline).

---

## Hotspots Compartilhados

- `src/core/tts_engine.py` (adicionando Piper-TTS e Whisper)
- `src/core/video_assembler.py` (suporte a B-rolls múltiplos e trilha de fundo)
- `run_operator.py` (integração dos novos recursos na esteira do Jayp)

---

## Tarefas

| Tarefa | Agent | Model | Effort | Tempo | Depends-on | Requisitos |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| T1 | tear-backend | inherit | high | 30m | (nenhum) | REQ-AV-01, REQ-AV-03 |
| T2 | tear-backend | inherit | high | 30m | T1 | REQ-AV-02 |
| T3 | tear-backend | inherit | medium | 30m | T2 | REQ-AV-04 |

---

## Matriz de Rastreabilidade

| REQ | TESTE | TAREFA |
| :--- | :--- | :--- |
| REQ-AV-01 | tests/test_tts_engine.py | T1 |
| REQ-AV-02 | tests/test_tts_engine.py | T2 |
| REQ-AV-03 | tests/test_tts_engine.py | T1 |
| REQ-AV-04 | tests/test_video_assembler.py | T3 |
