# 👨‍🍳 AI 흑백요리사 맛집 컨설턴트 (AI Black-and-White Chef Consultant)

**AI 흑백요리사 맛집 컨설턴트**는 넷플릭스 '흑백요리사'에 출연한 셰프들의 식당을 사용자 취향에 맞춰 추천해주는 웹 서비스입니다. 
단순한 정보 제공을 넘어, **백종원**, **안성재** 심사위원의 개성을 그대로 살린 **AI 심사평**을 실시간으로 들려드립니다.

---

## 🚀 프로젝트 개요
이 서비스는 **FastAPI** 백엔드와 **Streamlit** 프런트엔드를 연동하여 개발되었습니다. **MongoDB**에 저장된 셰프들의 식당 데이터를 활용하며, **OpenAI의 GPT-4o** 모델을 통해 각 심사위원의 페르索나(Persona)가 반영된 맞춤형 맛 평가를 생성합니다.

---

## 🛠 사용 기술 (Tech Stack)
* **Frontend**: `Streamlit`
* **Backend**: `FastAPI` (Uvicorn)
* **Database**: `MongoDB`
* **AI Model**: `OpenAI API (GPT-4o)`
* **Language**: `Python 3.11`

---

## 🔄 서비스 흐름 (Service Flow)



1.  **데이터 초기화 (`setup.py`)**: 셰프 및 식당 정보(이름, 장르, 위치 등)를 로컬 MongoDB에 저장합니다.
2.  **사용자 인터페이스 (`app3.py`)**: 사용자가 원하는 음식 장르와 전담 심사위원을 선택하고 '추천받기' 버튼을 클릭합니다.
3.  **식당 선정 (Random Selection)**: Streamlit 앱이 MongoDB에서 조건에 맞는 식당 중 하나를 무작위로 선정합니다.
4.  **AI 심사평 요청**: 선정된 식당 이름과 심as위원 정보를 FastAPI 서버(`/ai-recommend`)로 전송합니다.
5.  **AI 답변 생성 (`main.py`)**: FastAPI는 받은 정보를 바탕으로 GPT-4o에게 심사위원의 말투와 평가 기준을 적용한 심사평 생성을 요청합니다.
6.  **결과 출력**: 추천 식당 정보, 지도 링크(카카오/구글), 그리고 생생한 AI 심사평을 한 화면에 보여줍니다.

---

## 📝 주요 기능
* **장르별 맛집 추천**: 한식, 일식, 중식, 양식 등 카테고리별 필터링 기능.
* **심사위원 페르소나 적용**: 
    * **백종원**: 구수한 충청도 사투리, 대중적인 맛과 가성비 중심의 따뜻한 조언.
    * **안성재**: 깐깐한 익힘 정도, 셰프의 의도를 파악하는 날카롭고 논리적인 분석.
* **지도 플랫폼 연동**: 추천 식당 이름을 기반으로 카카오맵 및 구글 지도 검색 링크 제공.
* **원클릭 서비스**: 버튼 클릭 한 번으로 '식당 선정 - 상세 정보 확인 - AI 심사평'까지 즉시 확인 가능.

---

## 📂 파일 구조
* `setup.py`: 데이터베이스 초기화 및 기초 데이터(Seed Data) 삽입.
* `main.py`: OpenAI API 연동 및 심사평 생성 로직을 포함한 API 서버.
* `app3.py`: Streamlit을 이용한 사용자 화면 구성 및 추천 로직 제어.
* `.env`: API Key 등 보안 민감 정보 관리 (깃허브 업로드 제외 대상).

---

## ⚙️ 실행 방법

1. **MongoDB 실행**: 로컬 환경에서 MongoDB가 작동 중인지 확인합니다.
2. **필수 라이브러리 설치**:
   pip install fastapi uvicorn pymongo openai python-dotenv streamlit requests
3. 데이터 삽입: python setup.py,
  Backend(FastAPI) 서버 실행: uvicorn main:app --reload,
  Frontend(Streamlit) 실행: streamlit run app3.py,
