import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import re

# 한글 폰트 설정 (Nanum Gothic 예시)
plt.rc('font', family='NanumGothic')

# Nutritionix API 설정
API_URL = "https://trackapi.nutritionix.com/v2/natural/nutrients"
API_HEADERS = {
    "x-app-id": "3ca70f40",
    "x-app-key": "d42244c8bcd3039303637ad29615b7ed",
    "Content-Type": "application/json"
}

# 사용자 입력 기반 음식 섭취 기록
meal_records = []

# 음식 기록 함수
def log_meal():
    print("\n음식 기록을 추가합니다.")
    while True:
        date = input("날짜 (예: YYYY-MM-DD): ")
        try:
            datetime.strptime(date, "%Y-%m-%d")
            break
        except ValueError:
            print("날짜 형식이 올바르지 않습니다. 다시 입력하세요.")

    while True:
        food_item = input("음식 이름 (예: apple, cookie): ")
        if re.match(r'^[a-zA-Z]+$', food_item):
            break
        print("음식 이름은 영어로만 작성해야 합니다 (예: apple, cookie). 다시 입력하세요.")

    while True:
        serving_size = input("섭취량 및 단위 (예: 100g, 1컵): ")
        if re.match(r'^\d+(g|컵|ml|oz|kg|lb)$', serving_size.strip()):
            break
        print("섭취량은 숫자와 정확한 단위를 포함해야 합니다 (예: 100g, 1컵). 다시 입력하세요.")

    while True:
        meal_time = input("식사 시간 (아침, 점심, 저녁): ")
        if meal_time in ["아침", "점심", "저녁"]:
            break
        print("식사 시간은 '아침', '점심', '저녁' 중 하나여야 합니다. 다시 입력하세요.")

    response = requests.post(
        API_URL,
        headers=API_HEADERS,
        json={"query": f"{serving_size} {food_item} "}
    )

    if response.status_code == 200:
        data = response.json()
        nutrients = {
            "날짜": date,
            "음식 이름": food_item,
            "식사 시간": meal_time,
            "칼로리": data['foods'][0]['nf_calories'],
            "단백질": data['foods'][0]['nf_protein'],
            "탄수화물": data['foods'][0]['nf_total_carbohydrate'],
            "지방": data['foods'][0]['nf_total_fat'],
            "기록 시간": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        meal_records.append(nutrients)
        print(f"{food_item} 섭취 기록이 추가되었습니다.")
    else:
        print("음식 정보를 가져오는 데 실패했습니다. 다시 시도하세요.")

# 데이터프레임 생성
def create_dataframe():
    if not meal_records:
        return pd.DataFrame(columns=["날짜", "음식 이름", "식사 시간", "칼로리", "단백질", "탄수화물", "지방", "기록 시간"])
    return pd.DataFrame(meal_records)

# 날짜별 칼로리 및 영양소 비율 분석
def analyze_daily_nutrition(data):
    date = input("날짜를 입력하세요 (예: YYYY-MM-DD): ")
    daily_data = data[data["날짜"] == date]
    if daily_data.empty:
        print(f"{date} 날짜의 기록이 없습니다.")
        return

    # 식사 시간별 칼로리, 영양소 합계 및 음식 메뉴
    meal_groups = daily_data.groupby("식사 시간").agg({
        "칼로리": "sum",
        "단백질": "sum",
        "탄수화물": "sum",
        "지방": "sum",
        "음식 이름": lambda x: ', '.join(x)
    })

    # 총 영양소 비율 계산
    total_nutrition = daily_data[["칼로리", "단백질", "탄수화물", "지방"]].sum()
    total_calories = total_nutrition["칼로리"]
    carb_calories = total_nutrition["탄수화물"] * 4
    protein_calories = total_nutrition["단백질"] * 4
    fat_calories = total_nutrition["지방"] * 9

    # 각각의 비율 계산
    carb_ratio = (carb_calories / total_calories) * 100 if total_calories > 0 else 0
    protein_ratio = (protein_calories / total_calories) * 100 if total_calories > 0 else 0
    fat_ratio = (fat_calories / total_calories) * 100 if total_calories > 0 else 0

    # 영양소 비율 데이터프레임 생성
    nutrition_ratios = pd.DataFrame({
        "영양소": ["탄수화물", "단백질", "지방"],
        "비율 (%)": [carb_ratio, protein_ratio, fat_ratio]
    })

    # 출력
    print(f"\n=== {date} 날짜별 칼로리 및 영양소 분석 ===")
    print("\n[식사 시간별 총 섭취 칼로리 및 영양소]")
    print(meal_groups.to_string())

    # 아침/점심/저녁 칼로리 막대그래프
    plt.figure(figsize=(8, 6))
    meal_groups["칼로리"].plot(kind='bar', color='skyblue', legend=False)
    plt.title(f"{date} 식사 시간별 칼로리")
    plt.xlabel("식사 시간")
    plt.ylabel("칼로리")
    plt.xticks(rotation=0)
    plt.show()

    # 파이 차트 생성
    plt.figure(figsize=(6, 6))
    plt.pie(
        nutrition_ratios["비율 (%)"],
        labels=nutrition_ratios["영양소"],
        autopct="%1.1f%%",
        startangle=90,
        colors=sns.color_palette("pastel")
    )
    plt.title(f"{date} 날짜별 총 영양소 비율")
    plt.show()

    print("\n[식단 피드백]")
    print(f"총 칼로리: {total_calories:.2f} kcal")
    if carb_ratio > 55:
        print("- 탄수화물 섭취를 줄이세요.")
    if fat_ratio > 30:
        print("- 지방 섭취를 줄이세요.")
    if protein_ratio < 15:
        print("- 단백질 섭취를 늘리세요.")
    if total_calories > 2500:
        print("- 하루 칼로리 섭취량이 권장치를 초과했습니다. 조절이 필요합니다.")
    if total_calories < 1500:
        print("- 하루 칼로리 섭취량이 권장치보다 적습니다. 영양 섭취를 늘리세요.")
    print("- 수분 섭취를 잊지 마세요! 하루 2~3L의 물을 섭취하세요.")

    # 식사 시간별 패턴 피드백
    if "아침" in meal_groups.index:
        if meal_groups.loc["아침", "칼로리"] < 300:
            print("- 아침 식사의 칼로리가 낮습니다. 균형 잡힌 아침 식사를 섭취하세요.")
        elif meal_groups.loc["아침", "칼로리"] > 500:
            print("- 아침 식사의 칼로리가 높습니다. 섭취량을 적정 수준으로 조절하세요.")

    if "점심" in meal_groups.index:  # 점심 데이터가 있는 경우만 처리
        if meal_groups.loc["점심", "칼로리"] < 600:
            print("- 점심 식사의 칼로리가 낮습니다. 충분한 에너지를 섭취하세요.")
        elif meal_groups.loc["점심", "칼로리"] > 900:
            print("- 점심 식사의 칼로리가 높습니다. 섭취량을 조절하세요.")

    if "저녁" in meal_groups.index:  # 저녁 데이터가 있는 경우만 처리
        if meal_groups.loc["저녁", "칼로리"] < 400:
            print("- 저녁 식사의 칼로리가 낮습니다. 균형 잡힌 식사를 섭취하세요.")
        elif meal_groups.loc["저녁", "칼로리"] > 700:
            print("- 저녁 식사의 칼로리가 높습니다. 저녁 섭취량을 줄이고 가벼운 음식을 선택하세요.")

# 주간 보고서 생성
def analyze_weekly_nutrition(data):
    current_date = datetime.now()
    current_week = current_date.isocalendar().week
    current_year = current_date.year

    weekly_data = data[(data["날짜"] >= (current_date - pd.Timedelta(days=7)).strftime("%Y-%m-%d")) & (data["날짜"] <= current_date.strftime("%Y-%m-%d"))]
    if weekly_data.empty:
        print("이번 주의 기록이 없습니다.")
        return

    # 일별 총 칼로리 계산
    daily_calories = weekly_data.groupby("날짜")["칼로리"].sum()

    # 주간 총 영양소 비율 계산
    weekly_totals = weekly_data[["칼로리", "단백질", "탄수화물", "지방"]].sum()
    total_calories = weekly_totals["칼로리"]
    carb_calories = weekly_totals["탄수화물"] * 4
    protein_calories = weekly_totals["단백질"] * 4
    fat_calories = weekly_totals["지방"] * 9

    # 각각의 비율 계산
    carb_ratio = (carb_calories / total_calories) * 100 if total_calories > 0 else 0
    protein_ratio = (protein_calories / total_calories) * 100 if total_calories > 0 else 0
    fat_ratio = (fat_calories / total_calories) * 100 if total_calories > 0 else 0

    # 영양소 비율 데이터프레임 생성
    nutrition_ratios = pd.DataFrame({
        "영양소": ["탄수화물", "단백질", "지방"],
        "비율 (%)": [carb_ratio, protein_ratio, fat_ratio]
    })

    # 출력
    print(f"\n=== {current_year}년 {current_week}주차 주간 칼로리 및 영양소 분석 ===")
    print("\n[일별 총 칼로리]")
    print(daily_calories)

    # 파이 차트 생성
    plt.figure(figsize=(6, 6))
    plt.pie(
        nutrition_ratios["비율 (%)"],
        labels=nutrition_ratios["영양소"],
        autopct="%1.1f%%",
        startangle=90,
        colors=sns.color_palette("pastel")
    )
    plt.title(f"{current_year}년 {current_week}주차 주간 총 영양소 비율")
    plt.show()

    # 막대그래프 생성 (요일별 칼로리)
    plt.figure(figsize=(8, 6))
    day_of_week = {
        0: "월요일", 1: "화요일", 2: "수요일", 3: "목요일", 4: "금요일", 5: "토요일", 6: "일요일"
    }
    daily_calories.index = [
        f"{day_of_week[datetime.strptime(date, '%Y-%m-%d').weekday()]} ({date})"
        for date in daily_calories.index
    ]
    daily_calories.plot(kind="bar", color=sns.color_palette("pastel"))
    plt.title(f"{current_year}년 {current_week}주차 요일별 칼로리")
    plt.xlabel("날짜")
    plt.ylabel("칼로리")
    plt.xticks(rotation=45)
    plt.show()

    print("\n[식단 피드백]")
    print(f"총 칼로리: {total_calories:.2f} kcal")
    if carb_ratio > 55:
        print("- 탄수화물 섭취를 줄이세요.")
    if fat_ratio > 30:
        print("- 지방 섭취를 줄이세요.")
    if protein_ratio < 15:
        print("- 단백질 섭취를 늘리세요.")
    if total_calories > 17500:
        print("- 이번 주 칼로리 섭취량이 권장치를 초과했습니다. 조절이 필요합니다.")
    if total_calories < 10500:
        print("- 이번 주 칼로리 섭취량이 권장치보다 적습니다. 영양 섭취를 늘리세요.")  
    print("- 이번 주 물 섭취량을 체크하세요! 하루 2~3L를 유지하세요.")

    # 주간 트렌드 피드백
    high_calories_days = daily_calories[daily_calories > 2500]
    low_calories_days = daily_calories[daily_calories < 1200]

    if not high_calories_days.empty:
        print("- 다음 날들은 칼로리 섭취량이 너무 많습니다. 식단을 조절하세요:")
        for date, calories in high_calories_days.items():
            print(f"  {date}: {calories:.2f} kcal")

    if not low_calories_days.empty:
        print("- 다음 날들은 칼로리 섭취량이 너무 적습니다. 균형 잡힌 식사를 하세요:")
        for date, calories in low_calories_days.items():
            print(f"  {date}: {calories:.2f} kcal")

# 전체 기록 건강 상태 평가
def evaluate_health_status(data):
    if data.empty:
        print("기록된 데이터가 없습니다.")
        return

    grouped = data[["칼로리", "단백질", "탄수화물", "지방"]].sum()
    total_calories = grouped["칼로리"]
    carb_calories = grouped["탄수화물"] * 4
    protein_calories = grouped["단백질"] * 4
    fat_calories = grouped["지방"] * 9

    # 정규화된 비율 계산
    total_macros = carb_calories + protein_calories + fat_calories
    carb_ratio = (carb_calories / total_macros) * 100 if total_macros > 0 else 0
    protein_ratio = (protein_calories / total_macros) * 100 if total_macros > 0 else 0
    fat_ratio = (fat_calories / total_macros) * 100 if total_macros > 0 else 0

    # 정규화된 영양소 비율 데이터프레임 생성
    nutrition_ratios = pd.DataFrame({
        "영양소": ["탄수화물", "단백질", "지방"],
        "비율 (%)": [carb_ratio, protein_ratio, fat_ratio]
    })

    print("\n=== 전체 건강 상태 평가 ===")
    print(f"총 칼로리: {total_calories:.2f} kcal")
    print(nutrition_ratios.to_string(index=False))
    if carb_ratio > 55:
        print("- 탄수화물 섭취를 줄이세요.")
    if fat_ratio > 30:
        print("- 지방 섭취를 줄이세요.")
    if protein_ratio < 15:
        print("- 단백질 섭취를 늘리세요.")
    print("- 건강을 위해 물 섭취량을 확인하세요! 하루 2~3L를 유지하세요.")

# 메인 프로그램
def main():
    print("\n=== 개인 식사 기록 및 분석 프로그램 ===")
    while True:
        print("\n메뉴:")
        print("1. 음식 기록 추가")
        print("2. 일별 칼로리 및 영양소 비율 분석")
        print("3. 주간 칼로리 및 영양소 비율 분석")
        print("4. 전체 기록 건강 상태 평가")
        print("5. 종료")

        choice = input("메뉴를 선택하세요: ")

        if choice == "1":
            log_meal()
        elif choice == "2":
            data = create_dataframe()
            analyze_daily_nutrition(data)
        elif choice == "3":
            data = create_dataframe()
            analyze_weekly_nutrition(data)
        elif choice == "4":
            data = create_dataframe()
            evaluate_health_status(data)
        elif choice == "5":
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 선택입니다. 다시 시도하세요.")

if __name__ == "__main__":
    main()