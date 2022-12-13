import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import os
import plotly.express as px
from st_aggrid import JsCode,GridOptionsBuilder
from st_aggrid import AgGrid

st.set_page_config(
    page_title="기후변화 관련 입법부 대응 현황 분석",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': '2022년 2학기 데이터저널리즘 수업 1조 최종 과제 결과물입니다.',
    }
)

streamlit_style = """
			<style>
			@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
🏛️
			html, body, [class*="css"],g {
			  font-family: Pretendard, -apple-system, BlinkMacSystemFont, system-ui, Roboto, 'Helvetica Neue', 'Segoe UI', 'Apple SD Gothic Neo', 'Noto Sans KR', 'Malgun Gothic', sans-serif;
      }
			</style>
			"""
st.markdown(streamlit_style, unsafe_allow_html=True)

st.title('기후변화에 대해 입법부는 어떻게 대응해왔는가?')
st.markdown('---')

with st.sidebar:
    #a = st.selectbox('카테고리', ('소개','구글/트위터 인기 검색 키워드','온라인 커뮤니티 인기 게시물', '오늘의 주요 키워드 랭킹'))
    a = option_menu('카테고리', ['소개','1. 발의안 분석','2. 회의록 분석'],styles={"nav-link-selected": {"background-color": "#4BBBEE"}})
    st.markdown('---')
    st.markdown(
        '''
            <style>
                .css-1adrfps.e1fqkh3o2 {
                    width: 500px;
                }
                .css-1wf22gv.e1fqkh3o2 {
                    width: 500px;
                    margin-left: -500px;
                }
            </style>
        ''',
        unsafe_allow_html=True
    )

if a == '소개':
  st.header('프로젝트 시작 동기')

if a == '1. 발의안 분석':
  st.header('프로젝트 시작 동기')

if a == '2. 회의록 분석':
  st.header('프로젝트 시작 동기')

@st.cache(ttl=60*60)
def load_data(file_name):
  df = pd.read_csv(file_name)
  return df