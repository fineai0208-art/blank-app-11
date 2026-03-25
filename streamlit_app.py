import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. 페이지 설정
st.set_page_config(page_title="식단 영양 시뮬레이터", layout="wide")
st.title("🥩 실시간 식단 영양 대시보드")

# 2. 카테고리별 음식 데이터베이스
food_db_by_category = {
    "🍚 한식": {
        "쌀밥(1공기)": {"kcal": 310, "carbs": 68, "protein": 5, "fat": 0.5},
        "김치찌개(1인분)": {"kcal": 250, "carbs": 15, "protein": 18, "fat": 15},
        "된장국(1인분)": {"kcal": 120, "carbs": 14, "protein": 10, "fat": 3},
        "불고기(1인분)": {"kcal": 380, "carbs": 18, "protein": 30, "fat": 20},
        "비빔밥(1인분)": {"kcal": 550, "carbs": 90, "protein": 20, "fat": 12},
        "삼겹살(200g)": {"kcal": 700, "carbs": 0, "protein": 38, "fat": 60},
        "냉면(1인분)": {"kcal": 500, "carbs": 110, "protein": 15, "fat": 2},
        "김치(작은접시)": {"kcal": 25, "carbs": 5, "protein": 1.5, "fat": 0.2},
        "잡채(1인분)": {"kcal": 320, "carbs": 55, "protein": 10, "fat": 8},
        "순두부찌개(1인분)": {"kcal": 200, "carbs": 8, "protein": 15, "fat": 12},
    },
    "🍜 중식 / 분식": {
        "짜장면(1인분)": {"kcal": 800, "carbs": 120, "protein": 25, "fat": 25},
        "짬뽕(1인분)": {"kcal": 650, "carbs": 85, "protein": 30, "fat": 18},
        "마라탕(1인분)": {"kcal": 800, "carbs": 60, "protein": 35, "fat": 50},
        "쌀국수(1인분)": {"kcal": 500, "carbs": 95, "protein": 25, "fat": 2},
        "떡볶이(1인분)": {"kcal": 380, "carbs": 75, "protein": 8, "fat": 5},
        "순대(1인분)": {"kcal": 300, "carbs": 30, "protein": 14, "fat": 14},
        "라면(1개)": {"kcal": 500, "carbs": 75, "protein": 10, "fat": 16},
        "김밥(1줄)": {"kcal": 400, "carbs": 70, "protein": 12, "fat": 8},
        "삼각김밥(1개)": {"kcal": 180, "carbs": 35, "protein": 4, "fat": 2.5},
    },
    "🍔 패스트푸드": {
        "빅맥(1개)": {"kcal": 550, "carbs": 45, "protein": 25, "fat": 30},
        "에그 맥머핀(1개)": {"kcal": 303, "carbs": 28, "protein": 17, "fat": 13},
        "해쉬 브라운(1개)": {"kcal": 159, "carbs": 15, "protein": 1, "fat": 10},
        "감자튀김(M)": {"kcal": 330, "carbs": 40, "protein": 3, "fat": 17},
        "피자(1조각)": {"kcal": 280, "carbs": 30, "protein": 12, "fat": 12},
        "치킨버거(1개)": {"kcal": 480, "carbs": 42, "protein": 22, "fat": 24},
        "핫도그(1개)": {"kcal": 290, "carbs": 25, "protein": 11, "fat": 16},
        "일반 콜라(355ml)": {"kcal": 150, "carbs": 38, "protein": 0, "fat": 0},
        "제로 콜라(355ml)": {"kcal": 0, "carbs": 0, "protein": 0, "fat": 0},
    },
    "🥩 고단백 식품": {
        "닭가슴살 100g": {"kcal": 165, "carbs": 0, "protein": 31, "fat": 3.6},
        "소고기(등심) 200g": {"kcal": 500, "carbs": 0, "protein": 52, "fat": 30},
        "연어(100g)": {"kcal": 208, "carbs": 0, "protein": 20, "fat": 13},
        "참치캔(1개/100g)": {"kcal": 130, "carbs": 0, "protein": 28, "fat": 1},
        "달걀(2개)": {"kcal": 155, "carbs": 1.1, "protein": 13, "fat": 11},
        "두부(100g)": {"kcal": 76, "carbs": 2, "protein": 8, "fat": 4},
        "그릭요거트(1팩/150g)": {"kcal": 130, "carbs": 8, "protein": 15, "fat": 4},
        "프로틴바(1개)": {"kcal": 200, "carbs": 20, "protein": 20, "fat": 7},
    },
    "🥗 채소 / 건강식": {
        "브로콜리(100g)": {"kcal": 34, "carbs": 7, "protein": 2.8, "fat": 0.4},
        "샐러드(1인분)": {"kcal": 80, "carbs": 10, "protein": 3, "fat": 3},
        "고구마(1개/150g)": {"kcal": 130, "carbs": 30, "protein": 2, "fat": 0.1},
        "바나나(1개)": {"kcal": 105, "carbs": 27, "protein": 1.3, "fat": 0.4},
        "사과(1개)": {"kcal": 95, "carbs": 25, "protein": 0.5, "fat": 0.3},
        "아보카도(1/2개)": {"kcal": 160, "carbs": 9, "protein": 2, "fat": 15},
        "견과류(한줌/30g)": {"kcal": 180, "carbs": 6, "protein": 5, "fat": 16},
        "오트밀(1인분/40g)": {"kcal": 150, "carbs": 27, "protein": 5, "fat": 3},
    },
    "☕ 음료 / 카페": {
        "아이스 아메리카노(1잔)": {"kcal": 10, "carbs": 1, "protein": 0.5, "fat": 0},
        "카페라떼(1잔)": {"kcal": 180, "carbs": 15, "protein": 10, "fat": 9},
        "아이스 바닐라 라떼(1잔)": {"kcal": 220, "carbs": 30, "protein": 7, "fat": 8},
        "초코 프라푸치노(1잔)": {"kcal": 420, "carbs": 65, "protein": 6, "fat": 14},
        "우유(200ml)": {"kcal": 130, "carbs": 10, "protein": 6, "fat": 7},
        "두유(200ml)": {"kcal": 90, "carbs": 8, "protein": 5, "fat": 4},
        "오렌지주스(200ml)": {"kcal": 90, "carbs": 21, "protein": 1, "fat": 0},
        "요거트(1팩/100g)": {"kcal": 90, "carbs": 12, "protein": 3.5, "fat": 3},
        "에너지드링크(1캔)": {"kcal": 110, "carbs": 27, "protein": 1, "fat": 0},
    },
    "🍰 간식 / 디저트": {
        "초콜릿(30g)": {"kcal": 160, "carbs": 18, "protein": 2, "fat": 9},
        "감자칩(1봉/50g)": {"kcal": 270, "carbs": 28, "protein": 3, "fat": 17},
        "빵(식빵 2쪽)": {"kcal": 160, "carbs": 30, "protein": 5, "fat": 2},
        "크로아상(1개)": {"kcal": 280, "carbs": 30, "protein": 5, "fat": 16},
        "아이스크림(1스쿱)": {"kcal": 140, "carbs": 17, "protein": 2, "fat": 7},
        "케이크(1조각)": {"kcal": 350, "carbs": 45, "protein": 5, "fat": 18},
        "떡(100g)": {"kcal": 220, "carbs": 50, "protein": 3, "fat": 0.5},
        "팝콘(1봉/50g)": {"kcal": 200, "carbs": 22, "protein": 3, "fat": 11},
    },
}

# 전체 flat db (계산용)
food_db = {}
for cat_foods in food_db_by_category.values():
    food_db.update(cat_foods)

# 3. 사이드바: 목표 설정
st.sidebar.header("🎯 오늘의 목표")
gender = st.sidebar.radio("성별", ["남성", "여성"])
activity = st.sidebar.selectbox("활동량", ["비활동적", "보통", "활동적", "매우 활동적"])

default_kcal = {"비활동적": 1800, "보통": 2000, "활동적": 2400, "매우 활동적": 2800}
default_kcal_f = {"비활동적": 1500, "보통": 1700, "활동적": 2000, "매우 활동적": 2400}
rec_kcal = default_kcal[activity] if gender == "남성" else default_kcal_f[activity]

target_kcal   = st.sidebar.number_input("목표 칼로리 (kcal)", value=rec_kcal)
target_carbs  = st.sidebar.number_input("탄수화물 목표 (g)", value=int(target_kcal * 0.5 / 4))
target_protein = st.sidebar.number_input("단백질 목표 (g)", value=int(target_kcal * 0.2 / 4))
target_fat    = st.sidebar.number_input("지방 목표 (g)", value=int(target_kcal * 0.3 / 9))

st.sidebar.markdown("---")
st.sidebar.caption(f"💡 권장 칼로리: {rec_kcal} kcal")

# 4. 카테고리 탭으로 음식 선택
st.subheader("🍽 오늘 무엇을 드셨나요?")

if "selected_foods" not in st.session_state:
    st.session_state.selected_foods = []

tabs = st.tabs(list(food_db_by_category.keys()))
for tab, (cat_name, cat_foods) in zip(tabs, food_db_by_category.items()):
    with tab:
        cols = st.columns(4)
        for i, food_name in enumerate(cat_foods.keys()):
            with cols[i % 4]:
                if st.button(
                    food_name,
                    key=f"btn_{food_name}",
                    type="secondary" if food_name not in st.session_state.selected_foods else "primary",
                    use_container_width=True
                ):
                    if food_name in st.session_state.selected_foods:
                        st.session_state.selected_foods.remove(food_name)
                    else:
                        st.session_state.selected_foods.append(food_name)
                    st.rerun()

selected_foods = st.session_state.selected_foods

# 선택된 음식 표시 & 수량 입력
total_stats = {"kcal": 0, "carbs": 0, "protein": 0, "fat": 0}
quantities = {}

if selected_foods:
    st.divider()
    st.subheader("✏️ 선택된 음식 & 수량")

    if st.button("🗑 전체 초기화", type="secondary"):
        st.session_state.selected_foods = []
        st.rerun()

    cols = st.columns(min(len(selected_foods), 3))
    for i, food in enumerate(selected_foods):
        with cols[i % 3]:
            count = st.number_input(f"{food}", min_value=0.0, value=1.0, step=0.5, key=f"qty_{food}")
            quantities[food] = count
            total_stats["kcal"]    += food_db[food]["kcal"]    * count
            total_stats["carbs"]   += food_db[food]["carbs"]   * count
            total_stats["protein"] += food_db[food]["protein"] * count
            total_stats["fat"]     += food_db[food]["fat"]     * count

    st.divider()

    # 5. 메트릭
    st.subheader("📊 실시간 섭취 현황")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("총 칼로리",  f"{total_stats['kcal']:.0f} kcal",    f"{total_stats['kcal']-target_kcal:.0f} kcal",    delta_color="inverse")
    m2.metric("탄수화물",   f"{total_stats['carbs']:.1f} g",      f"{total_stats['carbs']-target_carbs:.1f} g",     delta_color="inverse")
    m3.metric("단백질",     f"{total_stats['protein']:.1f} g",   f"{total_stats['protein']-target_protein:.1f} g")
    m4.metric("지방",       f"{total_stats['fat']:.1f} g",        f"{total_stats['fat']-target_fat:.1f} g",         delta_color="inverse")

    # 6. 목표 대비 게이지
    st.subheader("🎯 목표 달성률")
    g1, g2, g3, g4 = st.columns(4)

    def gauge(col, label, value, target, color):
        pct = min(value / target * 100, 150) if target > 0 else 0
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=value,
            delta={"reference": target, "valueformat": ".0f"},
            title={"text": label, "font": {"size": 13}},
            gauge={
                "axis": {"range": [0, target * 1.5], "tickfont": {"size": 9}},
                "bar": {"color": color},
                "steps": [
                    {"range": [0, target * 0.8], "color": "#e8f5e9"},
                    {"range": [target * 0.8, target], "color": "#fff9c4"},
                    {"range": [target, target * 1.5], "color": "#ffebee"},
                ],
                "threshold": {"line": {"color": "red", "width": 2}, "value": target},
            },
            number={"suffix": " kcal" if label == "칼로리" else " g", "font": {"size": 14}},
        ))
        fig.update_layout(height=200, margin=dict(t=40, b=10, l=20, r=20))
        col.plotly_chart(fig, use_container_width=True)

    gauge(g1, "칼로리",   total_stats["kcal"],    target_kcal,    "#ef5350")
    gauge(g2, "탄수화물", total_stats["carbs"],   target_carbs,   "#ff9800")
    gauge(g3, "단백질",   total_stats["protein"], target_protein, "#42a5f5")
    gauge(g4, "지방",     total_stats["fat"],     target_fat,     "#ab47bc")

    # 7. 차트
    c1, c2 = st.columns(2)

    with c1:
        chart_df = pd.DataFrame({
            "영양소": ["탄수화물", "단백질", "지방"],
            "섭취량(g)": [total_stats["carbs"], total_stats["protein"], total_stats["fat"]]
        })
        chart_df = chart_df[chart_df["섭취량(g)"] > 0]
        if not chart_df.empty:
            fig = px.pie(chart_df, values="섭취량(g)", names="영양소", hole=0.4,
                         title="오늘의 영양 균형",
                         color_discrete_sequence=["#ff9800", "#42a5f5", "#ab47bc"])
            st.plotly_chart(fig, use_container_width=True)

    with c2:
        targets_df = pd.DataFrame({
            "영양소": ["탄수화물", "단백질", "지방"],
            "섭취": [total_stats["carbs"], total_stats["protein"], total_stats["fat"]],
            "목표": [target_carbs, target_protein, target_fat],
        })
        fig2 = px.bar(targets_df, x="영양소", y=["섭취", "목표"],
                      barmode="group", title="섭취 vs 목표",
                      color_discrete_map={"섭취": "#42a5f5", "목표": "#e0e0e0"})
        fig2.update_layout(legend_title_text="")
        st.plotly_chart(fig2, use_container_width=True)

    # 8. AI 영양 조언
    st.divider()
    st.subheader("💬 영양 조언")

    kcal_ratio  = total_stats["kcal"]    / target_kcal    if target_kcal    else 0
    carb_ratio  = total_stats["carbs"]   / target_carbs   if target_carbs   else 0
    prot_ratio  = total_stats["protein"] / target_protein if target_protein else 0
    fat_ratio   = total_stats["fat"]     / target_fat     if target_fat     else 0

    advices = []

    # 칼로리
    if kcal_ratio > 1.2:
        advices.append(("🔴", "칼로리 초과",
            f"목표보다 {total_stats['kcal']-target_kcal:.0f} kcal 더 섭취했습니다. "
            "저녁은 샐러드나 단백질 위주로 가볍게 드세요."))
    elif kcal_ratio > 1.0:
        advices.append(("🟠", "칼로리 주의",
            f"목표 칼로리에 근접했습니다. 간식은 피하고 물을 충분히 드세요."))
    elif kcal_ratio < 0.5:
        advices.append(("🔵", "칼로리 부족",
            f"아직 {target_kcal - total_stats['kcal']:.0f} kcal 남았습니다. 규칙적인 식사가 중요해요!"))
    else:
        advices.append(("🟢", "칼로리 양호",
            f"칼로리 섭취가 적절합니다. 잘 하고 계세요!"))

    # 탄수화물
    if carb_ratio > 1.2:
        advices.append(("🟠", "탄수화물 과다",
            "탄수화물이 많습니다. 다음 식사는 채소·단백질 위주로 구성하세요."))
    elif carb_ratio < 0.4:
        advices.append(("🔵", "탄수화물 부족",
            "에너지원인 탄수화물이 부족합니다. 통곡물·고구마 등 복합 탄수화물을 추가하세요."))

    # 단백질
    if prot_ratio < 0.6:
        advices.append(("🟡", "단백질 부족",
            f"단백질이 목표의 {prot_ratio*100:.0f}%입니다. "
            "닭가슴살·달걀·두부·그릭요거트로 보충하세요."))
    elif prot_ratio >= 1.0:
        advices.append(("🟢", "단백질 충족",
            "단백질 목표를 달성했습니다. 근육 유지에 좋습니다!"))

    # 지방
    if fat_ratio > 1.3:
        advices.append(("🔴", "지방 과다",
            "포화지방이 많을 수 있습니다. 튀김·패스트푸드는 줄이고 견과류·아보카도 같은 "
            "불포화지방으로 대체하세요."))

    # 종합 균형
    carb_pct  = total_stats["carbs"]   * 4 / total_stats["kcal"] * 100 if total_stats["kcal"] else 0
    prot_pct  = total_stats["protein"] * 4 / total_stats["kcal"] * 100 if total_stats["kcal"] else 0
    fat_pct   = total_stats["fat"]     * 9 / total_stats["kcal"] * 100 if total_stats["kcal"] else 0

    if carb_pct > 65:
        advices.append(("🟠", "탄수화물 비율 높음",
            f"현재 탄수화물 비율이 {carb_pct:.0f}%입니다. 이상적 범위는 45~65%예요."))
    if prot_pct < 15:
        advices.append(("🟡", "단백질 비율 낮음",
            f"단백질 비율이 {prot_pct:.0f}%로 낮습니다. 15~25%를 목표로 해보세요."))

    for icon, title, msg in advices:
        if icon == "🔴":
            st.error(f"**{icon} {title}** — {msg}")
        elif icon == "🟠":
            st.warning(f"**{icon} {title}** — {msg}")
        elif icon == "🟢":
            st.success(f"**{icon} {title}** — {msg}")
        else:
            st.info(f"**{icon} {title}** — {msg}")

    # 9. 음식별 칼로리 상세
    with st.expander("📋 음식별 상세 칼로리 보기"):
        detail_rows = []
        for food in selected_foods:
            qty = quantities.get(food, 1)
            d = food_db[food]
            detail_rows.append({
                "음식": food,
                "수량": qty,
                "칼로리(kcal)": round(d["kcal"] * qty),
                "탄수화물(g)":  round(d["carbs"] * qty, 1),
                "단백질(g)":    round(d["protein"] * qty, 1),
                "지방(g)":      round(d["fat"] * qty, 1),
            })
        st.dataframe(pd.DataFrame(detail_rows), use_container_width=True, hide_index=True)

else:
    st.info("위 탭에서 음식을 클릭해 선택하세요. 선택 즉시 데이터가 업데이트됩니다.")
