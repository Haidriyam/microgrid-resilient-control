import unittest
from src.microgrid_sim import InverterUnit
from src.resilient_consensus import ResilientConsensusEngine


class TestMicrogridResilience(unittest.TestCase):

    def setUp(self):
        self.inverter = InverterUnit(inverter_id=1, p_rated=100.0)
        self.engine = ResilientConsensusEngine(f_nominal=50.0, f_threshold=0.5)

    def test_primary_droop_sag(self):
        f_droop = self.inverter.calculate_primary_frequency(active_load=200.0)
        # f = 50.0 - (0.002 * 200) = 49.6 Hz
        self.assertEqual(f_droop, 49.6)

    def test_fdi_attack_filtering(self):
        # Local is 49.6; malicious node injects 55.0 Hz
        raw_telemetry = [49.55, 49.62, 55.00]
        sanitized = self.engine.sanitize_neighbor_telemetry(49.6, raw_telemetry)
        self.assertNotIn(55.00, sanitized)
        self.assertEqual(len(sanitized), 2)

    def test_consensus_restores_frequency_toward_nominal(self):
        local_f = 49.6
        raw_telemetry = [49.6, 49.58]
        correction = self.engine.compute_secondary_correction(local_f, raw_telemetry)
        # Correction must be positive to drive frequency back to 50 Hz
        self.assertGreater(correction, 0.0)


if __name__ == "__main__":
    unittest.main()