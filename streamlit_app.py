import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 설정 및 제목
st.set_page_config(page_title="식단 영양 시뮬레이터", layout="wide")
st.title("🥩 영양 성분 실시간 대시보드")

# 2. 간단한 음식 데이터베이스 (실제로는 CSV나 DB에서 불러오기 권장)
food_db = {
    "소고기(등심)": {"kcal": 250, "carbs": 0, "protein": 26, "fat": 15},
    "닭가슴살": {"kcal": 165, "carbs": 0, "protein": 31, "fat": 3.6},
    "쌀밥": {"kcal": 130, "carbs": 28, "protein": 2.7, "fat": 0.3},
    "달걀": {"kcal": 155, "carbs": 1.1, "protein": 13, "fat": 11},
    "브로콜리": {"kcal": 34, "carbs": 7, "protein": 2.8, "fat": 0.4}
}

# 3. 사이드바: 목표 설정
st.sidebar.header("🎯 오늘의 목표")
target_carbs = st.sidebar.number_input("탄수화물 제한 (g)", value=160)
target_kcal = st.sidebar.number_input("목표 칼로리 (kcal)", value=2000)

# 4. 메인 화면: 음식 입력부
st.subheader("🍽 무엇을 드셨나요?")
selected_foods = st.multiselect("음식을 선택하세요", options=list(food_db.keys()))

total_stats = {"kcal": 0, "carbs": 0, "protein": 0, "fat": 0}

cols = st.columns(len(selected_foods) if selected_foods else 1)
for i, food in enumerate(selected_foods):
    with cols[i]:
        weight = st.number_input(f"{food} 중량(g)", min_value=0, value=100, step=10)
        # 비율 계산
        ratio = weight / 100
        total_stats["kcal"] += food_db[food]["kcal"] * ratio
        total_stats["carbs"] += food_db[food]["carbs"] * ratio
        total_stats["protein"] += food_db[food]["protein"] * ratio
        total_stats["fat"] += food_db[food]["fat"] * ratio

st.divider()

# 5. 결과 시각화 (Metrics)
st.subheader("📊 현재 섭취 현황")
m1, m2, m3, m4 = st.columns(4)
m1.metric("총 칼로리", f"{total_stats['kcal']:.1f} kcal", f"{total_stats['kcal'] - target_kcal:.1f} kcal", delta_color="inverse")
m2.metric("탄수화물", f"{total_stats['carbs']:.1f} g", f"{total_stats['carbs'] - target_carbs:.1f} g", delta_color="inverse")
m3.metric("단백질", f"{total_stats['protein']:.1f} g")
m4.metric("지방", f"{total_stats['fat']:.1f} g")

# 6. 경고 알림 (Logic)
if total_stats["carbs"] > target_carbs:
    st.warning(f"⚠️ 탄수화물 섭취량이 설정값({target_carbs}g)을 초과했습니다!")
elif total_stats["carbs"] > target_carbs * 0.8:
    st.info("💡 탄수화물 섭취가 목표치에 가까워지고 있어요.")

# 7. 차트 시각화
chart_data = pd.DataFrame({
    "영양소": ["탄수화물", "단백질", "지방"],
    "섭취량(g)": [total_stats["carbs"], total_stats["protein"], total_stats["fat"]]
})

fig = px.pie(chart_data, values="섭취량(g)", names="영양소", title="오늘의 탄/단/지 비율", hole=0.4)
st.plotly_chart(fig, use_container_width=True)
