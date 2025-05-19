import unittest
from datetime import datetime, timezone
from omron_connect_api.blood_pressure.blood_pressure_reading_response import BloodPressureReadingResponse


class TestBloodPressureReadingResponse(unittest.TestCase):

    def test_parses_json(self):
        reading = BloodPressureReadingResponse.from_json(
            {
                'measurementDate': '1747615042000',
                'diastolic': 82,
                'systolic': 103,
                'pulse': 62,
                'countIrregularHeartBeat': '2',
                'movementDetect': 1
            }
        )
        datetime_in_utc = datetime(2025, 5, 19, 0, 37, 22, tzinfo=timezone.utc)
        self.assertEqual(reading.measurement_date, datetime_in_utc)
        self.assertEqual(reading.diastolic, 82)
        self.assertEqual(reading.systolic, 103)
        self.assertEqual(reading.pulse, 62)
        self.assertEqual(reading.irregular_heart_beats, 2)
        self.assertEqual(reading.movements, 1)
