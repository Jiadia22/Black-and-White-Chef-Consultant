from pymongo import MongoClient

def setup_db():
    # 1. 텍스트 파일 읽기
    try:
        with open('restaurants.txt', 'r', encoding='utf-8') as f:
            raw_data = f.read()
    except FileNotFoundError:
        print("🚨 'restaurants.txt' 파일을 찾을 수 없습니다!")
        return
    
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
