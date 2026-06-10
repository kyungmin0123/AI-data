import streamlit as st
import pandas as pd
import plotly.express as px

# ========== 페이지 설정 ==========
st.set_page_config(
    page_title="AI 학습용 데이터 구축 현황 대시보드",
    page_icon="🤖",
    layout="wide"
)

# ========== 데이터 로드 ==========
@st.cache_data
def load_data():
    df = pd.read_csv("data.csv", encoding="utf-8-sig")
    df.columns = df.columns.str.strip()
    df["연도"] = df["연도"].astype(int)
    df["분야"] = df["분야"].str.strip()

    # 카테고리 분류 함수
    def categorize(row):
        분야 = str(row["분야"])
        내용 = str(row["주요내용"])

        if any(k in 분야 or k in 내용 for k in ["음성", "대화", "말뭉치", "텍스트", "번역", "독해", "방언", "OCR", "법률", "법령", "특허", "일반상식", "요약", "명령어", "챗봇"]):
            return "언어·텍스트"
        elif any(k in 분야 or k in 내용 for k in ["자율주행", "주행", "도로", "교통", "드론", "항만", "자율버스", "로봇관점"]):
            return "자율주행·교통"
        elif any(k in 분야 or k in 내용 for k in ["암", "진단", "의료", "헬스케어", "질환", "뇌파", "수면", "피부", "구강", "치매", "진료", "건강", "신장", "폐암", "체부", "신경", "자궁"]):
            return "의료·헬스케어"
        elif any(k in 분야 or k in 내용 for k in ["농업", "농작물", "작물", "축산", "어류", "산림", "피복", "농경", "농산물"]):
            return "농업·환경"
        elif any(k in 분야 or k in 내용 for k in ["안전", "CCTV", "보안", "이상행동", "산업안전", "시설물", "생활안전", "위해물품", "위험"]):
            return "안전·보안"
        elif any(k in 분야 or k in 내용 for k in ["환경", "오염", "상하수도", "위성영상"]):
            return "환경·인프라"
        else:
            return "이미지·영상"

    df["카테고리"] = df.apply(categorize, axis=1)
    return df

df = load_data()

# ========== 카테고리 색상 ==========
category_colors = {
    "언어·텍스트":   "#4A90D9",
    "이미지·영상":   "#7ED321",
    "의료·헬스케어": "#E74C3C",
    "자율주행·교통": "#F39C12",
    "농업·환경":     "#27AE60",
    "안전·보안":     "#8E44AD",
    "환경·인프라":   "#16A085"
}

category_icons = {
    "언어·텍스트":   "💬",
    "이미지·영상":   "🖼️",
    "의료·헬스케어": "🏥",
    "자율주행·교통": "🚗",
    "농업·환경":     "🌱",
    "안전·보안":     "🔒",
    "환경·인프라":   "🌊"
}

# ========== 타이틀 ==========
st.markdown("""
    <h1 style='text-align: center; color: #2C3E50;'>
        🤖 AI 학습용 데이터 구축 현황 대시보드
    </h1>
    <p style='text-align: center; color: #7F8C8D; font-size: 16px;'>
        한국지능정보사회진흥원 | 2017 ~ 2020
    </p>
    <hr>
""", unsafe_allow_html=True)

# ========== 사이드바 필터 ==========
st.sidebar.title("🔍 필터 옵션")
st.sidebar.markdown("---")

years = sorted(df["연도"].unique())
selected_years = st.sidebar.multiselect(
    "📅 연도 선택",
    options=years,
    default=years
)

categories = sorted(df["카테고리"].unique())
selected_categories = st.sidebar.multiselect(
    "📂 카테고리 선택",
    options=categories,
    default=categories
)

st.sidebar.markdown("---")
st.sidebar.info("💡 필터를 조정하여 원하는 데이터를 확인하세요!")

# 필터 적용
filtered_df = df[
    (df["연도"].isin(selected_years)) &
    (df["카테고리"].isin(selected_categories))
]

# ========== KPI 카드 ==========
st.markdown("### 📊 전체 현황")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="📁 전체 데이터셋 수",
        value=f"{len(filtered_df)}개",
        delta=f"전체 {len(df)}개 중"
    )
with col2:
    st.metric(
        label="📅 선택 연도 범위",
        value=f"{len(selected_years)}개 연도",
        delta=f"{min(selected_years) if selected_years else '-'} ~ {max(selected_years) if selected_years else '-'}"
    )
with col3:
    st.metric(
        label="📂 카테고리 수",
        value=f"{filtered_df['카테고리'].nunique()}개",
        delta="분야별 분류"
    )
with col4:
    if not filtered_df.empty:
        most_common = filtered_df['카테고리'].value_counts().idxmax()
        most_count = filtered_df['카테고리'].value_counts().max()
    else:
        most_common, most_count = "-", 0
    st.metric(
        label="🏆 최다 카테고리",
        value=most_common,
        delta=f"{most_count}개 데이터셋"
    )

st.markdown("---")

# ========== 차트 1행 ==========
st.markdown("### 📈 연도별 · 카테고리별 분석")
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 📅 연도별 데이터셋 구축 수")
    year_count = filtered_df.groupby("연도").size().reset_index(name="데이터셋 수")
    fig1 = px.bar(
        year_count,
        x="연도",
        y="데이터셋 수",
        color="데이터셋 수",
        color_continuous_scale="Blues",
        text="데이터셋 수"
    )
    fig1.update_traces(textposition="outside")
    fig1.update_layout(
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(tickmode="linear"),
        height=350
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("#### 📂 카테고리별 데이터셋 비율")
    cat_count = filtered_df["카테고리"].value_counts().reset_index()
    cat_count.columns = ["카테고리", "데이터셋 수"]
    fig2 = px.pie(
        cat_count,
        names="카테고리",
        values="데이터셋 수",
        color="카테고리",
        color_discrete_map=category_colors,
        hole=0.4
    )
    fig2.update_traces(textposition="inside", textinfo="percent+label")
    fig2.update_layout(
        height=350,
        paper_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig2, use_container_width=True)

# ========== 차트 2행 ==========
col3, col4 = st.columns(2)

with col3:
    st.markdown("#### 🔄 연도별 카테고리 구성 변화")
    year_cat = filtered_df.groupby(["연도", "카테고리"]).size().reset_index(name="데이터셋 수")
    fig3 = px.bar(
        year_cat,
        x="연도",
        y="데이터셋 수",
        color="카테고리",
        color_discrete_map=category_colors,
        barmode="stack",
        text_auto=True
    )
    fig3.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(tickmode="linear"),
        height=350,
        legend=dict(orientation="h", yanchor="bottom", y=-0.6)
    )
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.markdown("#### 📊 카테고리별 데이터셋 수 (가로 막대)")
    cat_bar = filtered_df["카테고리"].value_counts().reset_index()
    cat_bar.columns = ["카테고리", "데이터셋 수"]
    fig4 = px.bar(
        cat_bar.sort_values("데이터셋 수"),
        x="데이터셋 수",
        y="카테고리",
        orientation="h",
        color="카테고리",
        color_discrete_map=category_colors,
        text="데이터셋 수"
    )
    fig4.update_traces(textposition="outside")
    fig4.update_layout(
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=350
    )
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# ========== 카테고리별 상세 카드 ==========
st.markdown("### 📋 카테고리별 상세 데이터")

for category in selected_categories:
    cat_df = filtered_df[filtered_df["카테고리"] == category]
    if cat_df.empty:
        continue

    icon  = category_icons.get(category, "📁")
    color = category_colors.get(category, "#333333")

    with st.expander(f"{icon} {category} ({len(cat_df)}개)", expanded=False):
        for _, row in cat_df.iterrows():
            st.markdown(f"""
                <div style='
                    background-color: #F8F9FA;
                    border-left: 5px solid {color};
                    padding: 10px 15px;
                    margin: 8px 0;
                    border-radius: 5px;
                '>
                    <b style='color: {color};'>📌 [{row["연도"]}] {row["분야"]}</b><br>
                    <span style='color: #555; font-size: 14px;'>{row["주요내용"]}</span>
                </div>
            """, unsafe_allow_html=True)

st.markdown("---")

# ========== 데이터 테이블 ==========
st.markdown("### 📄 전체 데이터 테이블")

search = st.text_input("🔍 키워드 검색 (분야, 주요내용)", "")

if search:
    table_df = filtered_df[
        filtered_df["분야"].str.contains(search, case=False, na=False) |
        filtered_df["주요내용"].str.contains(search, case=False, na=False)
    ]
else:
    table_df = filtered_df

st.dataframe(
    table_df[["연도", "카테고리", "분야", "주요내용"]].reset_index(drop=True),
    use_container_width=True,
    height=400
)
st.markdown(f"**총 {len(table_df)}개** 데이터셋이 표시되고 있습니다.")

# ========== 푸터 ==========
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #AAA; font-size: 13px;'>
        📊 데이터 출처: 한국지능정보사회진흥원_인공지능 학습용 데이터 구축 현황 (2021.01.04)<br>
        🏫 당곡고등학교 AI 학습 대시보드
    </div>
""", unsafe_allow_html=True)
