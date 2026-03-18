from __future__ import annotations

from dataclasses import dataclass, field
from random import Random


@dataclass(slots=True)
class Actor:
    actor_id: int
    x: int
    y: int
    faction: str
    goal: str
    energy: int = 100


@dataclass(slots=True)
class Chunk:
    chunk_id: int
    x0: int
    y0: int
    width: int
    height: int
    threat: int
    fertility: int
    noise: float = 0.0
    seen_ticks: int = 0
    actors: list[int] = field(default_factory=list)

    def desirability(self) -> float:
        """Higher means this zone should be simulated more often."""
        return (self.threat * 1.5) + (self.fertility * 0.75) + self.noise + (self.seen_ticks * 0.1)


class World:
    def __init__(self, width: int, height: int, chunk_size: int, seed: int) -> None:
        self.width = width
        self.height = height
        self.chunk_size = chunk_size
        self.rng = Random(seed)
        self.chunks = self._build_chunks()
        self.actors: dict[int, Actor] = {}

    def _build_chunks(self) -> list[Chunk]:
        chunks: list[Chunk] = []
        chunk_id = 0
        for y in range(0, self.height, self.chunk_size):
            for x in range(0, self.width, self.chunk_size):
                chunks.append(
                    Chunk(
                        chunk_id=chunk_id,
                        x0=x,
                        y0=y,
                        width=min(self.chunk_size, self.width - x),
                        height=min(self.chunk_size, self.height - y),
                        threat=self.rng.randint(0, 10),
                        fertility=self.rng.randint(0, 10),
                    )
                )
                chunk_id += 1
        return chunks

    def spawn_actor(self, actor_id: int, faction: str, goal: str) -> None:
        x = self.rng.randrange(self.width)
        y = self.rng.randrange(self.height)
        actor = Actor(actor_id=actor_id, x=x, y=y, faction=faction, goal=goal)
        self.actors[actor_id] = actor
        self.chunk_for(actor.x, actor.y).actors.append(actor_id)

    def chunk_for(self, x: int, y: int) -> Chunk:
        col = min(x // self.chunk_size, max((self.width - 1) // self.chunk_size, 0))
        row = min(y // self.chunk_size, max((self.height - 1) // self.chunk_size, 0))
        idx = row * ((self.width + self.chunk_size - 1) // self.chunk_size) + col
        return self.chunks[idx]

    def move_actor(self, actor_id: int, dx: int, dy: int) -> None:
        actor = self.actors[actor_id]
        src = self.chunk_for(actor.x, actor.y)
        actor.x = max(0, min(self.width - 1, actor.x + dx))
        actor.y = max(0, min(self.height - 1, actor.y + dy))
        dest = self.chunk_for(actor.x, actor.y)
        if src.chunk_id != dest.chunk_id:
            src.actors.remove(actor_id)
            dest.actors.append(actor_id)
            dest.noise += 0.4
        actor.energy = max(0, actor.energy - 1)

    def tick_decay(self) -> None:
        for c in self.chunks:
            c.noise *= 0.9
            c.seen_ticks += 1
