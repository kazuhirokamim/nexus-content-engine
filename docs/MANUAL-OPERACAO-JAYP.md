# 🕹️ Manual de Operação do Jayp — Rotina & Execução Diária

Olá, **Jayp**! Este manual foi construído para você operar a máquina de conteúdo do **GTA 6** com máxima eficiência, sem perder tempo com edições manuais cansativas e sem precisar de reuniões diárias com o Kazu.

A sua missão principal é **gerenciar a curadoria, revisar os vídeos automáticos e garantir a distribuição diária nas redes sociais**. A esteira de código faz 90% do trabalho pesado.

---

## ⏰ A Rotina Diária de 25 Minutos (Checklist)

```
┌────────────────────────────────────────────────────────┐
│ PASSO 1: Curadoria de Pauta Quente (5 min)             │
│ PASSO 2: Inserir tema no script gerador (3 min)        │
│ PASSO 3: Prévia & Aprovação do Vídeo Gerado (5 min)    │
│ PASSO 4: Upload em 3 Redes (Shorts, TikTok, Reels) (10)│
│ PASSO 5: Responder os 5 primeiros comentários (2 min)  │
└────────────────────────────────────────────────────────┘
```

---

## 🧭 Passo a Passo Operacional

### 1. Onde encontrar temas quentes (Fontes Diárias)
Dedique 5 minutos pela manhã ou à noite para checar:
* **Reddit r/GTA6:** [reddit.com/r/GTA6](https://reddit.com/r/GTA6) (veja a aba *Top: Today* ou *Hot*).
* **X (Twitter):** Busque pelos termos `#GTA6`, `#GTAVI` e perfis de notícias como `@GTAVI_Countdown` ou `@RockstarGames`.
* **Canais Gringos no YouTube:** Veja os últimos títulos de canais como *LegacyKillaHD*, *Gamer Inquirer* ou *Badger Goodger*.

### 2. Disparando a Esteira de Vídeo
Você não precisa saber programar. Basta abrir o terminal na pasta do projeto e rodar o comando:

```bash
cd ~/Projetos/gta6-content-engine
source .venv/bin/activate

# Exemplo de geração de 1 vídeo
python3 src/main.py --topic "Nova física de deformação de carros vazada do GTA 6"
```

A esteira vai:
1. Escrever o roteiro otimizado para retenção (com gancho nos primeiros 3s e loop no final).
2. Gerar a narração neural limpa (sem voz robótica).
3. Selecionar o B-Roll de gameplay 4K da biblioteca de mídias.
4. Sincronizar as legendas dinâmicas estilo karaoke.
5. Exportar o arquivo `.mp4` pronto na pasta `output/`.

### 3. Revisão do Vídeo (Quality Check)
Abra o vídeo gerado na pasta `output/` e valide 3 coisas:
* [ ] O gancho inicial prende a atenção de imediato?
* [ ] A legenda está perfeitamente alinhada com a voz?
* [ ] O corte final faz um loop suave com o início?

### 4. Publicação em Multi-Canais
Poste o mesmo arquivo `.mp4` nas 3 redes:
* **YouTube Shorts** (Melhores horários: 12h00 e 18h30)
* **TikTok** (Melhores horários: 13h00 e 20h00)
* **Instagram Reels** (Melhores horários: 11h30 e 19h00)

**Títulos e Descrições:**
* Título curto e instigante (ex: *"Isso vai mudar o GTA 6 para sempre 🤯"*).
* Hashtags padrão: `#gta6 #gtavi #rockstargames #games #playstation5 #vicecity`.
* Comentário fixado seu: *"Você acha que o GTA 6 chega no prazo ou atrasa? Comenta aí!"* (força comentários e aumenta entrega).

---

## 🤝 Alinhamento Kazu & Jayp

* **Kazu:** Responsável pela arquitetura do código, novas integrações de IA, melhoria na qualidade dos cortes e manutenção técnica.
* **Jayp:** Responsável pelo crescimento das redes, relacionamento com o público, testes de títulos/capas e consistência de postagem.
* **Comunicação:** Caso a esteira apresente qualquer erro ou precise de novos clipes de gameplay, avise o Kazu com o log de erro no terminal.
