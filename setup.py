from pymongo import MongoClient

# 1. 새로 가공하신 데이터를 여기에 붙여넣으세요.
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

def setup_db():
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
            
            # 쉼표나 슬래시(/)가 섞여 있어도 분리할 수 있게 처리
            import re
            res_list = re.split(',|/', restaurants)
            
            for res in res_list:
                res_name = res.strip()
                # '미공개', '명인' 키워드가 들어간 행은 저장하지 않음 (정제)
                if "미공개" not in res_name and "명인" not in res_name:
                    final_data.append({
                        "장르": current_genre,
                        "셰프": chef.strip(),
                        "식당명": res_name
                    })

    # MongoDB 저장
    client = MongoClient('mongodb://localhost:27017/')
    db = client['chef_db']
    db.restaurants.drop()  # 깔끔하게 새로 시작
    db.restaurants.insert_many(final_data)
    print(f"🎉 가공 완료! 총 {len(final_data)}개의 진짜 맛집을 DB에 넣었습니다.")

if __name__ == "__main__":
    setup_db()