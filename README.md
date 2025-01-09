# 개인 식사 기록 및 영양소 분석 프로그램

## 소개

이 프로그램은 개인의 식사 기록을 기반으로 칼로리, 단백질, 탄수화물, 지방과 같은 영양소를 분석하여 건강한 식단 관리를 돕습니다. 사용자는 음식 기록을 추가하고, 날짜별 및 주간 영양소 분석, 건강 상태 평가 등의 기능을 활용할 수 있습니다.

---

## 주요 기능

1. **음식 기록 추가**:

   - 날짜, 음식 이름, 섭취량 및 식사 시간을 입력하여 기록.
   - Nutritionix API를 통해 음식의 칼로리와 영양소 정보를 자동으로 가져옵니다.

2. **날짜별 영양소 분석**:

   - 특정 날짜의 식사 데이터를 기반으로 칼로리 및 영양소 비율을 분석.
   - 분석 결과를 그래프와 함께 제공.

3. **주간 영양소 분석**:

   - 최근 일주일 동안의 식사 데이터를 분석.
   - 요일별 칼로리 및 영양소 비율을 시각화.

4. **전체 건강 상태 평가**:

   - 모든 기록을 기반으로 영양소 섭취 비율 및 칼로리 소비 상태를 평가.
   - 건강한 식단을 위한 피드백 제공.

5. **데이터 시각화**:

   - 날짜별 및 주간 데이터를 그래프로 보여줍니다.
   - 탄수화물, 단백질, 지방의 비율을 한눈에 확인할 수 있습니다.

---

## 설치 방법

### 1. 클론 또는 다운로드

이 저장소를 로컬로 클론하거나 ZIP 파일로 다운로드하세요.

```bash
# 저장소 클론
git clone https://github.com/your-repo-url.git
cd your-repo-url
```

### 2. 의존성 설치

Python 3.9 이상이 설치되어 있어야 합니다. 다음 명령어로 필요한 라이브러리를 설치하세요:

```bash
pip install -r requirements.txt
```

### 3. 실행

아래 명령어로 프로그램을 실행하세요:

```bash
python main.py
```

---

## 사용 방법

### 1. 프로그램 시작

프로그램을 실행하면 아래와 같은 메뉴가 표시됩니다:

```text
=== 개인 식사 기록 및 분석 프로그램 ===

메뉴:
1. 음식 기록 추가
2. 일별 칼로리 및 영양소 비율 분석
3. 주간 칼로리 및 영양소 비율 분석
4. 전체 기록 건강 상태 평가
5. 종료
```

### 2. 음식 기록 추가

- 메뉴에서 `1`을 선택하여 음식 기록을 추가합니다.
- 날짜, 음식 이름, 섭취량, 식사 시간을 입력하면 해당 음식의 영양소 정보가 자동으로 저장됩니다.

### 3. 일별 영양소 분석

- 메뉴에서 `2`를 선택하여 특정 날짜의 식사 데이터를 분석합니다.
- 분석 결과는 텍스트 및 그래프 형태로 제공됩니다.

### 4. 주간 영양소 분석

- 메뉴에서 `3`을 선택하여 최근 7일간의 데이터를 분석합니다.
- 요일별 칼로리 및 영양소 비율이 시각화됩니다.

### 5. 건강 상태 평가

- 메뉴에서 `4`를 선택하여 전체 데이터를 기반으로 건강 상태를 평가합니다.
- 현재 식단의 문제점을 지적하고 개선점을 제안합니다.

---

## 테스트 방법

### 유닛 테스트

- 프로그램의 주요 함수들이 독립적으로 올바르게 작동하는지 확인합니다.
- 다음 명령어로 유닛 테스트를 실행하세요:

```bash
python -m unittest discover -s tests
```

### 통합 테스트

- 전체 워크플로우(입력 → 처리 → 분석)가 정상적으로 동작하는지 확인합니다.
- 통합 테스트 실행:

```bash
python tests/test_integration.py
```

---

## GitHub Actions

- 이 저장소는 GitHub Actions를 사용하여 자동으로 테스트를 실행합니다.
- 코드 푸시 또는 Pull Request 시 모든 테스트가 자동 실행됩니다.

---

## 사용 시 유의사항

1. **Nutritionix API 키**:

   - 프로그램을 실행하기 위해 Nutritionix API 키가 필요합니다.
   - `main.py` 파일에서 API 키를 설정하세요:
     ```python
     API_HEADERS = {
         "x-app-id": "your-app-id",
         "x-app-key": "your-app-key",
         "Content-Type": "application/json"
     }
     ```

2. **Python 버전**:

   - Python 3.9 이상이 필요합니다.

3. **테스트 데이터**:

   - 테스트 실행 시 Mock 데이터를 사용하므로, API 호출이 실제로 이루어지지 않습니다.

---

## 기여 방법

1. 이 저장소를 Fork 하세요.
2. 새로운 브랜치를 생성하세요:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. 변경사항을 커밋하고 푸시하세요:
   ```bash
   git commit -m "Add your commit message"
   git push origin feature/your-feature-name
   ```
4. Pull Request를 생성하세요.

---

