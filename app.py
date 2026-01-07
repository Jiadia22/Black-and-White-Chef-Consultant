import streamlit as st
from pymongo import MongoClient
import random
import requests
from streamlit_extras.let_it_rain import rain

from styles import get_restaurant_box_html

# 페이지 설정
st.set_page_config(page_title="AI 흑백요리사 맛집", page_icon="👨‍🍳")

# DB 연결
client = MongoClient('mongodb://localhost:27017/')
db = client['chef_db']

st.title("👨‍🍳 AI 흑백요리사 컨설턴트")
st.write("셰프님들의 식당 중 오늘 당신에게 완벽한 한 끼를 골라드려요.")

st.markdown("---")

# 1. 심사위원 및 장르 선택
judge = st.radio("전담 심사위원 선택", ["안성재", "백종원"], horizontal=True)
genres = ["전체"] + list(db.restaurants.distinct("장르"))
selected_genre = st.selectbox("어떤 종류의 음식을 좋아하시나요?", genres, key="random_select")

# 2. 추천 버튼
btn_recommend = st.button("🍴 바로 추천 및 심사평 듣기", type="primary")

if btn_recommend:
    # (1) 식당 랜덤 추출
    query = {}
    if selected_genre != "전체":
        query["장르"] = selected_genre
    
    results = list(db.restaurants.find(query))
    
    if results:
        pick = random.choice(results)
        # 장르별 이모지 사전 (여기서 이모지를 마음대로 바꿀 수 있어요!)
        emoji_map = {
            "한식": "🍚",
            "중식": "🥟",
            "일식": "🍣",
            "양식": "🍕",
            "분식": "🍢",
            "고기": "🍖",
            "디저트": "🍰",
            "세계음식": "🌮",
            "퓨전": "🌀",
        }
        
        # 식당 장르에 맞는 이모지 찾기 (없으면 기본값 👨‍🍳)
        food_emoji = emoji_map.get(pick['장르'], "👨‍🍳")
            
        # 음식 비 내리기
        rain(
            emoji=food_emoji,
            font_size=54,
            falling_speed=5,
            animation_length="1s",
        )

                
        # 함수를 불러서 HTML 완성! (괄호 안에 pick 데이터를 쏙 넣어줍니다)
        box_html = get_restaurant_box_html(pick['식당명'], pick['셰프'], pick['장르'])
        
        st.markdown(box_html, unsafe_allow_html=True)
       
   

        if judge == "백종원":
            loading_msg = "🤔 백종원 대표님이 메뉴판을 스캔하는 중입니다..."
        else:
            loading_msg = "🤨 안성재 심사위원이 익힘 정도를 상상하는 중입니다..."

        # (3) ★중요: 즉시 AI 심사평 가져오기★
        with st.spinner(loading_msg):
            try:
                # FastAPI 서버로 요청 (식당 이름과 심사위원을 전달)
                # 팁: FastAPI 쪽에 해당 식당에 대한 멘트를 요청하는 파라미터를 맞춰야 합니다.
                res = requests.get(f"http://127.0.0.1:8000/ai-recommend?user_msg={pick['식당명']}&judge={judge}&genre={pick['장르']}")
                data = res.json()
                
                with st.chat_message("assistant", avatar="👨‍🍳"):
                    st.write(f"**[{judge} 심사위원의 분석 결과]**")
                    # FastAPI에서 넘겨주는 키값(예: 'comment')에 맞춰 출력
                    st.write(data.get('ai_comment', data.get('description', "맛 평가를 불러올 수 없습니다.")))
            except Exception as e:
                st.error(f"심사평을 가져오는데 실패했습니다. FastAPI 서버를 확인해주세요! (오류: {e})")
            
        # (4) 지도 버튼
        map_col1, map_col2 = st.columns(2)
        with map_col1:
            st.link_button("🦁 카카오맵 보기", f"https://map.kakao.com/?q={pick['식당명']}", use_container_width=True)
        with map_col2:
            st.link_button("🌐 구글 지도 검색", f"https://www.google.com/maps/search/{pick['식당명']}", use_container_width=True)

    else:
        st.warning("조건에 맞는 식당이 없습니다!")

st.markdown("---")
st.caption("Developed with FastAPI + MongoDB + Streamlit + OpenAI + Perplexity AI")
