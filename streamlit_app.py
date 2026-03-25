import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 설정
st.set_page_config(page_title="식단 영양 시뮬레이터", layout="wide")
st.title("🥩 실시간 식단 영양 대시보드")

# 2. 보편적인 1회 제공량 기준 데이터베이스 (최종본)
food_db = {
    "에그 맥머핀(1개)": {"kcal": 303, "carbs": 28, "protein": 17, "fat": 13},
    "해쉬 브라운(1개)": {"kcal": 159, "carbs": 15, "protein": 1, "fat": 10},
    "일반 콜라(355ml)": {"kcal": 150, "carbs": 38, "protein": 0, "fat": 0},
    "제로 콜라(355ml)": {"kcal": 0, "carbs": 0, "protein": 0, "fat": 0},
    "소고기(등심) 200g": {"kcal": 500, "carbs": 0, "protein": 52, "fat": 30},
    "닭가슴살 100g": {"kcal": 165, "carbs": 0, "protein": 31, "fat": 3.6},
    "달걀(2개)": {"kcal": 155, "carbs": 1.1, "protein": 13, "fat": 11},
    "김치찌개(1인분)": {"kcal": 250, "carbs": 15, "protein": 18, "fat": 15},
    "된장국(1인분)": {"kcal": 120, "carbs": 14, "protein": 10, "fat": 3},
    "마라탕(1인분)": {"kcal": 800, "carbs": 60, "protein": 35, "fat": 50},
    "짜장면(1인분)": {"kcal": 800, "carbs": 120, "protein": 25, "fat": 25},
    "냉면(1인분)": {"kcal": 500, "carbs": 110, "protein": 15, "fat": 2},
    "김치(작은접시)": {"kcal": 25, "carbs": 5, "protein": 1.5, "fat": 0.2},
    "우유(200ml)": {"kcal": 130, "carbs": 10, "protein": 6, "fat": 7},
    "카페라떼(1잔)": {"kcal": 180, "carbs": 15, "protein": 10, "fat": 9},
    "브로콜리(100g)": {"kcal": 34, "carbs": 7, "protein": 2.8, "fat": 0.4}
}

# 3. 사이드바: 목표 설정
st.sidebar.header("🎯 오늘의 목표")
target_carbs = st.sidebar.number_input("탄수화물 제한 (g)", value=160)
target_kcal = st.sidebar.number_input("목표 칼로리 (kcal)", value=2000)

# 4. 메인 화면: 음식 입력부
st.subheader("🍽 오늘 무엇을 드셨나요?")
selected_foods = st.multiselect("음식을 선택하면 즉시 계산됩니다", options=list(food_db.keys()))

total_stats = {"kcal": 0, "carbs": 0, "protein": 0, "fat": 0}

if selected_foods:
    cols = st.columns(len(selected_foods))
    for i, food in enumerate(selected_foods):
        with cols[i]:
            count = st.number_input(f"{food} (수량)", min_value=0.0, value=1.0, step=0.5, key=f"input_{food}")
            
            total_stats["kcal"] += food_db[food]["kcal"] * count
            total_stats["carbs"] += food_db[food]["carbs"] * count
            total_stats["protein"] += food_db[food]["protein"] * count
            total_stats["fat"] += food_db[food]["fat"] * count

    st.divider()

    # 5. 결과 시각화 (Metrics)
    st.subheader("📊 실시간 섭취 현황")
    m1, m2, m3, m4 = st.columns(4)
    
    kcal_diff = total_stats['kcal'] - target_kcal
    carb_diff = total_stats['carbs'] - target_carbs
    
    m1.metric("총 칼로리", f"{total_stats['kcal']:.0f} kcal", f"{kcal_diff:.0f} kcal", delta_color="inverse")
    m2.metric("탄수화물", f"{total_stats['carbs']:.1f} g", f"{carb_diff:.1f} g", delta_color="inverse")
    m3.metric("단백질", f"{total_stats['protein']:.1f} g")
    m4.metric("지방", f"{total_stats['fat']:.1f} g")

    # 6. 알림 메시지 로직
    if total_stats["carbs"] > target_carbs:
        st.error(f"⚠️ 탄수화물 섭취량이 제한치({target_carbs}g)를 넘었습니다!")
    elif total_stats["carbs"] > target_carbs * 0.8:
        st.warning("💡 탄수화물이 거의 찼습니다. 남은 식사는 육류나 채소 위주를 권장합니다.")
    else:
        st.success("✅ 탄수화물 관리가 아주 잘 되고 있습니다!")

    # 7. 차트 시각화
    chart_df = pd.DataFrame({
        "영양소": ["탄수화물", "단백질", "지방"],
        "섭취량(g)": [total_stats["carbs"], total_stats["protein"], total_stats["fat"]]
    })
    
    # 0g인 영양소는 차트에서 제외하여 깔끔하게 표시
    chart_df = chart_df[chart_df["섭취량(g)"] > 0]
    
    if not chart_df.empty:
        fig = px.pie(chart_df, values="섭취량(g)", names="영양소", hole=0.4, title="오늘의 영양 균형")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("섭취한 영양소가 없습니다.")

else:
    st.info("음식을 선택해 주세요. 선택 즉시 데이터가 업데이트됩니다.")
