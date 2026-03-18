# grand-slacks

`grand-slacks` is an emergent sci-fantasy RPG simulation prototype inspired by **Caves of Qud**, **RimWorld**, **Dwarf Fortress**, and **Cogmind**.

This iteration focuses on **scalability and old hardware support**:

- Chunk-based world simulation so only relevant regions are updated each tick.
- Adaptive performance governor that lowers simulation complexity when frame budget is exceeded.
- Low-power mode that halves active chunk processing cadence while keeping world state coherent.

## Run locally

```bash
python -m grand_slacks.cli --ticks 20 --actors 250 --low-power
```

## Test

```bash
python -m unittest discover -s tests -v
```

## Current architecture

- `grand_slacks/world.py`: world primitives (chunks, actors, movement).
- `grand_slacks/simulation.py`: tick loop, active-chunk scheduling, adaptive throttling.
- `grand_slacks/config.py`: hardware-targetable tuning knobs.

This is a foundation for future systems: procedural biomes, tactical combat, item simulation, colony jobs, and faction ecology.
