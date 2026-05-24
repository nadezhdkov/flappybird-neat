import os

import neat
import pygame

import manager
import neats
from   config      import Config
from   objectscene import Bird, Ground, Pipe


CONFIG       = Config()
__statistics = CONFIG.get("game.statistics")


class GameState:
    """Encapsula o estado mutável de uma rodada do jogo."""

    def __init__(self):
        self.birds:    list[Bird]                       = []
        self.genomes:  list[neat.DefaultGenome]         = []
        self.networks: list[neat.nn.FeedForwardNetwork] = []
        self.pipes:    list[Pipe]                       = [Pipe(CONFIG.get("pipe.spawn_x"))]
        self.ground:   Ground                           = Ground(CONFIG.get("ground.position_y"))
        self.points:   int                              = 0

    # ------------------------------------------------------------------
    # Inicialização
    # ------------------------------------------------------------------

    def setup_ai(self, raw_genomes, config):
        """Popula birds/genomes/redes para o modo IA."""
        for _, genome in raw_genomes:
            genome.fitness = 0
            network = neat.nn.FeedForwardNetwork.create(genome, config)
            self.networks.append(network)
            self.genomes.append(genome)
            self.birds.append(self._make_bird())

    def setup_player(self):
        """Cria um único pássaro para o modo jogador."""
        self.birds.append(self._make_bird())

    @staticmethod
    def _make_bird() -> Bird:
        return Bird(CONFIG.get("bird.spawn_x"), CONFIG.get("bird.spawn_y"))

    # ------------------------------------------------------------------
    # Consultas de estado
    # ------------------------------------------------------------------

    @property
    def alive(self) -> bool:
        return bool(self.birds)

    @property
    def active_pipe_index(self) -> int:
        """Retorna o índice do cano relevante para a decisão da IA."""
        if len(self.pipes) > 1:
            first = self.pipes[0]
            if self.birds[0].axes_x > first.axes_x + first.PIPE_TOP.get_width():
                return 1
        return 0


class FlappyGame:
    """Responsável pelo loop principal e pela lógica de um episódio."""

    def __init__(self):
        self._screen = pygame.display.set_mode(
            (manager.WINDOWS_WIDTH, manager.WINDOWS_HEIGHT)
        )
        self._clock = pygame.time.Clock()

    # ------------------------------------------------------------------
    # Ponto de entrada
    # ------------------------------------------------------------------

    def run(self, state: GameState) -> None:
        """Executa o loop do jogo até não restar pássaros."""
        while state.alive:
            self._clock.tick(CONFIG.get("game.fps"))

            if not self._handle_events(state):
                return  # janela fechada

            self._step(state)
            manager.update(
                self._screen, state.birds, state.pipes, state.ground, state.points
            )

    # ------------------------------------------------------------------
    # Eventos
    # ------------------------------------------------------------------

    def _handle_events(self, state: GameState) -> bool:
        """Processa eventos pygame. Retorna False se o jogo deve encerrar."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if not neats.ai_is_playing and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for bird in state.birds:
                        bird.jump()
        return True

    # ------------------------------------------------------------------
    # Atualização por frame
    # ------------------------------------------------------------------

    def _step(self, state: GameState) -> None:
        pipe_idx = state.active_pipe_index
        self._update_birds(state, pipe_idx)
        state.ground.move()
        self._update_pipes(state)
        self._remove_ground_colliders(state)

    def _update_birds(self, state: GameState, pipe_idx: int) -> None:
        """Move cada pássaro e aplica a decisão da rede neural (modo IA)."""
        for i, bird in enumerate(state.birds):
            bird.move()
            if neats.ai_is_playing:
                state.genomes[i].fitness += 0.1
                self._apply_network(state, i, pipe_idx)

    def _apply_network(
        self, state: GameState, bird_idx: int, pipe_idx: int
    ) -> None:
        """Consulta a rede do pássaro `bird_idx` e pula se necessário."""
        bird = state.birds[bird_idx]
        pipe = state.pipes[pipe_idx]
        inputs = (
            bird.axes_y,
            abs(bird.axes_y - pipe.height),
            abs(bird.axes_y - pipe.pos_base),
        )
        output = state.networks[bird_idx].activate(inputs)
        if output[0] > 0.5:
            bird.jump()

    def _update_pipes(self, state: GameState) -> None:
        """Move os canos, detecta colisões e adiciona novos quando necessário."""
        pipes_to_remove: list[Pipe] = []
        add_pipe = False

        for pipe in state.pipes:
            self._check_pipe_collisions(state, pipe)

            if not pipe.passed and state.birds and pipe.axes_x < state.birds[0].axes_x:
                pipe.passed = True
                add_pipe = True

            pipe.move()

            if pipe.axes_x + pipe.PIPE_TOP.get_width() < 0:
                pipes_to_remove.append(pipe)

        if add_pipe:
            self._on_pipe_passed(state)

        for pipe in pipes_to_remove:
            state.pipes.remove(pipe)

    def _check_pipe_collisions(self, state: GameState, pipe: Pipe) -> None:
        """Remove pássaros que colidiram com `pipe`."""
        dead_indices = [
            i
            for i, bird in enumerate(state.birds)
            if pipe.collision_2d(bird)
        ]
        self._kill_birds(state, dead_indices, fitness_penalty=-1)

    def _on_pipe_passed(self, state: GameState) -> None:
        """Contabiliza ponto e adiciona próximo cano."""
        state.points += 1
        state.pipes.append(Pipe(CONFIG.get("pipe.next_pipe_spawn_x")))
        if neats.ai_is_playing:
            for genome in state.genomes:
                genome.fitness += 5

    def _remove_ground_colliders(self, state: GameState) -> None:
        """Remove pássaros que tocaram o chão ou saíram pelo topo."""
        ground_y = state.ground.axes_y
        dead_indices = [
            i
            for i, bird in enumerate(state.birds)
            if (bird.axes_y + bird.sprit.get_height()) > ground_y or bird.axes_y < 0
        ]
        self._kill_birds(state, dead_indices)

    # ------------------------------------------------------------------
    # Utilitário
    # ------------------------------------------------------------------

    @staticmethod
    def _kill_birds(
        state: GameState,
        indices: list[int],
        fitness_penalty: float = 0,
    ) -> None:
        """Remove pássaros (e estruturas associadas) pelos índices fornecidos."""
        for i in sorted(indices, reverse=True):
            state.birds.pop(i)
            if neats.ai_is_playing:
                if fitness_penalty:
                    state.genomes[i].fitness += fitness_penalty
                state.genomes.pop(i)
                state.networks.pop(i)


# ---------------------------------------------------------------------------
# Funções de entry-point (mantidas compatíveis com o runner NEAT)
# ---------------------------------------------------------------------------


def fitness_function(raw_genomes, config):
    """Função de fitness exigida pelo NEAT – assinatura (genomes, config)."""
    neats.generation += 1

    state = GameState()
    if neats.ai_is_playing:
        state.setup_ai(raw_genomes, config)
    else:
        state.setup_player()

    game = FlappyGame()
    game.run(state)


def build_population(config_path: str) -> neat.Population:
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path,
    )
    population = neat.Population(config)

    if __statistics:
        population.add_reporter(neat.StdOutReporter(True))
        population.add_reporter(neat.StatisticsReporter())

    return population


def run(config_path: str) -> None:
    population = build_population(config_path)

    if neats.ai_is_playing:
        population.run(fitness_function, 50)
    else:
        fitness_function(None, None)


if __name__ == "__main__":
    _base = os.path.dirname(__file__)
    run(os.path.join(_base, "config.txt"))