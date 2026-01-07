# 👨‍🍳 AI 흑백요리사 맛집 컨설턴트 (AI Black-and-White Chef Consultant)

**AI 흑백요리사 맛집 컨설턴트**는 넷플릭스 '흑백요리사' 출연 셰프들의 식당을 사용자 취향에 맞춰 추천하고, 심사위원의 페르소나를 빌려 실시간 심사평을 제공하는 인텔리전트 맛집 추천 서비스입니다.

단순한 DB 조회를 넘어, **Perplexity AI를 통한 실시간 메뉴 검색**과 **GPT-4o의 고도화된 페르소나 분석**을 결합하여 실제와 가까운 미식 경험을 제공합니다.

---

## 🚀 프로젝트 주요 업데이트 (Refactoring)
* **하드코딩 제거**: 식당 데이터(`restaurants.txt`)와 UI 스타일(`styles.py`)을 로직에서 완벽히 분리하여 유지보수성을 높였습니다.
* **실시간 데이터 강화**: `Perplexity AI (sonar-pro)`를 연동하여, DB에 없는 식당의 최신 인기 메뉴를 실시간으로 수집합니다.
* **관심사 분리 (SoC)**: 데이터 적재(Setup), 비즈니스 로직(API Server), 사용자 인터페이스(UI)를 독립적인 파일로 구조화했습니다.

---

## 🛠 사용 기술 (Tech Stack)
* **Frontend**: `Streamlit`, `Streamlit-Extras` (Rain 효과)
* **Backend**: `FastAPI` (Uvicorn 비동기 서버)
* **Database**: `MongoDB` (NoSQL)
* **AI Models**: 
    * `OpenAI GPT-4o` (심사평 생성)
    * `Perplexity AI sonar-pro` (실시간 메뉴 데이터 분석 및 검색)
* **Language**: `Python 3.11+`

---

## 🔄 서비스 아키텍처 (Service Architecture)

1. **Data Ingestion (`setup.py`)**: `restaurants.txt`에서 원천 데이터를 읽어 MongoDB에 체계적으로 적재합니다.
2. **User Request (`app.py`)**: 사용자가 장르와 심사위원(안성재/백종원)을 선택합니다.
3. **Smart Selection**: MongoDB 쿼리를 통해 조건에 맞는 식당을 무작위로 선정하고 화려한 UI 효과(`Rain`)를 출력합니다.
4. **Real-time Analysis (`main.py`)**:
    * **Step 1**: Perplexity AI가 해당 식당의 최신 블로그 리뷰를 분석하여 시그니처 메뉴 Top 3를 추출합니다.
    * **Step 2**: GPT-4o가 추출된 메뉴 정보를 바탕으로 선택된 심사위원의 말투와 기준에 맞춘 심사평을 생성합니다.
5. **Interactive UI**: `styles.py`에 정의된 모던 다크 테마 박스를 통해 추천 결과와 지도 링크를 사용자에게 즉시 보여줍니다.

---

## 📝 주요 기능
* **실시간 인기 메뉴 추출**: 웹 검색을 통해 식당의 가장 최신 인기 메뉴 2가지를 함께 추천합니다.
* **심사위원 페르소나 극대화**: 
    * **백종원**: "이거 재밌네~", "예술이에유~" 등 구수한 말투와 가성비 중심 평가.
    * **안성재**: "익힘 정도", "셰프의 의도", "이븐(Even)함"을 강조하는 논리적 분석.
* **모던 다크 UI/UX**: 사용자 경험을 고려한 다크 테마 디자인과 이모지 애니메이션.
* **멀티 지도 연동**: 카카오맵과 구글 지도 링크를 동시에 제공하여 접근성 극대화.

---

## 📂 파일 구조
* `restaurants.txt`: 관리하기 쉬운 텍스트 형식의 맛집 원천 데이터.
* `setup.py`: 데이터 파싱 및 MongoDB 적재 로직.
* `main.py`: FastAPI 서버 및 AI(OpenAI, Perplexity) 연동 코어.
* `app.py`: Streamlit 기반의 인터랙티브 웹 프론트엔드.
* `styles.py`: HTML/CSS 템플릿 및 UI 설정 관리.
* `requirements.txt`: 프로젝트 실행을 위한 라이브러리 의존성 목록.
* `.env`: API Key 보안 관리 (환경변수).

---

## ⚙️ 실행 방법 (How to Run)

### 1. 환경 설정 (Environment Setup)
프로젝트 루트 폴더에 `.env` 파일을 생성하고 아래 키를 입력합니다.
```env
OPENAI_API_KEY=your_openai_key
PPLX_API_KEY=your_perplexity_key
```

### 2. 패키지 설치 (Install Dependencies)
```bash
pip install -r requirements.txt
```

### 3. 데이터 적재 (Data Ingestion)
**사전 요구사항**: 로컬 환경에 MongoDB가 설치되어 있고 실행 중(`localhost:27017`)이어야 합니다.
```bash
python setup.py
```
> "🎉 가공 완료! 총 ...개의 진짜 맛집을 DB에 넣었습니다." 메시지가 나오면 성공입니다.

### 4. 백엔드 서버 실행 (Backend Server)
FastAPI 서버를 실행하여 AI 로직과 DB 연동을 처리합니다.
```bash
uvicorn main:app --reload
```
> 터미널에 `Application startup complete.` 메시지가 뜨면 준비 완료입니다.

### 5. 프론트엔드 실행 (Frontend App)
**새로운 터미널**을 열고 Streamlit 앱을 실행합니다.
```bash
streamlit run app.py
```
> 브라우저가 자동으로 열리며 서비스를 사용할 수 있습니다.
