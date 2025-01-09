import unittest
from unittest.mock import patch
from main import log_meal, meal_records

class TestLogMeal(unittest.TestCase):
    def setUp(self):
        meal_records.clear()

    @patch('requests.post')
    def test_log_meal(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "foods": [{
                "nf_calories": 100,
                "nf_protein": 3,
                "nf_total_carbohydrate": 25,
                "nf_total_fat": 1
            }]
        }

        with patch('builtins.input', side_effect=["2025-01-09", "apple", "100g", "아침"]):
            log_meal()
        
        self.assertEqual(len(meal_records), 1)
        self.assertEqual(meal_records[0]["음식 이름"], "apple")
        self.assertEqual(meal_records[0]["칼로리"], 100)
