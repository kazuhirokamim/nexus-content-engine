---
numero: 3
titulo: Motor Combinatório Cartesiano NexusScale (1-to-N) para Produção em Massa
data: 2026-10-14
status: Aceito
autores:
  - Philip Kazuhiro Kamimura
  - Noesis Architecture Maestro
  - Tear Maestro
aplica_a:
  - src/core
  - tests
tags:
  - nexus-scale
  - combinatorial
  - batch-render
  - multi-niche
---

# ADR-003: Motor Combinatório Cartesiano NexusScale (1-to-N) para Produção em Massa

## Contexto e Declaração do Problema

No contexto de escalabilidade exponencial de vídeos verticais 9:16 para o Nexus Content Engine, enfrentando a lentidão e o esforço manual de produzir variações unitárias além dos altos custos de plataformas em nuvem proprietárias, decidimos por implementar o motor combinatório cartesiano NexusScale com amostragem configurável e renderização neural local, para alcançar a geração massiva de dezenas de variações A/B por tema a custo zero, aceitando o processamento linear em lote de renderização por hardware.

## Decisão

1. **Produto Cartesiano Tipado e Determinístico:** Implementação da classe `ScaleMatrix` que decompõe o vídeo nos três blocos fundamentais:
   $$\mathcal{V} = \mathcal{H}_{\text{hooks}} \times \mathcal{B}_{\text{broll}} \times \mathcal{C}_{\text{cta}}$$
   gerando instâncias imutáveis de `ScaleVariation` com identificadores únicos baseados em hash determinístico.
2. **Amostragem e Controle de Volume (`count` / `seed`):** Capacidade de gerar o conjunto completo de combinações ou extrair uma amostra pseudo-aleatória reproduzível para evitar redundância.
3. **Execução em Lote com Fallback Defensivo:** Cada variação é renderizada pelo pipeline de áudio neural (`Piper-TTS` + `Faster-Whisper`) e montagem de vídeo (`FFmpeg` GPU), isolando falhas por variação para que o lote continue mesmo se uma mídia estiver temporariamente corrompida.
4. **Matriz Declarativa JSON & Parâmetros CLI:** Suporte à ingestão de arquivos estruturados `matrix.json` ou chamada direta via CLI `--scale --niche gta6 --count N`.

## Consequências

### Positivas
* Capacidade de gerar dezenas de variações a partir de um único tema em minutos.
* Suporte nativo a múltiplos nichos (GTA 6, Tech, Crimes, Crypto) de forma simétrica.
* Total independência de cotas ou mensalidades de plataformas fechadas.
* Metadados gerados em JSON para rastreamento de performance de cada headline/variação.

### Negativas
* O tempo total de processamento em lote escala linearmente com $N$, exigindo uso eficiente de aceleração por GPU.

### Neutras/Riscos Mitigados
* Uso de geradores `itertools.product` para manter o consumo de memória principal em $\mathcal{O}(1)$ durante o planejamento da matriz.
