from dataclasses import dataclass
from datetime import datetime

@dataclass
class PredictionHistory:
    id: int
    air_temp: float
    process_temp: float
    rotational_speed: int
    torque: float
    tool_wear: float
    energy_source: int
    timestamp: datetime
    prediction_type: str
    confidence_level: float
    carbon_intensity: float
    carbon_footprint: float