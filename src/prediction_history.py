from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime

@dataclass
class PredictionHistory:
    # Fields that are auto-generated
    id: Optional[int]
    

    # Fields populated by the user or application logic
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
@dataclass
class Device:
    # Fields that are auto-generated
    id: Optional[int]
    timestamp: Optional[datetime]
    

    # Fields populated by the user or application logic
    device_name: str
    device_type: str
    device_location: str
    device_status: str
    device_owner: str
    device_description: str


@dataclass 
class PredictionRecord:
    # Fields that are auto-generated
    id: Optional[int]
    timestamp: Optional[datetime] 

    # Fields populated by the user or application logic
    run_frequency: int
    device_id: int
    air_temp: float
    process_temp: float
    rotational_speed: int
    torque: float
    tool_wear: float
    energy_source: int
    prediction_type: str
    confidence_level: float
    carbon_intensity: float
    carbon_footprint: float
    