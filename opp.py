import streamlit as st
import google.generativeai as genai

# 1. 사이드바 메뉴 설정
st.sidebar.title("🎬 AI Studio 작업실")
app_mode = st.sidebar.selectbox("앱 선택", ["시나리오 어시스턴트", "스토리보드 생성기"])

# 2. API 키 연결 (Streamlit 비밀설정에서 가져옴)
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    st.error("API 키 설정이 필요합니다. Streamlit Cloud의 Secrets 설정을 확인하세요.")

# 3. 각 앱의 기능 구현
if app_mode == "시나리오 어시스턴트":
    st.header("✍️ 시나리오 어시스턴트")
    
    # [실시간 프롬프트 수정창]
    with st.expander("⚙️ 프롬프트 엔지니어링 (여기서 실시간으로 수정하세요)", expanded=False):
        system_prompt = st.text_area(
            "AI에게 줄 지시사항:",
            value="당신은 전문 시나리오 작가입니다. 사용자의 아이디어를 바탕으로 몰입감 넘치는 장면을 구성해 주세요."
        )
    
    user_input = st.text_area("로그라인이나 아이디어를 입력하세요.")
    
    if st.button("시나리오 생성"):
        model = genai.GenerativeModel('gemini-pro')
        # 위에서 수정한 system_prompt와 사용자의 입력을 합쳐서 보냅니다.
        full_query = f"{system_prompt}\n\n사용자 아이디어: {user_input}"
        
        with st.spinner('AI 작가가 집필 중입니다...'):
            response = model.generate_content(full_query)
            st.markdown("---")
            st.write(response.text)

elif app_mode == "스토리보드 생성기":
    st.header("🖼️ 스토리보드 프롬프트 생성")
    
    # [실시간 프롬프트 수정창]
    with st.expander("⚙️ 프롬프트 규칙 수정", expanded=False):
        system_prompt = st.text_area(
            "프롬프트 생성 규칙:",
            value="영화 감독을 위한 이미지 생성 프롬프트를 짜줘. 전문적인 촬영 용어를 사용하고 미드저니 스타일로 작성해줘."
        )
    
    scene_desc = st.text_input("장면 묘사 (예: 로봇의 탈출)")
    col1, col2 = st.columns(2)
    with col1:
        shot_size = st.selectbox("샷 사이즈", ["ECU", "CU", "MS", "WS", "FS"])
    with col2:
        lens = st.selectbox("렌즈", ["Anamorphic", "35mm", "50mm", "85mm"])
    
    if st.button("프롬프트 생성"):
        model = genai.GenerativeModel('gemini-pro')
        full_query = f"{system_prompt}\n장면: {scene_desc}, 샷: {shot_size}, 렌즈: {lens}"
        
        with st.spinner('프롬프트 생성 중...'):
            response = model.generate_content(full_query)
            st.subheader("결과 프롬프트")
            st.code(response.text)
