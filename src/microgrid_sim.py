"""
Nonlinear Inverter Droop Dynamic Simulator for Islanded AC Microgrid.
Models primary P-f and Q-V droop characteristics of grid-forming (GFM) inverters.
"""
from dataclasses import dataclass


@dataclass
class InverterUnit:
    inverter_id: int
    p_rated: float       # kW
    f_nominal: float = 50.0  # Hz
    k_droop: float = 0.002   # Droop coefficient (Hz/kW)

    def calculate_primary_frequency(self, active_load: float) -> float:
        """Calculate steady-state frequency under primary droop control: f = f_nom - k*P."""
        if active_load < 0:
            raise ValueError("Load demand must be non-negative.")
        return self.f_nominal - (self.k_droop * active_load)