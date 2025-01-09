import unittest
from unittest.mock import patch
from main import analyze_weekly_nutrition, create_dataframe, meal_records

class TestAnalyzeWeeklyNutrition(unittest.TestCase):
    def setUp(self):
        meal_records.clear()

    def test_analyze_weekly_nutrition(self):
        meal_records.append({
            "날짜": "2025-01-08",
            "음식 이름": "apple",
            "식사 시간": "아침",
            "칼로리": 95,
            "단백질": 0.5,
            "탄수화물": 25,
            "지방": 0.3,
            "기록 시간": "2025-01-08 10:00:00"
        })
        data = create_dataframe()

        with patch('matplotlib.pyplot.show'):  # 시각화 무시
            analyze_weekly_nutrition(data)

        self.assertEqual(data["칼로리"].sum(), 95)
