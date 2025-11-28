import os
import json
import time
import pandas as pd
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# --------------------------------------------------------------------------
# 1. 초기 설정 및 환경 변수 로드
# --------------------------------------------------------------------------
load_dotenv()

st.set_page_config(
    page_title="Community Insight Bot",
    page_icon="🕵️‍♂️",
    layout="wide"
)

# 새로운 모듈 임포트 (Stage 1 요구사항)
try:
    from src.crawler_wrapper import search_community
    from src.preprocessor import filter_hate_speech
except ImportError as e:
    st.error(f"필수 모듈을 임포트하는 중 오류가 발생했습니다: {e}")
    st.stop()

# --------------------------------------------------------------------------
# 2. 사이드바 설정 (커뮤니티 선택 제거, API 키 확인 유지)
# --------------------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ 설정")
    
    # API 키 및 모델 설정 확인 (기존 로직 유지)
    if not os.getenv("API_KEY"):
        st.error("🚨 API 키가 설정되지 않았습니다. .env 파일을 확인해주세요.")
    
    if not os.getenv("MODEL"):
        st.warning("⚠️ 모델이 설정되지 않았습니다. .env 파일을 확인해주세요.")
        
    st.info("AI가 사용자의 질문을 분석하여 자동으로 커뮤니티(DC/Arca)를 선정하고 데이터를 수집합니다.")
    st.markdown("---")
    st.caption("Powered by Google Gemini")

# --------------------------------------------------------------------------
# 3. Gemini 모델 로드 (기존 로직 유지)
# --------------------------------------------------------------------------
@st.cache_resource
def get_gemini_model():
    """
    Gemini 모델을 로드합니다. 
    st.cache_resource를 사용하여 세션 간 모델 객체를 공유합니다.
    """
    YOUR_API_KEY = os.getenv("API_KEY")
    if not YOUR_API_KEY:
        st.error("🚨 API 키가 설정되지 않았습니다. .env 파일을 확인해주세요.")
        st.stop()

    YOUR_MODEL = os.getenv("MODEL")
    if not YOUR_MODEL:
        st.error("모델이 설정되지 않았습니다. '.env' 파일에 'MODEL'을 설정해주세요.")
        st.stop()
        
    genai.configure(api_key=YOUR_API_KEY)
    
    # 안전 설정: 모든 카테고리에 대해 차단 없음(BLOCK_NONE)으로 설정하여 오탐지 방지
    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_NONE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_NONE"
        },
    ]
    
    return genai.GenerativeModel(YOUR_MODEL, safety_settings=safety_settings)

# --------------------------------------------------------------------------
# 4. 메인 로직 (Stage 2에서 구현 예정)
# --------------------------------------------------------------------------
st.title("🕵️‍♂️ Community Insight Bot (AI Auto-Mode)")
st.caption("AI가 자동으로 커뮤니티를 선정하고 여론을 분석합니다.")

if "messages" not in st.session_state:
    st.session_state.messages = []
    welcome_msg = "안녕하세요! 궁금한 게임, 인물, 이슈 등을 물어봐주세요. 제가 알아서 적절한 커뮤니티를 찾아 분석해드릴게요."
    st.session_state.messages.append({"role": "assistant", "content": welcome_msg})

for message in st.session_state.messages:
    avatar_img = "assets/purple_avatar.png" if message["role"] == "assistant" else None
    with st.chat_message(message["role"], avatar=avatar_img):
        st.markdown(message["content"])

# 사용자 입력 대기 (로직은 비워둠)
if prompt := st.chat_input("무엇을 분석해 드릴까요?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    st.info("🚧 [Stage 1] 현재 기본 설정만 완료되었습니다. 다음 단계에서 분석 로직이 구현될 예정입니다.")