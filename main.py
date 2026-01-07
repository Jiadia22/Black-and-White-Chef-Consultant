from fastapi import FastAPI
from pymongo import MongoClient
from openai import OpenAI
import random
import re
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
# 말하기 담당
client_ai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 검색 담당
client_pplx = OpenAI(
    api_key=os.getenv("PPLX_API_KEY"), 
    base_url="https://api.perplexity.ai")

db_client = MongoClient('mongodb://localhost:27017/')
db = db_client['chef_db']

def search_menu_with_perplexity(restaurant_name, chef_name, genre):
    """
    Perplexity에게 실시간으로 식당 메뉴를 검색해오라고 시키는 함수
    """
    print(f"🔎 Perplexity가 '{restaurant_name}' 메뉴를 검색 중입니다...")
    try:
        response = client_pplx.chat.completions.create(
            model="sonar-pro", # 검색 특화 모델 (sonar 또는 sonar-pro)
            messages=[
                {
                    "role": "system",
                    "content": "너는 여러 개의 정보를 취합하여 공통점을 찾아내는 데이터 분석가야."},
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
                    - (예시: 봉골레 파스타, 트러플 뇨끼, 티라미수)"""
                }
            ]
        )
        raw_text = response.choices[0].message.content

        # 1. [1], [12] 같은 대괄호 숫자 제거
        clean_text = re.sub(r'\[\d+\]', '', raw_text)
        
        # 2. (1), (2) 같은 소괄호 숫자 제거
        clean_text = re.sub(r'\(\d+\)', '', clean_text)
        
        # 3. 특수문자 제거 (별표, 따옴표 등) - 한글은 절대 안 건드림!
        clean_text = clean_text.replace('**', '').replace('"', '').replace("'", "")
        
        # 4. 혹시 모를 앞뒤 공백만 살짝 다듬기 (글자 자르기 금지)
        clean_text = clean_text.strip()
        
        # 5. (안전장치) 만약 결과가 ', ' 로 시작하면 앞부분 제거
        if clean_text.startswith(", "):
             clean_text = clean_text[2:]

        print(f"✅ [검색 결과] {clean_text}")
        return clean_text
    except Exception as e:
        print(f"🚨 검색 실패: {e}")
        return "정보를 찾을 수 없음"

@app.get("/ai-recommend")
def get_ai_recommend(user_msg: str, judge: str, genre: str = "전체"):
    
    pick = db.restaurants.find_one({"식당명": user_msg})

    if not pick:
        return {"result": "식당 정보가 없습니다."}
    
    # 실시간 메뉴 검색 시키기
    real_menu = search_menu_with_perplexity(pick['식당명'], pick['셰프'], pick['장르'])
    print(f"✅ 검색된 메뉴: {real_menu}") # 터미널에서 확인용

    # 심사위원별 맞춤 지시사항(프롬프트) 설정
    if judge == "백종원":
        system_role = "너는 백종원 대표야. 구수한 말투를 쓰고, 대중적인 맛과 가성비를 중요하게 생각해. '이거 재밌네~', '이거 먹어봐유~', '예술이에유~' 같은 충청도 사투리 감탄사를 섞어줘."
    else:
        system_role = "너는 안성재 심사위원이야. 매우 깐깐하고 논리적이야. 재료의 익힘 정도와 셰프의 의도를 중요하게 생각해. '익힘 정도가 좋아요', '이븐해요', 논리적인 느낌으로 이런 말을 써줘."

    prompt = f"""사용자 상황: {user_msg}
    식당: {pick['식당명']} ({pick['장르']})
    셰프: {pick['셰프']}
    
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


    return {
        "restaurant": pick['식당명'],
        "chef": pick['셰프'],
        "ai_comment": response.choices[0].message.content,
        "judge_name": judge
    }

