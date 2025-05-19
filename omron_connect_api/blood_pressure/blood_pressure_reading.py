from dataclasses import dataclass
from datetime import datetime
from typing import TypeAlias

mmHg: TypeAlias = int
bpm: TypeAlias = int
count: TypeAlias = int


@dataclass()
class BloodPressureReading:
    measurement_date: datetime
    diastolic: mmHg
    systolic: mmHg
    pulse: bpm
    irregular_heart_beats: count
    movements: count
