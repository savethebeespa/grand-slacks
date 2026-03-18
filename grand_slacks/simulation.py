from __future__ import annotations

import time
from dataclasses import dataclass
from random import Random

from .config import SimConfig
from .world import World


GOALS = ("scavenge", "craft", "fortify", "explore")
FACTIONS = ("drifters", "forgekin", "mycelials", "null monks")


@dataclass(slots=True)
class TickReport:
    tick: int
    simulated_chunks: int
    actor_updates: int
    elapsed_ms: float


class Simulation:
    def __init__(self, config: SimConfig) -> None:
        self.config = config
        self.world = World(config.width, config.height, config.chunk_size, config.seed)
        self.rng = Random(config.seed + 99)
        self.tick_number = 0
        self._seed_actors(config.actor_count)

    def _seed_actors(self, actor_count: int) -> None:
        for actor_id in range(actor_count):
            self.world.spawn_actor(
                actor_id=actor_id,
                faction=self.rng.choice(FACTIONS),
                goal=self.rng.choice(GOALS),
            )

    def _pick_active_chunks(self) -> list[int]:
        chunk_scores = [(c.chunk_id, c.desirability()) for c in self.world.chunks]
        chunk_scores.sort(key=lambda item: item[1], reverse=True)
        budget = self.config.max_active_chunks
        if self.config.low_power_mode:
            budget = max(4, budget // 2)
        return [chunk_id for chunk_id, _ in chunk_scores[:budget]]

    def tick(self) -> TickReport:
        start = time.perf_counter()
        active = set(self._pick_active_chunks())
        actor_updates = 0

        for chunk in self.world.chunks:
            if chunk.chunk_id not in active:
                continue

            cadence = 2 if self.config.low_power_mode else 1
            if (self.tick_number + chunk.chunk_id) % cadence != 0:
                continue

            local_ids = list(chunk.actors)
            for actor_id in local_ids:
                dx = self.rng.randint(-1, 1)
                dy = self.rng.randint(-1, 1)
                self.world.move_actor(actor_id, dx, dy)
                actor_updates += 1

        self.world.tick_decay()
        self.tick_number += 1
        elapsed_ms = (time.perf_counter() - start) * 1000

        if elapsed_ms > self.config.max_tick_ms:
            # Dynamic degradation keeps game responsive on older machines.
            self.config.max_active_chunks = max(4, self.config.max_active_chunks - 1)

        return TickReport(
            tick=self.tick_number,
            simulated_chunks=len(active),
            actor_updates=actor_updates,
            elapsed_ms=elapsed_ms,
        )
