import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 설정
st.set_page_config(page_title="식단 영양 시뮬레이터", layout="wide")
st.title("🥩 실시간 식단 영양 대시보드")

# 2. 확장된 음식 데이터베이스 (100g 기준 일반적 수치)
food_db = {
    "소고기(등심)": {"kcal": 250, "carbs": 0, "protein": 26, "fat": 15},
    "닭가슴살": {"kcal": 165, "carbs": 0, "protein": 31, "fat": 3.6},
    "달걀": {"kcal": 155, "carbs": 1.1, "protein": 13, "fat": 11},
    "브로콜리": {"kcal": 34, "carbs": 7, "protein": 2.8, "fat": 0.4},
    # 추가된 음식들
    "김치": {"kcal": 18, "carbs": 3.4, "protein": 1.3, "fat": 0.2},
    "된장국": {"kcal": 40, "carbs": 4.5, "protein": 3.5, "fat": 0.8},
    "김치찌개": {"kcal": 65, "carbs": 4.2, "protein": 4.5, "fat": 3.8},
    "마라탕": {"kcal": 150, "carbs": 12, "protein": 7, "fat": 10},
    "짜장면": {"kcal": 145, "carbs": 21, "protein": 5, "fat": 4.5},
    "냉면": {"kcal": 115, "carbs": 25, "protein": 3.5, "fat": 0.5},
    "우유": {"kcal": 65, "carbs": 4.8, "protein": 3.2, "fat": 3.6},
    "카페라떼": {"kcal": 45, "carbs": 4.2, "protein": 2.8, "fat": 2.4}
}

# 3. 사이드바: 목표 설정
st.sidebar.header("🎯 오늘의 목표")
target_carbs = st.sidebar.number_input("탄수화물 제한 (g)", value=160)
target_kcal = st.sidebar.number_input("목표 칼로리 (kcal)", value=2000)

# 4. 메인 화면: 음식 입력부
st.subheader("🍽 오늘의 식단 입력")
selected_foods = st.multiselect("먹은 음식을 선택하세요", options=list(food_db.keys()))

total_stats = {"kcal": 0, "carbs": 0, "protein": 0, "fat": 0}

if selected_foods:
    # 입력 편의를 위해 컬럼 나누기
    input_cols = st.columns(min(len(selected_foods), 4)) 
    for i, food in enumerate(selected_foods):
        with input_cols[i % 4]:
            weight = st.number_input(f"{food} (g)", min_value=0, value=150, step=50, key=food)
            ratio = weight / 100
            total_stats["kcal"] += food_db[food]["kcal"] * ratio
            total_stats["carbs"] += food_db[food]["carbs"] * ratio
            total_stats["protein"] += food_db[food]["protein"] * ratio
            total_stats["fat"] += food_db[food]["fat"] * ratio

    st.divider()

    # 5. 결과 시각화 (Metrics)
    st.subheader("📊 현재 섭취 현황")
    m1, m2, m3, m4 = st.columns(4)
    
    # 탄수화물/칼로리는 초과 시 빨간색 표시를 위해 delta 설정
    kcal_diff = total_stats['kcal'] - target_kcal
    carb_diff = total_stats['carbs'] - target_carbs
    
    m1.metric("총 칼로리", f"{total_stats['kcal']:.1f} kcal", f"{kcal_diff:.1f} kcal", delta_color="inverse")
    m2.metric("탄수화물", f"{total_stats['carbs']:.1f} g", f"{carb_diff:.1f} g", delta_color="inverse")
    m3.metric("단백질", f"{total_stats['protein']:.1f} g")
    m4.metric("지방", f"{total_stats['fat']:.1f} g")

    # 6. 경고 알림 및 피드백
    if total_stats["carbs"] > target_carbs:
        st.error(f"⚠️ 탄수화물 섭취량이 목표({target_carbs}g)를 초과했습니다!")
    elif total_stats["carbs"] > target_carbs * 0.8:
        st.warning("💡 탄수화물 섭취가 한계치에 가까워요. 주의가 필요합니다.")
    else:
        st.success("✅ 탄수화물 섭취량이 안정권입니다.")

    # 7. 차트 시각화
    chart_data = pd.DataFrame({
        "영양소": ["탄수화물", "단백질", "지방"],
        "섭취량(g)": [total_stats["carbs"], total_stats["protein"], total_stats["fat"]]
    })

    fig = px.pie(chart_data, values="섭취량(g)", names="영양소", 
                 title="오늘의 탄/단/지 구성 비율", 
                 hole=0.4,
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("위에서 음식을 선택하면 대시보드가 활성화됩니다.")
