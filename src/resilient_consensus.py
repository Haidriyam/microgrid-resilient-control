"""
Secondary Frequency Consensus Protocol with Attack Resilient Filtering.
Protects microgrid inverters against False Data Injection (FDI) and packet drops.
"""
from typing import List, Tuple


class ResilientConsensusEngine:
    def __init__(self, f_nominal: float = 50.0, f_threshold: float = 0.5):
        self.f_nominal = f_nominal
        self.f_threshold = f_threshold

    def sanitize_neighbor_telemetry(
        self,
        local_freq: float,
        neighbor_broadcasts: List[float]
    ) -> List[float]:
        """
        Filter out False Data Injection (FDI) attacks using a local bounding check.
        Nodes broadcasting data deviating beyond physical bounds are rejected.
        """
        sanitized = []
        for reading in neighbor_broadcasts:
            if abs(reading - local_freq) <= self.f_threshold:
                sanitized.append(reading)
            else:
                print(f"[SECURITY ALERT] FDI anomaly dropped: {reading:.2f} Hz from cluster")
        return sanitized

    def compute_secondary_correction(
        self,
        local_freq: float,
        neighbor_broadcasts: List[float],
        k_consensus: float = 0.15
    ) -> float:
        """
        Consensus algorithm for secondary frequency restoration:
        Delta_f = K_rest * (f_nom - f_i) + K_cons * Sum(A_ij * (f_j - f_i))
        """
        valid_neighbors = self.sanitize_neighbor_telemetry(local_freq, neighbor_broadcasts)

        restoration_term = (self.f_nominal - local_freq)

        if valid_neighbors:
            consensus_term = sum((f_j - local_freq) for f_j in valid_neighbors)
        else:
            consensus_term = 0.0

        return (0.2 * restoration_term) + (k_consensus * consensus_term)


def run_simulation() -> Tuple[float, float]:
    """Demonstrate secondary restoration with and without FDI attack."""
    engine = ResilientConsensusEngine()
    inverter_local_f = 49.3

    incoming_data = [49.32, 49.28, 59.80]

    correction = engine.compute_secondary_correction(inverter_local_f, incoming_data)
    restored_f = inverter_local_f + correction
    return inverter_local_f, restored_f


if __name__ == "__main__":
    init_f, new_f = run_simulation()
    print(f"[*] Initial Sagged Freq: {init_f:.2f} Hz | Corrected Freq: {new_f:.2f} Hz")
