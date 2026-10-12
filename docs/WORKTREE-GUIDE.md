# 🌿 Guia de Git Worktree — Desenvolvimento Paralelo sem Conflitos

Este guia explica como utilizar o **Git Worktree** no projeto **gta6-content-engine** para que você (**Kazu**) e o **Jayp** possam trabalhar em diferentes frentes (código da esteira, testes de templates, curadoria de mídias) simultaneamente, em pastas separadas, compartilhando o mesmo repositório Git local.

---

## 💡 O Que é Git Worktree e Por Que Usamos Aqui?

Tradicionalmente, para trocar de branch no Git você usa `git checkout` ou `git switch`. No entanto, em um projeto de mídia e código:
* Trocar de branch recarrega dependências e pode apagar arquivos temporários.
* Se alguém estiver rodando uma renderização de teste enquanto outra pessoa ajusta o código, dá conflito de arquivos de saída.

Com **Git Worktree**, o repositório principal gerencia múltiplos diretórios de trabalho independentes ao mesmo tempo. Cada pasta tem sua própria branch ativa!

```
gta6-content-engine/            <-- Repositório Principal (branch: main)
├── .git/
├── docs/
└── worktrees/
    ├── jayp-content/           <-- Pasta isolada rodando branch: feature/jayp-content
    └── engine-automation/      <-- Pasta isolada rodando branch: feature/engine-automation
```

---

## 🛠️ Comandos Práticos

### 1. Criar um novo Worktree para uma Feature
Para iniciar uma frente de trabalho isolada sem tocar na branch principal:

```bash
cd ~/Projetos/gta6-content-engine

# Cria uma pasta isolada dentro de worktrees/ vinculada à nova branch
git worktree add worktrees/engine-automation -b feature/engine-automation
```

Agora você pode abrir a pasta `worktrees/engine-automation` na sua IDE ou terminal e trabalhar livremente.

### 2. Criar um Worktree para o Jayp Operar Conteúdo
```bash
git worktree add worktrees/jayp-content -b feature/jayp-content
```

### 3. Listar todos os Worktrees Ativos
Para ver quais pastas e branches estão ativas:

```bash
git worktree list
```

A saída será parecida com:
```
/Users/user/.../gta6-content-engine                   749a12c [main]
/Users/user/.../gta6-content-engine/worktrees/engine  c4b2a19 [feature/engine-automation]
/Users/user/.../gta6-content-engine/worktrees/jayp    89d2e11 [feature/jayp-content]
```

### 4. Finalizar e Remover um Worktree
Quando a tarefa estiver concluída e mergeada:

```bash
# 1. Remova o diretório do worktree
git worktree remove worktrees/engine-automation

# 2. Delete a branch se já foi integrada
git branch -d feature/engine-automation
```

---

## 🛡️ Regras de Ouro
1. **Nunca comite arquivos de mídia (.mp4, .mov):** A pasta `worktrees/` já está no `.gitignore`.
2. **Branches de Feature:** Sempre crie branches no formato `feature/<slug>` para manter o padrão profissional do ecossistema.
3. **Ambiente Python:** Cada worktree pode criar seu próprio `.venv` ou reutilizar o ambiente principal.
