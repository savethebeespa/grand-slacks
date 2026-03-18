from __future__ import annotations

import argparse

from .config import SimConfig
from .simulation import Simulation


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Grand Slacks simulation runner")
    parser.add_argument("--ticks", type=int, default=10)
    parser.add_argument("--actors", type=int, default=180)
    parser.add_argument("--low-power", action="store_true", default=False)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = SimConfig(actor_count=args.actors, low_power_mode=args.low_power)
    sim = Simulation(config)
    for _ in range(args.ticks):
        report = sim.tick()
        print(
            f"tick={report.tick:03d} chunks={report.simulated_chunks:02d} "
            f"actors={report.actor_updates:03d} frame={report.elapsed_ms:0.2f}ms"
        )


if __name__ == "__main__":
    main()
