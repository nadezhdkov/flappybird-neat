# Prompt — Geração de README.md profissional
# Destino: agente Antigravity
# Projeto: Flappy Bird + NEAT (Python / Pygame)

---

## Contexto do projeto

Você deve gerar um `README.md` completo e profissional para um projeto chamado
**Flappy Bird NEAT** — uma implementação do jogo Flappy Bird em Python com
Pygame, treinada por um algoritmo de neuroevolução (NEAT) que aprende a jogar
sozinho ao longo de gerações.

### Estrutura do projeto

```
flappybird/
├── main.py            # Loop principal e função de fitness do NEAT
├── objectscene.py     # Entidades: Bird, Pipe, Ground
├── manager.py         # Renderização / HUD
├── config.py          # Carregador de config YAML (Singleton)
├── assetsutil.py      # Enum de assets + Loader com cache
├── neats.py           # Estado global do NEAT (geração, flags)
├── config.yml         # Parâmetros do jogo (física, janela, assets)
├── config.txt         # Configuração da rede neural NEAT
├── assets/
│   ├── bird_idle.png
│   ├── bird_flying.png
│   ├── bird_run.png
│   ├── pipe.png
│   ├── background.png
│   ├── ground.png
│   └── ai_playing.mp4   ← vídeo de demonstração da IA jogando
├── environment.yml    # Dependências Conda
├── requirements.txt   # Dependências pip
├── Makefile           # Comandos de build/run/lint
└── LICENSE            # MIT License
```

### Stack técnica

- **Python 3.11**
- **Pygame 2.6** — renderização 2D
- **NEAT-Python 0.92** — neuroevolução de topologias aumentantes
- **PyYAML 6** — configuração declarativa

---

## O que o README deve conter (obrigatório)

### 1. Badges / shields no topo

Use `shields.io` e coloque em linha. Inclua ao menos:

| Badge | Informação |
|-------|-----------|
| Python version | `3.11` |
| License | MIT |
| Pygame | `2.6.1` |
| NEAT-Python | `0.92` |
| Code style | Ruff |
| Status | `Active` |

Exemplo de formato esperado (adapte as URLs):
```markdown
![Python](https://img.shields.io/badge/python-3.11-blue?logo=python)
![License](https://img.shields.io/badge/license-MIT-green)
...
```

### 2. Título e descrição

- Nome do projeto em `# H1` com emoji temático (ex.: 🐦)
- Subtítulo em itálico: descrição de uma linha
- Parágrafo curto (~3 linhas) explicando o que o projeto faz

### 3. Demonstração em vídeo

Adicione uma seção `## 🎬 Demo` que incorpora o vídeo de demonstração da IA
jogando. O arquivo está em `assets/ai_playing.mp4`.

Use a tag HTML que o GitHub renderiza para vídeos locais no repositório:

```html
<video src="assets/ai_playing.mp4" width="640" controls autoplay loop muted></video>
```

Adicione uma legenda abaixo: *"IA treinada com NEAT aprendendo a passar pelos canos ao longo das gerações."*

### 4. Como funciona (arquitetura)

Seção `## 🧠 Como funciona` com dois sub-tópicos:

- **Flappy Bird** — regras do jogo, controles, colisão
- **NEAT** — explique brevemente o algoritmo: população inicial de redes,
  função de fitness (tempo vivo + canos passados − penalidade por colisão),
  seleção, mutação de pesos e topologia, convergência ao longo de gerações.
  Mencione os 3 inputs da rede: `axes_y do pássaro`, `distância ao topo do cano`,
  `distância à base do cano`.

### 5. Pré-requisitos

Seção `## ⚙️ Pré-requisitos` listando:
- Python 3.11+
- Conda **ou** pip + venv
- Sistema operacional: Linux / macOS / Windows

### 6. Instalação

Seção `## 🚀 Instalação` com dois blocos de código alternativos:

**Opção A — Conda (recomendado):**
```bash
git clone <repo-url>
cd flappybird
make install
conda activate flappybird-neat
```

**Opção B — pip + venv:**
```bash
git clone <repo-url>
cd flappybird
make install-pip
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### 7. Como executar

Seção `## ▶️ Executando` com:

```bash
# Modo IA (NEAT treinando)
make run

# Modo jogador (controle manual com SPACE)
make run-player
```

### 8. Comandos do Makefile

Seção `## 🛠️ Makefile` com tabela:

| Comando | Descrição |
|---------|-----------|
| `make install` | Cria o ambiente Conda e instala dependências |
| `make install-pip` | Instala via pip em venv |
| `make run` | Roda o jogo no modo IA |
| `make run-player` | Roda o jogo no modo jogador |
| `make lint` | Executa o linter (ruff) |
| `make format` | Formata o código (ruff) |
| `make clean` | Remove caches e arquivos compilados |

### 9. Configuração

Seção `## ⚙️ Configuração` explicando que os parâmetros do jogo (física do
pássaro, velocidade dos canos, resolução da janela) ficam em `config.yml` e
podem ser editados sem alterar o código. Mostre um trecho de exemplo fictício
mas plausível:

```yaml
bird:
  jump_force: -10.5
  gravity: 3.0
  max_rotation: 25

pipe:
  gap: 200
  velocity: 5

window:
  width: 500
  height: 800
```

### 10. Estrutura de arquivos

Seção `## 📁 Estrutura` com o tree do projeto acima, em bloco de código.

### 11. Licença

Seção `## 📄 Licença` com:

```
Este projeto está licenciado sob a MIT License — veja o arquivo LICENSE para detalhes.
```

---

## Regras de estilo para o README

1. **Idioma:** português brasileiro, tom técnico e direto.
2. **Emojis:** use com moderação — apenas nos títulos de seção, não no corpo do texto.
3. **Sem excesso de texto:** cada seção deve ser concisa. Prefira listas e blocos de código a parágrafos longos.
4. **Markdown válido:** o arquivo deve renderizar perfeitamente no GitHub.
5. **Sem placeholders vagos:** onde houver `<repo-url>`, mantenha explícito que o leitor deve substituir.
6. **Badges em uma única linha** no topo, separados por espaço.
7. **Não inclua** seções de "Contribuição" ou "Roadmap" — o projeto não as pediu.

---

## Saída esperada

Retorne **apenas o conteúdo do arquivo `README.md`**, começando com as badges
e terminando na seção de licença. Não adicione explicações fora do arquivo.
