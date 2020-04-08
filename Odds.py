from dataclasses import dataclass


@dataclass
class Odds:
    estimate: float
    estimate_lower_ci: float
    estimate_upper_ci: float
    odds: float
    odds_lower_ci: float
    odds_upper_ci: float
    p: float
