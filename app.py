import os
import streamlit as st
import streamlit.components.v1 as components

# 1. Streamlit 페이지 기본 설정 (와이드 모드)
st.set_page_config(
    page_title="Interactive AI Tutor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. HTML 파일 경로 설정 (htmls/index.html)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.join(BASE_DIR, "htmls", "index.html")

# 3. HTML 파일 읽기 및 안전한 렌더링
if os.path.exists(HTML_PATH):
    with open(HTML_PATH, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # st.markdown(unsafe_html=True) 대신 components.html 사용
    # height를 충분히 크게 확보하여 깔끔하게 표시
    components.html(html_content, height=950, scrolling=True)
else:
    st.error(f"❌ HTML 파일을 찾을 수 없습니다. 경로를 확인해주세요: `{HTML_PATH}`")
