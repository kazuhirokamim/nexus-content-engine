# PLAN-003: NexusScale Combinatorial Engine (1-to-N)

Status: RATIFICADO  
rev: d0fc9e6  
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
- **data**: 2026-10-14

---

## Não-Objetivos / Fora de Escopo

- Não implementar interface gráfica web nesta sprint (a CLI soberana é mantida).
- Não alterar as interfaces de persistência do pipeline existente.
- Não publicar em redes externas sem confirmação humana do operador.

---

## Requisitos EARS

| ID | Tipo | Texto |
| :--- | :--- | :--- |
| REQ-SCALE-01 | Ubiquitous | O sistema deve processar matrizes combinatórias contendo listas de ganchos (hooks), clipes de B-roll e chamadas para ação (CTAs). |
| REQ-SCALE-02 | Event-driven | Quando uma matriz de escala for executada, o sistema deve computar as variações cartesianas gerando planos de renderização estruturados. |
| REQ-SCALE-03 | Optional | Onde um limite de contagem (count) for especificado, o sistema deve amostrar as variações de forma determinística ou embaralhada com seed reproduzível. |
| REQ-SCALE-04 | Unwanted | Se os parâmetros de entrada contiverem listas vazias ou caminhos inválidos de mídia, o sistema deve emitir ScaleMatrixError com diagnóstico claro. |

---

## Orçamentos Não-Funcionais

- Complexidade de combinação: O(H * B * C) em tempo de memória constante O(1) por gerador/iterador.
- Orçamento de linhas: src/core/scale_matrix.py estritamente inferior a 700 linhas (Regra Tear #24).
- Cobertura de testes: Mínimo de 3 cenários (feliz, borda, erro) com 100% de asserções verdes.
- Custo operacional: R$ 0,00 de renderização por variação.

---

## Hotspots Compartilhados

- `src/core/scale_matrix.py` (novo módulo combinatório)
- `src/main.py` (integração da flag `--scale`)
- `tests/test_scale_matrix.py` (suíte de testes unitários)

---

## Tarefas

| Tarefa | Agent | Model | Effort | Tempo | Depends-on | Requisitos |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| T1 | tear-backend | inherit | high | 30m | (nenhum) | REQ-SCALE-01, REQ-SCALE-04 |
| T2 | tear-backend | inherit | medium | 30m | T1 | REQ-SCALE-02, REQ-SCALE-03 |

---

## Matriz de Rastreabilidade

| REQ | TESTE | TAREFA |
| :--- | :--- | :--- |
| REQ-SCALE-01 | tests/test_scale_matrix.py | T1 |
| REQ-SCALE-02 | tests/test_scale_matrix.py | T2 |
| REQ-SCALE-03 | tests/test_scale_matrix.py | T2 |
| REQ-SCALE-04 | tests/test_scale_matrix.py | T1 |
