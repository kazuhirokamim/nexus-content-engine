# 📋 Especificação Formal de Requisitos — Nexus Content Engine

**Documento:** `/documentation/REQUIREMENTS.md`  
**Padrão:** EARS (Easy Approach to Requirements Syntax)  
**Governança:** Cânone Tear & Noesis Requirements Swarm  
**Status:** Documento Vivo (Rule #1)

---

## 🎯 1. Requisitos Ubíquos (Ubiquitous Requirements)

* **REQ-UBI-01:** O sistema **deve** gerar vídeos no formato vertical estrito (proporção 9:16, resolução 1080x1920 pixels) com taxa de quadros mínima de 30 FPS.
* **REQ-UBI-02:** O sistema **deve** manter a separação arquitetural estrita entre o motor agnóstico (`core`) e os módulos de conteúdo específicos (`presets`).
* **REQ-UBI-03:** O sistema **deve** registrar logs estruturados em formato legível sem expor chaves de API ou dados confidenciais.

---

## ⚡ 2. Requisitos Orientados a Evento (Event-Driven Requirements)

* **REQ-EVT-01:** **Quando** o operador fornecer um tópico e um nicho, o sistema **deve** gerar um roteiro estruturado contendo gancho inicial (0-3s), miolo informativo e chamada de loop final com duração estimada entre 35 e 55 segundos.
* **REQ-EVT-02:** **Quando** um roteiro for aprovado, o sistema **deve** sintetizar o áudio neural correspondente e calcular os timestamps de cada palavra utilizando alinhamento fonético.
* **REQ-EVT-03:** **Quando** o áudio e as legendas forem gerados, o sistema **deve** renderizar o vídeo final aplicando zoom dinâmico e legendas estilo karaoke sincronizadas.

---

## 🛡️ 3. Requisitos de Tratamento de Exceção (Unwanted Behavior Requirements)

* **REQ-ERR-01:** **Se** o arquivo de B-roll especificado não for encontrado ou estiver corrompido, **então** o sistema **deve** selecionar um clipe padrão de fallback e registrar um aviso detalhado no log de execução sem interromper o pipeline com falha catastrófica.
* **REQ-ERR-02:** **Se** o serviço de síntese de voz (TTS) atingir limite de taxa (rate limit) ou falhar na conexão de rede, **então** o sistema **deve** aplicar backoff exponencial com até 3 tentativas antes de retornar código de erro controlado.
* **REQ-ERR-03:** **Se** o operador tentar executar o sistema fora de uma branch de trabalho ou violar o limite de linhas em código novo, **então** os hooks de governança Tear **devem** bloquear a operação na origem.

---

## 🎛️ 4. Requisitos de Funcionalidades Opcionais (Optional Feature Requirements)

* **REQ-OPT-01:** **Onde** o módulo `presets/gta6` estiver ativo, o sistema **deve** carregar termos especializados do universo de Vice City, notícias de vazamentos e links de afiliados gamer recomendados.
* **REQ-OPT-02:** **Onde** a flag `--multi` for informada, o sistema **deve** gerar $N$ variações concorrentes do mesmo roteiro trocando os primeiros 3 segundos para testes A/B de retenção.
