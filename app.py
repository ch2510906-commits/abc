import os
import streamlit as st
import streamlit.components.v1 as components

# 1. Streamlit 페이지 기본 설정
st.set_page_config(
    page_title="Interactive AI Tutor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Streamlit 기본 여백 제거 및 UI 깔끔하게 스타일링
# CSS 문자열이 파이썬 문법과 충돌하지 않도록 triple quotes(""" """) 내부로 안전하게 처리
st.markdown("""
    <style>
        /* Streamlit 기본 여백 제거 */
        .block-container {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            padding-left: 0rem !important;
            padding-right: 0rem !important;
            max-width: 100% !important;
        }
        
        /* 상단 헤더, 푸터, 메뉴 숨기기 */
        header {visibility: hidden;}
        footer {visibility: hidden;}
        #MainMenu {visibility: hidden;}
        
        /* 커스텀 스크롤바 디자인 (오류가 났던 CSS 속성 부분) */
        ::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        ::-webkit-scrollbar-thumb {
            background: #cbd5e1;
            border-radius: 3px;
        }
        
        /* iframe 전체 화면 꽉 차게 설정 */
        iframe {
            width: 100% !important;
            height: 100vh !important;
            border: none !important;
        }
    </style>
""", unsafe_html=True)

# 3. HTML 파일 경로 설정 (htmls/index.html)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.join(BASE_DIR, "htmls", "index.html")

# 4. HTML 파일 읽기 및 렌더링
if os.path.exists(HTML_PATH):
    with open(HTML_PATH, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # Streamlit에 HTML 렌더링
    components.html(html_content, height=1000, scrolling=True)
else:
    st.error(f"❌ HTML 파일을 찾을 수 없습니다. 파일 경로를 확인해주세요: `{HTML_PATH}`")
