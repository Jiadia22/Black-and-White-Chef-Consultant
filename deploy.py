import streamlit as st
from openai import OpenAI
import random
import re
from streamlit_extras.let_it_rain import rain

# ==========================================
# 1. 데이터 영역 (DB 대신 여기에 데이터를 직접 넣습니다)
# ==========================================
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

def get_restaurant_list():
    lines = raw_data.strip().split('\n')
    final_data = []
    current_genre = ""
    for line in lines:
        line = line.strip()
        if not line: continue
        if line.startswith('<') and line.endswith('>'):
            current_genre = line[1:-1]
        elif ' - ' in line:
            chef, restaurants = line.split(' - ')
            res_list = re.split(',|/', restaurants)
            for res in res_list:
                res_name = res.strip()
                if "미공개" not in res_name and "명인" not in res_name:
                    final_data.append({"장르": current_genre, "셰프": chef.strip(), "식당명": res_name})
    return final_data

# ==========================================
# 2. 로직 영역 (검색 및 AI 기능)
# ==========================================
def search_menu_with_perplexity(restaurant_name, chef_name, genre, api_key):
    try:
        client_pplx = OpenAI(api_key=api_key, base_url="https://api.perplexity.ai")
        response = client_pplx.chat.completions.create(
            model="sonar-pro",
            messages=[
                {"role": "system", "content": "너는 여러 개의 정보를 취합하여 공통점을 찾아내는 데이터 분석가야."},
                {"role": "user", "content": f"""
                식당 이름: {restaurant_name} (셰프: {chef_name})
                장르: {genre}
                
                위 식당에 대해 **최소 3개 이상의 서로 다른 최신 네이버 블로그 후기**를 검색해줘.
                
                [분석 단계]
                1. 각 블로그에서 사람들이 '맛있다'고 극찬한 메뉴들을 뽑아.
                2. 그 중에서 **여러 블로그에서 공통적으로 중복 언급된(교집합)** 메뉴를 찾아.
                3. 가장 언급 빈도가 높은 **Top 3 시그니처 메뉴**만 선정해.
                
                [출력 규칙]
                - 설명, 미사여구, 번호 매기기 금지.
                - 오직 메뉴 이름만 쉼표(,)로 구분해서 나열.
                """}
            ]
        )
        raw_text = response.choices[0].message.content
        clean_text = re.sub(r'\[\d+\]', '', raw_text)
        clean_text = re.sub(r'\(\d+\)', '', clean_text)
        clean_text = clean_text.replace('**', '').replace('"', '').replace("'", "").strip()
        if clean_text.startswith(", "): clean_text = clean_text[2:]
        return clean_text
    except Exception as e:
        return "정보를 찾을 수 없음"

def get_ai_comment(restaurant, chef, genre, menu, judge, api_key):
    client_gpt = OpenAI(api_key=api_key)
    if judge == "백종원":
        system_role = "너는 백종원 대표야. 구수한 말투(~했쥬)를 쓰고, 가성비와 대중성을 중요하게 생각해."
    else:
        system_role = "너는 안성재 심사위원이야. 깐깐하고 논리적이며 재료의 익힘과 셰프의 의도를 중요하게 생각해."

    prompt = f"""
    식당: {restaurant} ({genre}) / 셰프: {chef}
    실제 인기 메뉴: {menu}
    
    위 정보를 바탕으로 심사평을 남겨줘.
    마지막 줄에는 위 메뉴 중 2개를 골라 '🍽️ **추천 메뉴:** (메뉴1), (메뉴2)' 형식으로 적어줘.
    """
    
    response = client_gpt.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_role},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# ==========================================
# 3. 화면 영역 (Streamlit UI)
# ==========================================
st.set_page_config(page_title="AI 흑백요리사 맛집", page_icon="👨‍🍳")

st.title("👨‍🍳 AI 흑백요리사 컨설턴트")
st.write("셰프님들의 식당 중 오늘 당신에게 완벽한 한 끼를 골라드려요.")
st.markdown("---")

# API 키 확인 (Streamlit Secrets에서 가져옵니다)
if "OPENAI_API_KEY" not in st.secrets or "PPLX_API_KEY" not in st.secrets:
    st.error("🚨 API 키가 설정되지 않았습니다! 배포 설정에서 Secrets를 등록해주세요.")
    st.stop()

# 데이터 로드
restaurant_data = get_restaurant_list()
genres = ["전체"] + sorted(list(set([r["장르"] for r in restaurant_data])))

# 선택 UI
judge = st.radio("전담 심사위원 선택", ["안성재", "백종원"], horizontal=True)
selected_genre = st.selectbox("어떤 종류의 음식을 좋아하시나요?", genres)
btn_recommend = st.button("🍴 바로 추천 및 심사평 듣기", type="primary")

if btn_recommend:
    # 필터링 및 랜덤 추출
    filtered = [r for r in restaurant_data if selected_genre == "전체" or r["장르"] == selected_genre]
    
    if filtered:
        pick = random.choice(filtered)
        
        # 이모지 비 내리기
        emoji_map = {"한식": "🍚", "중식": "🥟", "일식": "🍣", "양식": "🍕", "분식": "🍢", "고기": "🍖", "디저트": "🍰", "세계음식": "🌮", "퓨전": "🌀"}
        rain(emoji=emoji_map.get(pick['장르'], "👨‍🍳"), font_size=54, falling_speed=5, animation_length="1s")
        
        # 결과 박스 표시
        st.markdown(f"""
        <div style="background-color: #2b2b2b; border: 2px solid #555; border-radius: 12px; padding: 25px; margin-bottom: 20px; color: #fff;">
            <h3 style="color: #fff; margin:0; border-bottom: 1px solid #555; padding-bottom: 15px;">
                👨‍🍳 오늘의 추천: <span style="font-weight: 900;">{pick['식당명']}</span>
            </h3>
            <p style="font-size: 1.1em; margin-top: 15px;">
                <span style="color: #aaa;">🧑‍🍳 셰프:</span> {pick['셰프']}  |  <span style="color: #aaa;">📂 장르:</span> {pick['장르']}
            </p>
        </div>
        """, unsafe_allow_html=True)

        # AI 로직 실행
        msg = "🤔 백종원 대표님이 스캔 중..." if judge == "백종원" else "🤨 안성재 위원이 익힘을 확인 중..."
        with st.spinner(msg):
            real_menu = search_menu_with_perplexity(pick['식당명'], pick['셰프'], pick['장르'], st.secrets["PPLX_API_KEY"])
            comment = get_ai_comment(pick['식당명'], pick['셰프'], pick['장르'], real_menu, judge, st.secrets["OPENAI_API_KEY"])
            
            with st.chat_message("assistant", avatar="👨‍🍳"):
                st.write(f"**[{judge} 심사위원의 분석 결과]**")
                st.write(comment)
        
        # 지도 버튼
        col1, col2 = st.columns(2)
        col1.link_button("🦁 카카오맵 보기", f"https://map.kakao.com/?q={pick['식당명']}", use_container_width=True)
        col2.link_button("🌐 구글 지도 검색", f"https://www.google.com/maps/search/{pick['식당명']}", use_container_width=True)
    else:
        st.warning("조건에 맞는 식당이 없습니다!")