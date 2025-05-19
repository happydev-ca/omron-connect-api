from datetime import datetime, timezone
from typing import Any, Dict

from .. import BloodPressureReading


class BloodPressureReadingResponse:

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> BloodPressureReading:
        return BloodPressureReading(
            measurement_date=datetime.fromtimestamp(int(data['measurementDate'])/1000, timezone.utc),
            diastolic=data['diastolic'],
            systolic=data['systolic'],
            pulse=data['pulse'],
            irregular_heart_beats=int(data['countIrregularHeartBeat']),
            movements=data['movementDetect']
        )
