from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class Station:
    name: str
    distance_from_start: int
    chargers: int


@dataclass
class Bus:
    id: str
    operator: str
    direction: str
    departure_time: str


@dataclass
class ChargeEvent:
    station: str
    arrival_time: int
    wait_time: int
    charge_start: int
    charge_end: int
    departure_time: int


@dataclass
class BusSchedule:
    bus_id: str
    operator: str
    direction: str
    charge_events: List[ChargeEvent] = field(default_factory=list)
    final_arrival: int = 0
    total_wait: int = 0