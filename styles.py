# 🎨 색상 테마 설정 (모던 다크)
bg_color = "#2b2b2b"      # 어두운 회색 배경
border_color = "#555555"  # 차분한 회색 테두리
text_color = "#ffffff"    # 흰색 글자

def get_restaurant_box_html(restaurant_name, chef_name, genre):
    """추천 식당을 보여주는 HTML 박스 템플릿"""
    return f"""
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
            👨‍🍳 오늘의 추천: <span style="font-weight: 900;">{restaurant_name}</span>
        </h3>
        <p style="font-size: 1.1em; margin-top: 15px; margin-bottom: 0;">
            <span style="color: #aaaaaa;">🧑‍🍳 셰프:</span> {chef_name}   |   
            <span style="color: #aaaaaa;">📂 장르:</span> {genre}
        </p>
    </div>
    """