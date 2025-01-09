import unittest
from unittest.mock import patch
from main import evaluate_health_status, create_dataframe, meal_records

class TestEvaluateHealthStatus(unittest.TestCase):
    def setUp(self):
        meal_records.clear()

    def test_evaluate_health_status(self):
        meal_records.append({
            "날짜": "2025-01-09",
            "음식 이름": "apple",
            "식사 시간": "아침",
            "칼로리": 95,
            "단백질": 0.5,
            "탄수화물": 25,
            "지방": 0.3,
            "기록 시간": "2025-01-09 10:00:00"
        })
        data = create_dataframe()

        with patch('matplotlib.pyplot.show'):  # 시각화 무시
            evaluate_health_status(data)

        self.assertEqual(data["칼로리"].sum(), 95)
