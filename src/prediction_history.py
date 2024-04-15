from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime

@dataclass
class PredictionHistory:
    # Fields that are auto-generated
    id: Optional[int]
    
    air_temp: float
    process_temp: float
    rotational_speed: int
    torque: float
    tool_wear: float
    energy_source: int
    timestamp: Optional[datetime]
    prediction_type: str
    confidence_level: float
    carbon_intensity: float
    carbon_footprint: float
    run_frequency:int
    label0:float
    label1:float
    label2:float
    label3:float
    label4:float
    label: Optional[str]
