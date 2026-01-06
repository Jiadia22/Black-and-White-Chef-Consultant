👨‍🍳 AI 흑백요리사 맛집 컨설턴트
AI 흑백요리사 맛집 컨설턴트는 사용자의 취향(장르)에 맞춰 '흑백요리사' 셰프들의 식당을 추천하고, 심사위원(백종원, 안성재)의 개성을 살린 AI 심사평을 즉석에서 제공하는 웹 서비스입니다.

🚀 프로젝트 개요
이 프로젝트는 FastAPI를 백엔드로, Streamlit을 프런트엔드로 사용하여 구축되었습니다. MongoDB에 저장된 실제 셰프들의 식당 데이터를 기반으로 하며, OpenAI의 GPT-4o 모델을 활용해 실감 나는 심사평을 생성합니다.

🛠 사용 기술 (Tech Stack)
Frontend: Streamlit

Backend: FastAPI (Uvicorn)

Database: MongoDB

AI: OpenAI API (GPT-4o)

Language: Python 3.x

🔄 서비스 흐름 (Service Flow)
데이터 초기화 (setup.py): 셰프 및 식당 정보(이름, 장르, 위치 등)를 로컬 MongoDB에 저장합니다.

사용자 인터페이스 (app3.py): 사용자가 원하는 음식 장르와 전담 심사위원을 선택하고 '추천받기'를 클릭합니다.

식당 선정 (Random Selection): Streamlit 앱이 MongoDB에서 조건에 맞는 식당 중 하나를 랜덤으로 선정합니다.

AI 심사평 요청: 선정된 식당 이름과 심사위원 정보를 FastAPI 서버로 전송합니다.

AI 답변 생성 (main.py): FastAPI는 받은 정보를 바탕으로 GPT-4o에게 심사위원의 말투를 재현한 심사평 생성을 요청합니다.

결과 출력: 추천 식당 정보, 지도 링크(카카오/구글), 그리고 AI 심사평을 사용자 화면에 한 번에 보여줍니다.

📝 주요 기능
맞춤형 추천: 한식, 일식, 중식, 양식 등 장르별 필터링 기능.

심사위원 페르소나:

백종원: 구수한 사투리와 대중적인 맛, 가성비 중심의 조언.

안성재: 깐깐한 익힘 정도, 셰프의 의도를 파악하는 논리적 분석.

지도 연동: 추천된 식당을 바로 찾아갈 수 있도록 카카오맵, 구글 지도 검색 링크 자동 생성.

실시간 AI 인터랙션: 버튼 클릭 한 번으로 식당 선정부터 맛 평가까지 즉시 로딩.

📂 파일 구조
setup.py: 데이터베이스 초기 설정 및 데이터 삽입 스크립트.

main.py: OpenAI API 연동 및 심사평 생성을 담당하는 API 서버.

app3.py: 사용자 화면 구현 및 식당 추천 로직을 담은 메인 앱.

⚙️ 실행 방법
MongoDB 실행: 로컬 환경에서 MongoDB 서비스가 실행 중이어야 합니다.

데이터 삽입:

Bash

python setup.py
Backend(FastAPI) 서버 실행:

Bash

uvicorn main:app --reload
Frontend(Streamlit) 실행:

Bash

streamlit run app3.py
Developed with ❤️ using FastAPI, MongoDB, and Streamlit.
