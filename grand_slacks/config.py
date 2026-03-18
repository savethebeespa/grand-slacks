from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class SimConfig:
    """Tuning knobs for running the simulation on very different hardware tiers."""

    width: int = 96
    height: int = 96
    chunk_size: int = 16
    max_active_chunks: int = 12
    low_power_mode: bool = True
    seed: int = 1337
    actor_count: int = 180
    max_tick_ms: int = 12

    @property
    def chunk_columns(self) -> int:
        return max(1, self.width // self.chunk_size)

    @property
    def chunk_rows(self) -> int:
        return max(1, self.height // self.chunk_size)

    @property
    def chunk_count(self) -> int:
        return self.chunk_columns * self.chunk_rows
