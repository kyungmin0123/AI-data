import streamlit as st
import pandas as pd
import plotly.express as px
import io

# ========== 페이지 설정 ==========
st.set_page_config(
    page_title="AI 학습용 데이터 구축 현황 대시보드",
    page_icon="🤖",
    layout="wide"
)

# ========== 데이터 (CSV 문자열로 내장) ==========
CSV_DATA = """연도,분야,주요내용
2017,법률,국가법령 중 교통사고 층간소음 창업 인허가 분야의 관련 법령 조문 판례 법률용어 데이터 11만건
2017,특허,국내 출원·등록된 전기·전자분야의 특허정보 심사정보 특허전문기술용어 데이터 100만건
2017,일반상식,한국어 위키백과에서 활용도가 높은 일반상식 데이터 15만건
2017,이미지,한국인 안면 이미지 600만장(200명) 및 한국음식 이미지 데이터 15만장(150종)
2018,헬스케어,안저 이미지에 주요 질환(녹내장 황반변성 당뇨망막증 등)의 전문의 검사소견을 결합한 데이터셋 3천장
2018,관광,주요 관광특구내 식당 시설의 이미지에 각종 다국어(한영중일) 정보를 결합한 데이터셋 150만건
2018,농업,국내 농작물의 영농정보 상담정보 지원사업정보 등을 가공한 데이터 및 농작물 병충해 이미지 데이터 5만건
2018,특허,전기·전자 기계 화학 분야의 출원 등록된 특허 청구항 정보 특허전문기술용어 데이터 70만건
2018,법령,이혼 한부모가족 학교폭력 퇴직금 분야 법령정보(법령 판례 사례 용어 등) 데이터 10만건
2018,이미지,한국인 안면이미지(200명) 구축 및 국산차량(100종)에 대한 이미지 데이터 615여만장
2019,한국어 음성,한국어 음성 인식 성능을 향상시키기 위해 자유연속발화 소음 환경 등을 고려한 음성 데이터 1000시간
2019,한국어 대화,영상에서 인물의 표정 음성(억양) 발화 내용 등의 감정이 포함된 멀티모달 영상 데이터 20시간
2019,멀티모달,중소상인 비즈니스에 적용가능한 한국어 챗봇 구축을 위한 한국어 표준 대화 시나리오 데이터 50만건
2019,기계독해,지문으로부터 AI가 학습을 통해 질의에 대한 답변을 추론하는 딥러닝 기반 기계독해(MRC) 데이터 40만건
2019,한영 번역 말뭉치,한국어 인공지능 번역 기술개발 및 성능강화를 위한 한국어-영어 병렬 말뭉치 데이터 160만건
2019,사물 이미지,한국형 객체 장소 상황 인지기술 개발 및 성능강화를 위한 사물/거리/건물/랜드마크 등 사물 이미지 데이터 360만건
2019,글자체 이미지,한글 광학글자인식(OCR) 성능개선을 위한 한글 글자체(손글씨 및 인쇄체) 이미지 660만건(580만자)
2019,인도보행 영상,시각장애인/전동휠체어 등의 보행지원기술 개발을 위한 국내 인도·횡단보도 보행 영상 및 라벨링 데이터 67만건(200시간)
2019,멀티모달 영상,감성인식 AI개발을 위해 동영상에서 인물의 표정 음성 발화 내용 상황 등의 정보가 포함된 멀티모달 영상 데이터 6천건(100시간)
2019,사람동작 영상,사람의 동작·자세·행동 인식기술 개발을 위해 다양한 조건에서 사람 동작 영상 데이터 50만건(20만 클립)
2019,안면 이미지,다양한 각도 조도 등의 환경 하에서 안면인식·식별 성능강화를 위한 한국인 얼굴 이미지 데이터 1944만장
2019,위해물품 엑스레이 이미지,위험물·도구 자동판별 기술개발 및 성능개선을 위한 위험물 범죄 도구 반입금지물품 등의 X-ray 이미지 48만장
2019,질병진단 이미지,안저질환 이미지 유방암 엑스레이 이미지 및 진단결과(질환 및 정상)를 라벨링한 질병진단 이미지 데이터 3만장
2020,문서요약 텍스트,AI가 텍스트를 이해하고 핵심 내용을 요약적으로 전달하기 위해 가공된 다양한 유형의 대규모 요약 텍스트 데이터(원문 40만건)
2020,대용량 동영상 콘텐츠,대용량 동영상 내 객체 탐지 상황 이해 행동 분석을 위한 대용량 동영상 AI 데이터 500시간
2020,딥페이크 변조영상,GAN 기반의 다양한 변형 알고리즘을 통해 생성된 변조 영상을 탐지하는 AI기술 개발에 필요한 원본 및 변조 영상 데이터(15만개)
2020,수어 영상,생활 이미지와 이미지에 대한 질문을 입력받아 질문에 대한 답을 생성하는 AI데이터 20만개
2020,시각정보 기반 질의응답,생활 이미지와 이미지에 대한 질문을 입력받아 질문에 대한 답을 생성하는 AI데이터(이미지 135만장 질의응답 750만쌍)
2020,전문분야 한영 말뭉치,대법원 판례 의료/보건 가정통신문 금융/IT 관광/문화 등 전문분야별 한영 말뭉치 155만건
2020,랜드마크 이미지,국내 도심 민간건물 공공기관 관광명소 편의시설 등 국내 도시별 주요 랜드마크 이미지 데이터
2020,자율주행드론 비행 영상,관광지 도심지 산림지 4K 25FPS 320시간 및 LiDAR 영상데이터 60시간
2020,한국인 대화음성,한국인의 일상 대화를 인식하고 음성을 문자로 실시간 변환하는 AI 기술 개발을 위한 대화 음성 데이터(음성 4000시간 텍스트 400만문장)
2020,사람 인체·자세 3D,2D인체 영상을 3D모델로 변환할 때 자세(pose)와 형태(shape)를 추론하기 위한 2D-3D 인체 데이터(2D 이미지 200만장 3D모델 50만건)
2020,질병진단 이미지,유방암 및 감염병(부비동) 질환의 진단을 위한 의료 영상 이미지 AI데이터(유방암 병리 이미지 10만건 부비동 8000건)
2020,도로환경 파노라마 이미지,자율주행용 이미지 AI데이터(도심지 파노라마 3400km 338910장 94시간 규모)
2020,피트니스 자세 이미지,피트니스 자세 평가/피드백 AI Application을 개발하고자 하는 기관들이 사용할 AI데이터(20만개)
2020,K-Fashion 이미지,구매 또는 직접 촬영하여 저작권 문제가 해결된 패션 이미지의 패션 요소 정보를 어노테이션한 이미지 120만장
2020,한국인 재식별 이미지,대한민국의 실내/외 구축된 공공 CCTV 환경을 고려한 한국인(1000명) 재식별 데이터 400만장
2020,도로주행영상,70건 이상 실도로 주행 데이터 기반 총 175TB 상당의 자율주행 원천데이터 수집 총 학습용 데이터 60만 5천 프레임
2020,치매진단 뇌파영상,기계학습(딥러닝) 기반의 의료영상진단 AI기술의 개발·확산을 위해 치매와 경도인지장애 및 이와 관련된 질환의 영상 데이터(MRI) 및 임상전문의의 진단정보 등을 어노테이션한 AI데이터 28만건
2020,감성 대화 말뭉치,우울증 등 심리 장애로 인한 사회문제 해결을 위해 감성대화 코퍼스 데이터(발화 음성 1만건 코퍼스 27만문장)
2020,위성영상 객체판독,국내 위성 영상 활용 산업의 발전을 위해 아리랑 위성영상을 이용한 범용 위성정보 데이터 120만건
2020,구강악 2D·3D 이미지,치아 및 치주질환 진단과 치료계획 수립을 위한 파노라마 영상과 CBCT 영상 데이터(파노라마 5천장 CBCT 20만장)
2020,자유대화,한국인의 음성을 문자로 바꾸고 문맥을 이해하는 한국어 음성언어처리 기술 개발을 위한 AI 학습용 한국어 음성 DB
2020,명령어,전 연령층을 대상으로 한 명령어 데이터를 수집하고 차량 내 대화 및 명령어 데이터를 수집한 AI 학습용 한국어 음성 DB
2020,상황별음성,한국인의 음성을 문자로 바꾸어 주고 문맥을 이해하는 한국어 음성 언어처리 기술 개발을 위한 AI 학습용 한국어 음성 DB
2020,한국어 방언,방언을 사용하는 발화자의 일상 대화를 수집하여 녹취하고 음성을 인식하고 텍스트로 전사하여 방언음성의 합성 및 활용 가능한 방언 발화 데이터
2020,요약 데이터,AI가 텍스트를 이해하고 핵심 내용을 요약적으로 전달하기 위해 가공된 다양한 유형의 대규모 요약 텍스트 데이터
2020,한국어 텍스트,도서자료 기계독해 콜센터(민원) 질의-응답 데이터 전문분야 말뭉치 한국어 SNS 등 총 4가지 도메인의 대규모 한국어 기반 텍스트 데이터
2020,영어 번역 말뭉치,고품질과 활용 가능성이 높은 전문분야의 영어 번역 말뭉치 300만개
2020,중국어-일본어 번역 말뭉치,한국어-중국어 한국어-일본어의 양질의 대규모 AI 학습용 번역 데이터 말뭉치
2020,OCR,현실 곳곳에 존재하는 한글 이미지 다양한 서체의 한글 글자체 공공행정문서 OCR 데이터
2020,소화기계,위암 대장암 의료 영상정보를 기반으로 한 인공지능 학습용 데이터
2020,신장계암,신장암 전립선암 임상정보를 기반으로 한 진단 CT영상 병리영상 수술 동영상 등 다차원적 인공지능 학습용 데이터
2020,간췌담도계암,판독 식별 분류 예측 등에 필요한 의료 영상 및 이와 관련한 진단과정에 필요한 의료정보가 결합된 데이터
2020,체부암,폐암의 X-ray CT PET CT 3종 갑상선의 초음파 Neck CT 세침흡인검사 병리이미지 3종 유방암 관련 데이터
2020,신경계질환,뇌혈관 질환 치매 및 인지기능 장애 등 신경계 질환의 진단 지원 AI 개발을 위한 학습용 데이터
2020,수면질,수면다원검사 학습용 데이터
2020,피부질환,피부질환 사진 및 임상 정보
2020,구강계질환,공공 및 민간 인공지능 정보기술의 개발을 촉진하기 위한 구강 점막질환 및 치과 x-ray 영상 학습용 데이터
2020,진료 및 건강,뇌경색 영상 데이터 수집/구축 진단/예방/치료데이터 처리 정제 및 저장 데이터 변환 및 표준화 인공지능 학습 데이터 구축
2020,주행 환경 정적 객체 인지,주행 환경 정적 객체 인지를 위한 AI 학습용 데이터
2020,동적 객체 인지,자율주행 기반 AI 학습용 데이터 기반 마련을 위해 동적 객체 인지(주차 장애물 인지 주차 관련 이동체 인지 차량·사람 인지) 데이터
2020,도로상태 및 자율버스,대규모 주행 데이터셋을 이용한 자율주행 분야 AI데이터
2020,드론 영상 데이터,드론을 통해 수집된 영상 학습데이터
2020,항만구조물,자율 운항의 기초 및 해상교통 사고 방지의 기초가 되는 지상 구조물에 대한 인식을 위한 학습데이터
2020,농업 영상 데이터,위성/드론 농경작지 촬영 영상 분야 농산물 품질(QC) 이미지 분야 시설 작물 개체 영상 분야 주요 농작물 생육 이미지 데이터 분야에 대한 영상 데이터
2020,작물 질병 해충 데이터,농지 시설 등 경작 작물의 재배 현황 및 작황 분석의 AI 기술 개발을 위한 다양한 작물의 질병 및 해충 데이터
2020,축산물 품질 및 가축행동 영상,축산물 품질 관리 강화 및 가축관리 시스템 구축을 위한 축산물 품질(QC) 이미지 및 가축 행동 영상 데이터
2020,어류행동 및 개체 데이터,양식어류의 행동 분석 개체추적 등을 위한 수산 AI 개발용 영상 데이터
2020,피복지도 및 산림수종 데이터,AI가 항공/위성 영상 중 토지피복 8개의 클래스 및 산림수종 4개의 클래스를 구분할 수 있도록 학습할 데이터
2020,환경오염,수질측정 및 오염원 데이터 산업 폐기물 이미지 생활 폐기물 이미지 데이터 수집·가공
2020,상하수도 및 열화상,지하에 매설된 상하수관로의 누수 및 파손 발생 시 AI 기반 상태진단 및 판단을 통한 안전관리를 위한 상하수도관 공간 및 누수 데이터
2020,영상 콘텐츠 이해,영유아 교육 영상 콘텐츠 장면인식/인물 인식을 위한 방송 영상 콘텐츠 영상이해(맥락) 기술을 위한 방송 영상 콘텐츠 3개 분야 AI 학습데이터
2020,감정인식 및 요약영상,한국인의 얼굴 표정과 상황적 맥락을 고려한 감정인식 학습모델 개발을 위한 영상 데이터셋과 다양한 카테고리의 영상 요약 학습모델 개발을 위한 동영상 요약 데이터
2020,사람행동영상,미디어 분야의 사람 행동 영상에서 2D-3D 자세와 형태 정보를 추출하여 이에 대한 데이터
2020,스포츠 사람동작,대표적인 운동인 골프 축구 농구의 스포츠 인공지능 분야 생태계 활성화를 위한 스포츠 인공지능 학습용 데이터
2020,교통안전,고속도로 시내도로 주유소 등의 CCTV 영상에서 차량과 교통관련 정보 측정 및 운전자의 상태를 판별하는 AI 기술 개발용 데이터
2020,산업안전,항공 활주로 내 이상물체 감지를 위한 객체 데이터 공사현장 안전장비 인식 데이터 화재 발생 예측 데이터(연기 동영상)
2020,CCTV영상,도시철도 역사 내 이상행동 13종 및 동일인 추적 대상 6종을 대상으로 CCTV 영상 인공지능 데이터
2020,생활안전,스쿨존 어린이 안전사회협력망 노인 이상행동 돌봄 등 생활안전 데이터
2020,시설물안전,국가 SOC 시설물이나 대형 건축물의 균열(결함) 데이터를 수집 구축하여 AI를 통해 결함 유형을 분류하는 학습데이터
2020,안면 이미지,딥러닝 기반 얼굴인식 알고리즘을 학습시키기 위한 얼굴 위변조 공격에 대응하기 위한 데이터
2020,실내라이다 및 AR VR,광량 변화가 존재하는 실내 환경에서 보행자가 이동할 때 이를 정확하게 추적할 수 있는 보행자 추적 기술을 개발하기 위한 학습 데이터
2020,상품이미지 및 고객 주문질의,무인 스토어 물류창고 t-commerce 등 다양한 분야에서 활용할 수 있는 상품이미지 데이터 및 고객 질의-응답 데이터
2020,로봇관점 주행 영상 데이터,국내 환경에 적합한 로봇 관점의 특화 자율주행 기술 및 서비스 개발 및 고도화를 위하여 다양한 주행 환경에서 로봇 관점의 주행 영상기반의 고품질 인공지능 학습용 데이터
2020,음식분류,AI 학습 이미지 데이터를 개발 각 음식별 영양성분(칼로리 당분 염도)에 해당하는 데이터
2020,반려동물,고품질의 반려동물 행동분석 AI 학습용 데이터
2020,수학분야 학습자 역량 측정,수학 분야 교과지식체계 및 학습자 역량 측정 및 탐색을 위한 데이터
2020,기계시설물 고장 예지 센서,데이터 구축이 어려운 정상 또는 고장 상태의 정보를 포함하는 모터의 인공지능 학습용 전류 및 진동 데이터
2020,해상 객체 이미지,중소·벤처 스타트업 등 민간의 해사교통안전 관련 인공지능 기술개발 촉진을 위한 대규모 인공지능 학습용 데이터
2020,교통 약자 주행 영상,전동휠체어 의료용 스쿠터 유모차 보행기 보행차 사용자들을 위한 배리어프리 존 관련 객체를 고려한 다양한 객체 데이터
2020,특수환경 자율주행 3D,고수준 자율주행에서 가장 핵심적인 역할을 하는 라이다 데이터가 포함된 2D-3D 융합 데이터 셋 및 일반 주행 영상 데이터"""

# ========== 데이터 로드 ==========
@st.cache_data
def load_data():
    df = pd.read_csv(io.StringIO(CSV_DATA))
    df.columns = df.columns.str.strip()
    df["연도"] = df["연도"].astype(int)
    df["분야"] = df["분야"].str.strip()

    def categorize(row):
        분야 = str(row["분야"])
        내용 = str(row["주요내용"])
        combined = 분야 + 내용

        if any(k in combined for k in ["자율주행", "주행", "도로", "자율버스", "로봇관점", "주행 환경", "동적 객체", "특수환경 자율"]):
            return "자율주행·교통"
        elif any(k in combined for k in ["교통안전", "교통 약자", "항만", "드론 영상"]):
            return "자율주행·교통"
        elif any(k in combined for k in ["암", "진단", "의료", "헬스케어", "질환", "뇌파", "수면", "피부", "구강", "치매", "진료", "건강", "신장", "폐암", "체부", "신경", "자궁", "헬스"]):
            return "의료·헬스케어"
        elif any(k in combined for k in ["농업", "농작물", "작물", "축산", "어류", "산림", "피복", "농경", "농산물", "해충"]):
            return "농업·환경"
        elif any(k in combined for k in ["안전", "CCTV", "이상행동", "산업안전", "시설물", "생활안전", "위해물품", "위험", "딥페이크"]):
            return "안전·보안"
        elif any(k in combined for k in ["환경오염", "오염", "상하수도", "위성영상", "열화상"]):
            return "환경·인프라"
        elif any(k in combined for k in ["음성", "대화", "말뭉치", "텍스트", "번역", "독해", "방언", "OCR", "법률", "법령", "특허", "일반상식", "요약", "명령어", "챗봇", "멀티모달", "감성 대화"]):
            return "언어·텍스트"
        else:
            return "이미지·영상"

    df["카테고리"] = df.apply(categorize, axis=1)
    return df

df = load_data()

# ========== 카테고리 색상 & 아이콘 ==========
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
    "📅 연도 선택", options=years, default=years
)

categories = sorted(df["카테고리"].unique())
selected_categories = st.sidebar.multiselect(
    "📂 카테고리 선택", options=categories, default=categories
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
    st.metric("📁 전체 데이터셋 수", f"{len(filtered_df)}개", f"전체 {len(df)}개 중")
with col2:
    y_min = min(selected_years) if selected_years else "-"
    y_max = max(selected_years) if selected_years else "-"
    st.metric("📅 선택 연도 범위", f"{len(selected_years)}개 연도", f"{y_min} ~ {y_max}")
with col3:
    st.metric("📂 카테고리 수", f"{filtered_df['카테고리'].nunique()}개", "분야별 분류")
with col4:
    if not filtered_df.empty:
        most_common = filtered_df['카테고리'].value_counts().idxmax()
        most_count  = filtered_df['카테고리'].value_counts().max()
    else:
        most_common, most_count = "-", 0
    st.metric("🏆 최다 카테고리", most_common, f"{most_count}개 데이터셋")

st.markdown("---")

# ========== 차트 1행 ==========
st.markdown("### 📈 연도별 · 카테고리별 분석")
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 📅 연도별 데이터셋 구축 수")
    year_count = filtered_df.groupby("연도").size().reset_index(name="데이터셋 수")
    fig1 = px.bar(
        year_count, x="연도", y="데이터셋 수",
        color="데이터셋 수", color_continuous_scale="Blues",
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
        cat_count, names="카테고리", values="데이터셋 수",
        color="카테고리", color_discrete_map=category_colors, hole=0.4
    )
    fig2.update_traces(textposition="inside", textinfo="percent+label")
    fig2.update_layout(height=350, paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig2, use_container_width=True)

# ========== 차트 2행 ==========
col3, col4 = st.columns(2)

with col3:
    st.markdown("#### 🔄 연도별 카테고리 구성 변화")
    year_cat = filtered_df.groupby(["연도", "카테고리"]).size().reset_index(name="데이터셋 수")
    fig3 = px.bar(
        year_cat, x="연도", y="데이터셋 수",
        color="카테고리", color_discrete_map=category_colors,
        barmode="stack", text_auto=True
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
    st.markdown("#### 📊 카테고리별 데이터셋 수")
    cat_bar = filtered_df["카테고리"].value_counts().reset_index()
    cat_bar.columns = ["카테고리", "데이터셋 수"]
    fig4 = px.bar(
        cat_bar.sort_values("데이터셋 수"),
        x="데이터셋 수", y="카테고리", orientation="h",
        color="카테고리", color_discrete_map=category_colors,
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

for category in sorted(selected_categories):
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

# ========== 검색 + 데이터 테이블 ==========
st.markdown("### 📄 전체 데이터 테이블")
search = st.text_input("🔍 키워드 검색 (분야 또는 주요내용)", "")

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
