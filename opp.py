import streamlit as st
import google.generativeai as genai

# 1. 사이드바 메뉴 설정
st.sidebar.title("🎬 AI Studio 작업실")
app_mode = st.sidebar.selectbox("앱 선택", ["시나리오 어시스턴트", "스토리보드 생성기"])

# 2. API 키 연결 (Streamlit 비밀설정에서 가져옴)
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    st.error("API 키 설정이 필요합니다.")

# 3. 각 앱의 기능 구현
if app_mode == "시나리오 어시스턴트":
    st.header("✍️ 시나리오 어시스턴트")
    user_input = st.text_area("로그라인이나 아이디어를 입력하세요.")
    if st.button("시나리오 확장하기"):
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(f"시나리오 작가로서 다음 내용을 확장해줘: {user_input}")
        st.write(response.text)

elif app_mode == "스토리보드 생성기":
    st.header("🖼️ 스토리보드 프롬프트 생성")
    scene_desc = st.text_input("어떤 장면인가요? (예: 로봇이 도망치는 장면)")
    shot_size = st.selectbox("샷 사이즈", ["ECU", "CU", "MS", "WS", "FS"])
    lens = st.selectbox("렌즈", ["Anamorphic", "35mm", "50mm"])
    
    if st.button("프롬프트 생성"):
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"영화 감독을 위한 이미지 생성 프롬프트를 짜줘. 장면: {scene_desc}, 샷: {shot_size}, 렌즈: {lens}"
        response = model.generate_content(prompt)
        st.code(response.text) # 복사하기 편하도록 코드로 출력
