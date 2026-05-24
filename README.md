![Python](https://img.shields.io/badge/python-3.11-blue?logo=python) ![License](https://img.shields.io/badge/license-MIT-green) ![Pygame](https://img.shields.io/badge/pygame-2.6.1-orange?logo=pygame) ![NEAT-Python](https://img.shields.io/badge/neat--python-0.92-purple) ![Code Style](https://img.shields.io/badge/code%20style-ruff-black) ![Status](https://img.shields.io/badge/status-active-brightgreen)

# 🐦 Flappy Bird NEAT

*Flappy Bird autônomo treinado por neuroevolução com NEAT-Python*

Uma implementação do clássico Flappy Bird em Python com Pygame, onde uma inteligência artificial aprende a jogar sozinha utilizando o algoritmo NEAT (NeuroEvolution of Augmenting Topologies). Ao longo de gerações, redes neurais evoluem suas topologias e pesos até dominar completamente o jogo — sem nenhuma intervenção humana.

---

## 🎬 Demo

<video src="assets/ai_playing.mp4" width="640" controls autoplay loop muted></video>

*IA treinada com NEAT aprendendo a passar pelos canos ao longo das gerações.*

---

## 🧠 Como funciona

### Flappy Bird

O jogo segue as regras clássicas: um pássaro avança horizontalmente pela tela enquanto pares de canos surgem da direita com uma abertura aleatória. O jogador (ou a IA) tem uma única ação disponível — **pular**. Se o pássaro colidir com um cano, com o chão ou sair da tela, ele morre.

### NEAT — NeuroEvolution of Augmenting Topologies

O algoritmo NEAT evolui uma população de redes neurais ao longo de gerações:

1. **População inicial** — cada indivíduo é uma rede neural simples que controla um pássaro.
2. **Inputs da rede** — cada rede recebe 3 entradas:
   - Posição Y do pássaro (`axes_y`)
   - Distância ao topo do próximo cano
   - Distância à base do próximo cano
3. **Função de fitness** — o fitness é calculado pelo tempo de sobrevivência somado aos canos ultrapassados, com penalidade por colisão. Pássaros que sobrevivem mais e passam por mais canos recebem pontuações mais altas.
4. **Seleção e mutação** — as melhores redes são selecionadas e sofrem mutação de pesos e topologia (adição/remoção de nós e conexões).
5. **Convergência** — após diversas gerações, a rede evolui até ser capaz de jogar indefinidamente sem colidir.

---

## ⚙️ Pré-requisitos

- **Python** 3.11+
- **Conda** ou **pip + venv**
- **Sistema operacional:** Linux / macOS / Windows

---

## 🚀 Instalação

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

> Substitua `<repo-url>` pela URL do seu repositório.

---

## ▶️ Executando

```bash
# Modo IA (NEAT treinando)
make run

# Modo jogador (controle manual com SPACE)
make run-player
```

---

## 🛠️ Makefile

| Comando            | Descrição                                  |
|---------------------|--------------------------------------------|
| `make install`      | Cria o ambiente Conda e instala dependências |
| `make install-pip`  | Instala via pip em venv                     |
| `make run`          | Roda o jogo no modo IA                     |
| `make run-player`   | Roda o jogo no modo jogador                |
| `make lint`         | Executa o linter (ruff)                    |
| `make format`       | Formata o código (ruff)                    |
| `make clean`        | Remove caches e arquivos compilados        |

---

## ⚙️ Configuração

Os parâmetros do jogo — física do pássaro, velocidade dos canos, resolução da janela — ficam em `config.yml` e podem ser editados sem alterar o código-fonte:

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

A configuração da rede neural NEAT (tamanho da população, taxas de mutação, espécies) fica em `config.txt`.

---

## 📁 Estrutura

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

---

## 📄 Licença

Este projeto está licenciado sob a MIT License — veja o arquivo [LICENSE](LICENSE) para detalhes.
