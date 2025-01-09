import unittest
import pandas as pd
from main import create_dataframe, meal_records

class TestCreateDataFrame(unittest.TestCase):
    def setUp(self):
        meal_records.clear()

    def test_create_dataframe(self):
        meal_records.append({
            "날짜": "2025-01-09",
            "음식 이름": "apple",
            "식사 시간": "아침",
            "칼로리": 100,
            "단백질": 3,
            "탄수화물": 25,
            "지방": 1,
            "기록 시간": "2025-01-09 10:00:00"
        })

        df = create_dataframe()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.iloc[0]["음식 이름"], "apple")
