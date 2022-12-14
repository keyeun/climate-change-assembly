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

with open('./css/style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def load_data(file_name):
  df = pd.read_csv(file_name)
  return df
st.title('기후변화에 대해 입법부는 어떻게 대응해왔는가?')
st.markdown('---')
law_total = load_data('https://docs.google.com/spreadsheets/d/e/2PACX-1vT6AFAcm5mv-htTPaHUlEOmTLkSoRwRGbWfvKJpB02LwPg3Q3bZ9TRAOIuGPB8LW37UVLUl_yNg3SeK/pub?gid=1079941894&single=true&output=csv')
topic_intro = load_data('https://docs.google.com/spreadsheets/d/e/2PACX-1vTBLls-7iUW19oceb2F-zuuMaR1jcOow7OiSEeVMA5yBy2PzGtAkW876AOBUFEAolV3GZ6iQI5TICuM/pub?gid=0&single=true&output=csv')

with st.sidebar:
    #a = st.selectbox('카테고리', ('소개','구글/트위터 인기 검색 키워드','온라인 커뮤니티 인기 게시물', '오늘의 주요 키워드 랭킹'))
    a = option_menu('카테고리', ['소개','1. 기후변화 관련 법안, 누가 많이 발의했나','2. 전기자동차부터 탄소 배출량 감축까지','3. 회의록 분석'],styles={"nav-link-selected": {"background-color": "#1C261F"}})
    st.markdown('---')
    st.markdown(
        '''
            <style>
                .css-1adrfps.e1fqkh3o2 {
                    width: 400px;
                }
                .css-1wf22gv.e1fqkh3o2 {
                    width: 400px;
                    margin-left: -400px;
                }
            </style>
        ''',
        unsafe_allow_html=True
    )

if a == '소개':
  st.header('프로젝트 시작 동기')

  st.header('이렇게 수집했어요')
  st.markdown('''
  - 발의안 데이터 수집 방법:
    1. 의안정보시스템 - **제안이유 검색 결과**로 1차 BillId 크롤링
    2. 의안정보시스템 - BillId로 제안이유 2차 크롤링 - 의안 정보
    3. 국회의원 발의법률안 API -  기타 meta data 3차 크롤링
  ''')
  st.header('이렇게 분석했어요')


if a == '1. 기후변화 관련 법안, 누가 많이 발의했나':
  st.header('기후변화 관련 법안, 누가 많이 발의했나')
  st.markdown('''
  국회는 기후변화와 관련해 어떠한 법을 제정하기 위해 노력했을까요? 이를 알아보기 위해, 노무현 정권부터 문재인 정권 내에 발의된 법안 905개를 모아 분석했습니다. 
  ''')
  st.subheader('녹색성장, 탄소중립 … 정권별 발의건수 패턴은 정권의 기조와 직결됐다')
  st.markdown('''
  발의건수를 정권별로 확인한 결과, 문재인 정권 510건, 이명박 정권 200건, 박근혜 정권 152건, 노무현 정권 29건 순으로 발의 건수가 높았습니다. 이는 **문재인 정권의 ‘탄소중립’, 이명박 정권의 ‘녹색성장’ 기조가 반영된 결과**라고 해석할 수 있습니다. \n\n

흥미로운 것은 정권별 여당 야당의 발의건수 패턴입니다. 박근혜 정권을 제외하고는, 여당이 기후변화에 대한 법적 논의를 견인한 것을 확인할 수 있었습니다. 일반적으로, 진보 성향의 정당이 기후변화 관련 법안을 많이 발의할 것이라는 통념과 달리, 이명박 정부에서는 여당이었던 한나라당(79건)과 새누리당(32건)이 많은 법안을 발의했습니다.  즉, 국회가 독립적으로 기후변화에 대한 논의를 전개하기보다는, 정부의 정책기조를 따라가는 패턴이 발견되었습니다. 박근혜 정권의 경우, [이명박 정부에서 추진되었던 녹색성장 정책을 지우려한]([https://www.pressian.com/pages/articles/64964](https://www.pressian.com/pages/articles/64964)) 것과 연관이 있다고 해석할 수 있습니다. 실제로, [박근혜 정부의 환경·에너지 정책은 학계와 시민사회단체 전문가 평가에서 5점 만점에 1.48점의 낙제점]([https://www.hani.co.kr/arti/society/environment/783696.html](https://www.hani.co.kr/arti/society/environment/783696.html))을 받았으며, 녹색성장위원회는 대통령 소속에서 국무총리 산하로 위상이 격하되었습니다. 문재인 정권에서는 진보성향의 여당인 더불어민주당이 315건으로, 뒤를 잇는 국민의힘(65건), 새누리당(54건)에 비해 압도적으로 많은 발의를 했습니다.
  ''')

  st.subheader('발의를 많이한 의원이 기후변화에 많은 관심? 발의 내용이 중요')
  st.markdown('''
  우리는 흔히 기후변화에 관심을 많이 가지는 의원이 많이 발의할 것을 기대합니다. 그러나 분석 결과, 발의량이 기후변화 관심도의 바로미터라고 보기 어렵다는 해석이 나왔습니다. 국회 대수별로 발의를 많이한 의원을 확인한 결과, **19대 김동철 의원(민주통합당), 20대 황주홍 의원(국민의당) 그리고 21대 허영 의원(더불어민주당)**이 각각 8건, 20건, 13건으로 가장 많이 발의했습니다. \n\n

  그러나 발의안을 실제로 살펴본 결과, 김동철 의원과 황주홍 의원의 많은 발의안은 하나의 주제만을 가리키고 있었습니다. 김동철 의원은 전기자동차 관련 세금 및 통행료 감면이 필요하다는 맥락에서 다양한 법률안을 발의했습니다. 황주홍 의원은 농어촌지역의 기후변화로 인한 농작물 작황 부진을 고려해 조세특례를 지속해야한다는 맥락에서 조세특례제한법 일부개정법률안 등을 여러 차례 발의했습니다. 허영 의원의 경우, 논의의 결이 조금 달라집니다. 기후변화인지 예·결산제도 관련 법안을 많이 발의하였지만, 그린리모델링 사업, 국가정원 확충 등의 온실가스 감축과 관련된 법안 역시 많이 발의하였다는 점에서 차이가 있습니다. \n\n
  이외에도 발의안 소관 상임위원회별 발의건수를 확인한 결과,  환경노동위원회(181건), 국토교통위원회 (101건), 기획재정위원회(99건)가 상위 결과에 속했습니다. 
  ''')

if a == '2. 전기자동차부터 탄소 배출량 감축까지':
  st.header('2. 전기자동차부터 탄소 배출량 감축까지')


if a == '3. 회의록 분석':
  st.header('3. 회의록 분석')