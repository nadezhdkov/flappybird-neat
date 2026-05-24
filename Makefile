.PHONY: help install install-pip env run run-player lint format clean

PYTHON      := python3
PIP         := pip3
CONDA_ENV   := flappybird-neat
ENTRY       := main.py

# ── Default ────────────────────────────────────────────────────────────────
help:
	@echo ""
	@echo "  Flappy Bird NEAT — available commands"
	@echo ""
	@echo "  make install      Create conda env and install dependencies"
	@echo "  make install-pip  Install dependencies via pip (venv)"
	@echo "  make env          Activate conda environment hint"
	@echo "  make run          Run the game in AI mode"
	@echo "  make run-player   Run the game in player mode"
	@echo "  make lint         Run ruff linter"
	@echo "  make format       Run ruff formatter"
	@echo "  make clean        Remove cache and compiled files"
	@echo ""

# ── Installation ───────────────────────────────────────────────────────────
install:
	conda env create -f environment.yml
	@echo ""
	@echo "  Done. Activate with: conda activate $(CONDA_ENV)"
	@echo ""

install-pip:
	$(PYTHON) -m venv .venv
	. .venv/bin/activate && $(PIP) install --upgrade pip && $(PIP) install -r requirements.txt
	@echo ""
	@echo "  Done. Activate with: source .venv/bin/activate"
	@echo ""

env:
	@echo "  Run: conda activate $(CONDA_ENV)"

# ── Run ────────────────────────────────────────────────────────────────────
run:
	$(PYTHON) $(ENTRY)

run-player:
	AI_PLAYING=false $(PYTHON) $(ENTRY)

# ── Quality ────────────────────────────────────────────────────────────────
lint:
	$(PYTHON) -m ruff check .

format:
	$(PYTHON) -m ruff format .

# ── Clean ──────────────────────────────────────────────────────────────────
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	@echo "  Cleaned."
