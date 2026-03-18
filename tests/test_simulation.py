import unittest

from grand_slacks.config import SimConfig
from grand_slacks.simulation import Simulation


class SimulationTests(unittest.TestCase):
    def test_tick_progresses_and_updates_actors(self) -> None:
        sim = Simulation(SimConfig(actor_count=40, max_active_chunks=8, low_power_mode=False))
        report = sim.tick()
        self.assertEqual(report.tick, 1)
        self.assertGreater(report.simulated_chunks, 0)
        self.assertGreaterEqual(report.actor_updates, 0)

    def test_low_power_mode_reduces_chunk_budget(self) -> None:
        cfg = SimConfig(actor_count=20, max_active_chunks=10, low_power_mode=True)
        sim = Simulation(cfg)
        active = sim._pick_active_chunks()
        self.assertLessEqual(len(active), 5)

    def test_auto_throttle_when_over_budget(self) -> None:
        sim = Simulation(SimConfig(actor_count=200, max_active_chunks=10, max_tick_ms=0, low_power_mode=False))
        before = sim.config.max_active_chunks
        _ = sim.tick()
        self.assertLess(sim.config.max_active_chunks, before)


if __name__ == "__main__":
    unittest.main()
