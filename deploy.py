import streamlit as st
from openai import OpenAI
import random
import re
from streamlit_extras.let_it_rain import rain

# ==========================================
# 1. 데이터 영역 (setup.py 내용을 그대로 가져옴)
# ==========================================
# 님께서 작성하신 데이터 원본입니다.
raw_data = """
<한식>
심성철 - Mari, Kochi(뉴욕)
선재스님 - 사찰음식
임성근 - 식당 미공개
이금희 - 봉래헌
김도윤 - 윤서울, 면서울
제니월튼 - Namu, Gaji(말뫼)
김상훈 - 독도16도
옥동식 - 옥동식, 옥동식그릴
이정수 - 온6.5
윤대현 - 옥돌현옥
남성렬 - 신안가옥
윤나라 - 윤주당
명현지 - 아선재
우정욱 - 수퍼판
채명희 - 은진포차
양수현 - 바삭마차
권옥식 - 급이다른부대찌개
방효숙 - 구들장흑도야지
이정서 - 힙한식
유금안 - 외암파전상전
김효숙 - 절라도
사이먼리(이영주) - Kisa
이선희 - 김치 명인
<고기>
유용욱 - 이목스모크다이닝, 유용욱바베큐연구소
황지훈 - 콘래드서울숯
<일식>
김건 - 고료리켄, 이치에, 회현식당/카페
정호영 - 카덴, 우동카덴
최강록 - 식당 미공개
박주성 - 소바쥬
신현도 - 모노로그
최규덕 - 미가키
나원계 - 호루몬
배재훈 - 갓포아키, 타카
신동민 - 멘야미코, 당옥
윤태호 - 키이로
박세효 - 죠죠
권민택 - 고미태
윤석환 - 칸세이
김태우 - 동경밥상, 오코메
<중식>
후덕죽 - 호빈
최유강 - 코자차
천상현 - 천상현의천상
신계숙 - 계향각
장보원 - 보보식당
담소룡 - 동보성
윤진원 - 무탄
김혜규 - 뼈대있는짬뽕
<양식>
이준 - 스와니예, 도우룸
손종원 - 이타닉가든, 라망시크레
김희은 - 소울, 에그앤플라워
송훈 - 크라운돼지
샘킴 - 오스테리아샘킴
김성운 - 테이블포포
임홍근 - 페리지
김훈 - 쌤쌤쌤, 테디뵈르하우스
타미리 - 비스트로드욘트빌
전지호 - 랑빠스81, 바라핀부쉬, 이태원실비/디스코
이찬양 - 오리지널넘버스
이재훈 - 까델루뽀
김호윤 - 더이탈리안클럽, 호시우보, 중식당청
윤아름 - 비스트로앤트로
김석현 - 몽도
김진래 - 서울다이닝
황제 - 래빗홀버거
손영철 - 보타르가비노
박가람 - 드레스덴그린
고효일 - 셰누프라이빗키친
김준형 - 레스토랑온
송호윤 - 양출서울
박정현 - 포그
김재호 - 디어그랜마
<세계음식>
김도형 - 만가타
원성훈 - 라오삐약
<퓨전>
김용성 - 중앙감속기, 중앙가속기
<분식>
김두래 - 떡산
정시우 - 삼미분식
<디저트>
임하선 - 파티세리후르츠, 피엔에이
"""

# setup.py의 로직을 그대로 사용하여 리스트를 만듭니다.
def get_database():
    lines = raw_data.strip().split('\n')
    final_data = []
    current_genre = ""

    for line in lines:
        line = line.strip()
        if not line: continue
        
        # 장르 처리
        if line.startswith('<') and line.endswith('>'):
            current_genre = line[1:-1]
        
        # 데이터 처리
        elif ' - ' in line:
            chef, restaurants = line.split(' - ')
            res_list = re.split(',|/', restaurants)
            for res in res_list:
                res_name = res.strip()
                if "미공개" not in res_name and "명인" not in res_name:
                    final_data.append({
                        "장르": current_genre,
                        "셰프": chef.strip(),
                        "식당명": res_name
                    })
    return final_data

# ==========================================
# 2. 로직 영역 (main.py 내용을 그대로 가져옴)
# ==========================================

# main.py에 있던 함수 1: Perplexity 검색 (워딩 그대로 유지)
def search_menu_with_perplexity(restaurant_name, chef_name, genre, api_key):
    # 키 설정
    client_pplx = OpenAI(api_key=api_key, base_url="https://api.perplexity.ai")
    
    try:
        response = client_pplx.chat.completions.create(
            model="sonar-pro",
            messages=[
                {
                    "role": "system",
                    "content": "너는 여러 개의 정보를 취합하여 공통점을 찾아내는 데이터 분석가야."
                },
                {
                    "role": "user",
                    "content": f"""
                    식당 이름: {restaurant_name} (셰프: {chef_name})
                    장르: {genre}
                    
                    위 식당에 대해 **최소 3개 이상의 서로 다른 최신 네이버 블로그 후기**를 검색해줘.
                    그리고 다음 단계로 분석해:
                    
                    [분석 단계]
                    1. 각 블로그에서 사람들이 '맛있다'고 극찬한 메뉴들을 뽑아.
                    2. 그 중에서 **여러 블로그에서 공통적으로 중복 언급된(교집합)** 메뉴를 찾아.
                    3. 가장 언급 빈도가 높은 **Top 3 시그니처 메뉴**만 선정해.
                    
                    [출력 규칙]
                    - 설명, 미사여구, 번호 매기기 금지.
                    - 오직 메뉴 이름만 쉼표(,)로 구분해서 나열.
                    - (예시: 봉골레 파스타, 트러플 뇨끼, 티라미수)
                    """
                }
            ]
        )
        raw_text = response.choices[0].message.content

        # 님께서 완성하신 정규표현식 청소 로직 그대로 적용
        clean_text = re.sub(r'\[\d+\]', '', raw_text)
        clean_text = re.sub(r'\(\d+\)', '', clean_text)
        clean_text = clean_text.replace('**', '').replace('"', '').replace("'", "")
        clean_text = clean_text.strip()
        
        if clean_text.startswith(", "):
             clean_text = clean_text[2:]

        return clean_text
    except Exception as e:
        return "정보를 찾을 수 없음"

# main.py에 있던 함수 2: GPT 심사평 (워딩 그대로 유지)
def get_gpt_response(user_msg, judge, genre, real_menu, restaurant_name, chef_name, api_key):
    client_ai = OpenAI(api_key=api_key)

    if judge == "백종원":
        system_role = "너는 백종원 대표야. 구수한 말투를 쓰고, 대중적인 맛과 가성비를 중요하게 생각해. '이거 재밌네~', '이거 먹어봐유~', '예술이에유~' 같은 충청도 사투리 감탄사를 섞어줘."
    else:
        system_role = "너는 안성재 심사위원이야. 매우 깐깐하고 논리적이야. 재료의 익힘 정도와 셰프의 의도를 중요하게 생각해. '익힘 정도가 좋아요', '이븐해요', 논리적인 느낌으로 이런 말을 써줘."

    prompt = f"""사용자 상황: {user_msg}
    식당: {restaurant_name} ({genre})
    셰프: {chef_name}
    
    [블로그 분석을 통해 검증된 실제 인기 메뉴]
    {real_menu}
    
    위 정보를 바탕으로 심사평을 남겨줘.
    
    그리고 답변의 맨 마지막 줄에는 위 [실제 인기 메뉴] 중 2개를 골라 아래 형식으로 적어줘.
    (네가 생각하기에 가장 자신 있는 메뉴로 골라줘.)
    
    [답변 형식]
    (심사평 내용)
    
    🍽️ **추천 메뉴:** (메뉴1), (메뉴2)
    """
    
    response = client_ai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_role},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


# ==========================================
# 3. 화면 영역 (app3.py 내용을 그대로 가져옴)
# ==========================================

# 페이지 설정
st.set_page_config(page_title="AI 흑백요리사 맛집", page_icon="👨‍🍳")

st.title("👨‍🍳 AI 흑백요리사 컨설턴트")
st.write("셰프님들의 식당 중 오늘 당신에게 완벽한 한 끼를 골라드려요.")

st.markdown("---")

# Secrets에서 키 가져오기 (배포 환경용)
if "OPENAI_API_KEY" not in st.secrets or "PPLX_API_KEY" not in st.secrets:
    st.error("🚨 API 키가 설정되지 않았습니다! 배포 설정에서 Secrets를 등록해주세요.")
    st.stop()

# DB 연결 대신 setup.py 로직으로 데이터 가져오기
db_restaurants = get_database() # 이제 이게 db.restaurants.find() 역할을 합니다.

# 1. 심사위원 및 장르 선택
judge = st.radio("전담 심사위원 선택", ["안성재", "백종원"], horizontal=True)

# 장르 목록 추출
all_genres = sorted(list(set([item['장르'] for item in db_restaurants])))
genres = ["전체"] + all_genres
selected_genre = st.selectbox("어떤 종류의 음식을 좋아하시나요?", genres, key="random_select")

# 2. 추천 버튼
btn_recommend = st.button("🍴 바로 추천 및 심사평 듣기", type="primary")

if btn_recommend:
    # (1) 식당 랜덤 추출 (MongoDB 쿼리 대체)
    if selected_genre == "전체":
        results = db_restaurants
    else:
        results = [r for r in db_restaurants if r['장르'] == selected_genre]
    
    if results:
        pick = random.choice(results)
        
        # 장르별 이모지 사전
        emoji_map = {
            "한식": "🍚", "중식": "🥟", "일식": "🍣",
            "양식": "🍕", "분식": "🍢", "고기": "🍖",
            "디저트": "🍰", "세계음식": "🌮", "퓨전": "🌀",
        }
        
        # 식당 장르에 맞는 이모지 찾기
        food_emoji = emoji_map.get(pick['장르'], "👨‍🍳")
            
        # 음식 비 내리기
        rain(
            emoji=food_emoji,
            font_size=54,
            falling_speed=5,
            animation_length="1s",
        )
        
        # 🎨 색상 테마 설정
        bg_color = "#2b2b2b"
        border_color = "#555555"
        text_color = "#ffffff"

        # 디자인 박스 HTML 만들기 (님 코드 그대로)
        box_html = f"""
        <div style="
            background-color: {bg_color}; 
            border: 2px solid {border_color}; 
            border-radius: 12px; 
            padding: 25px;
            margin-bottom: 20px;
            color: {text_color};
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        ">
            <h3 style="color: {text_color}; margin-top: 0; border-bottom: 1px solid {border_color}; padding-bottom: 15px;">
                👨‍🍳 오늘의 추천: <span style="font-weight: 900;">{pick['식당명']}</span>
            </h3>
            <p style="font-size: 1.1em; margin-top: 15px; margin-bottom: 0;">
                <span style="color: #aaaaaa;">🧑‍🍳 셰프:</span> {pick['셰프']}   |   
                <span style="color: #aaaaaa;">📂 장르:</span> {pick['장르']}
            </p>
        </div>
        """
        
        st.markdown(box_html, unsafe_allow_html=True)

        if judge == "백종원":
            loading_msg = "🤔 백종원 대표님이 메뉴판을 스캔하는 중입니다..."
        else:
            loading_msg = "🤨 안성재 심사위원이 익힘 정도를 상상하는 중입니다..."

        # (3) ★중요: 즉시 AI 심사평 가져오기★
        with st.spinner(loading_msg):
            try:
                # requests.get(...) 대신 내부 함수를 직접 호출합니다.
                # 1단계: 메뉴 검색
                real_menu = search_menu_with_perplexity(
                    pick['식당명'], 
                    pick['셰프'], 
                    pick['장르'], 
                    st.secrets["PPLX_API_KEY"]
                )
                
                # 2단계: 심사평 생성
                ai_comment = get_gpt_response(
                    user_msg=pick['식당명'], 
                    judge=judge, 
                    genre=pick['장르'], 
                    real_menu=real_menu,
                    restaurant_name=pick['식당명'],
                    chef_name=pick['셰프'],
                    api_key=st.secrets["OPENAI_API_KEY"]
                )
                
                with st.chat_message("assistant", avatar="👨‍🍳"):
                    st.write(f"**[{judge} 심사위원의 분석 결과]**")
                    st.write(ai_comment)

            except Exception as e:
                st.error(f"심사평을 가져오는데 실패했습니다. (오류: {e})")
            
        # (4) 지도 버튼
        map_col1, map_col2 = st.columns(2)
        with map_col1:
            st.link_button("🦁 카카오맵 보기", f"https://map.kakao.com/?q={pick['식당명']}", use_container_width=True)
        with map_col2:
            st.link_button("🌐 구글 지도 검색", f"https://www.google.com/maps/search/{pick['식당명']}", use_container_width=True)

    else:
        st.warning("조건에 맞는 식당이 없습니다!")

st.markdown("---")
st.caption("Developed with FastAPI Logic + Streamlit + OpenAI")
