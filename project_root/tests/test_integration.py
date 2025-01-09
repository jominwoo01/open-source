import sys
import os

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch
from main import log_meal, create_dataframe, analyze_daily_nutrition, analyze_weekly_nutrition, evaluate_health_status, meal_records

class TestIntegration(unittest.TestCase):
    def setUp(self):
        meal_records.clear()  # 테스트 전 데이터 초기화

    @patch('requests.post')
    def test_full_workflow(self, mock_post):
        # Mock API 응답 설정
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "foods": [{
                "nf_calories": 100,
                "nf_protein": 3,
                "nf_total_carbohydrate": 25,
                "nf_total_fat": 1
            }]
        }

        # Step 1: 음식 기록 (log_meal)
        with patch('builtins.input', side_effect=["2025-01-10", "apple", "100g", "아침"]):
            log_meal()
        self.assertEqual(len(meal_records), 1)  # 데이터가 추가되었는지 확인

        # Step 2: 데이터프레임 생성 (create_dataframe)
        df = create_dataframe()
        self.assertEqual(df.shape[0], 1)  # 데이터프레임의 행 개수 확인
        self.assertEqual(df.iloc[0]["칼로리"], 100)  # 칼로리 값 확인

        # Step 3: 날짜별 영양소 분석 (analyze_daily_nutrition)
        with patch('builtins.input', return_value="2025-01-10"), patch('matplotlib.pyplot.show'):
            analyze_daily_nutrition(df)  # 분석 수행 (시각화 무시)

        # Step 4: 주간 영양소 분석 (analyze_weekly_nutrition)
        with patch('matplotlib.pyplot.show'):
            analyze_weekly_nutrition(df)

        # Step 5: 전체 건강 상태 평가 (evaluate_health_status)
        with patch('matplotlib.pyplot.show'):
            evaluate_health_status(df)

if __name__ == "__main__":
    unittest.main()
