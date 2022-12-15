from pydoc_data.topics import topics
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

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
@st.experimental_memo
def load_data(file_name):
  df = pd.read_csv(file_name)
  return df

def load_image(image_file) :
    img = Image.open(image_file)
    return(img)

st.title('기후변화에 대해 입법부는 어떻게 대응해왔는가?')
st.markdown('---')
#law_total = load_data('https://docs.google.com/spreadsheets/d/e/2PACX-1vT6AFAcm5mv-htTPaHUlEOmTLkSoRwRGbWfvKJpB02LwPg3Q3bZ9TRAOIuGPB8LW37UVLUl_yNg3SeK/pub?gid=1079941894&single=true&output=csv')
hwang_ex = load_data('https://docs.google.com/spreadsheets/d/e/2PACX-1vT6AFAcm5mv-htTPaHUlEOmTLkSoRwRGbWfvKJpB02LwPg3Q3bZ9TRAOIuGPB8LW37UVLUl_yNg3SeK/pub?gid=1266754791&single=true&output=csv')
topic_intro = load_data('https://docs.google.com/spreadsheets/d/e/2PACX-1vTBLls-7iUW19oceb2F-zuuMaR1jcOow7OiSEeVMA5yBy2PzGtAkW876AOBUFEAolV3GZ6iQI5TICuM/pub?gid=0&single=true&output=csv')
topic_rank = load_data('https://docs.google.com/spreadsheets/d/e/2PACX-1vT6AFAcm5mv-htTPaHUlEOmTLkSoRwRGbWfvKJpB02LwPg3Q3bZ9TRAOIuGPB8LW37UVLUl_yNg3SeK/pub?gid=456523749&single=true&output=csv')
yy = load_data('https://docs.google.com/spreadsheets/d/e/2PACX-1vSoAYOiuIHUBXvfQ6xf8yBeinK-zWmGlGtVWXb336K47Q28Ke_mjwM6V2wFaHVaZvJnt6_KrkLnpRim/pub?gid=0&single=true&output=csv')
df = load_data('./data/conference_total.csv')
clstr = load_data("https://docs.google.com/spreadsheets/d/e/2PACX-1vSyoeLyhung7IUTPARDqxlb_pf3XpytIksylGeySIQfagQQRTxuUJvRrMmjhhL_zHJvkBwbYu_yI8_s/pub?gid=889562349&single=true&output=csv")
wc1 = load_image('./img/노무현green10.png')
wc2 = load_image('./img/이명박green10-1.png')
wc3 = load_image('./img/박근혜green10-1.png')
wc4 = load_image('./img/문재인green10.png')

with st.sidebar:
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
  st.markdown('''
  - 회의록 데이터 수집 방법:
    1. 공공데이터 포털 ‘국회회의록 빅데이터'에서 ‘기후', ‘탄소', ‘녹색', ‘그린' 네 가지 키워드를 포함하고 있는 16대-18대 회의록 동적크롤링, 2352개의 회의록 csv 데이터를 수집
    2. ‘그린아이넷’ 등 기후변화와 직접적으로 연관이 없는 키워드를 stop words로 지정해, 이를 포함한 발언을 삭제하는 등 데이터 클리닝 작업 진행
    3. 오픈 API를 활용해 16-18대 국회의원 정당 및 지역구를 회의록 발언데이터에 태깅함으로써, 4072개의 관찰값으로 구성된 분석 데이터를 완성
  ''')
  st.header('이렇게 분석했어요')
  st.markdown('''
  발의안에 대해서는 BERTopic을 활용해 토픽 분석을 진행했습니다. Sentence Transformer로
  임베딩 후, UMAP으로 차원 축소 후, HDBSCAN을 활용해 클러스터링하는 방법입니다. 회의록에 대해서는 위와 같은
  방법을 수행한 후, 임베딩 벡터값을 활용해 코사인 유사도를 계산했습니다. 또한, 발언의 개별 키워드를 추출하기 위해 KeyBERT를
  활용했습니다. KeyBERT는 키워드 임베딩과 문서 임베딩을 따로 계산 후 둘 사이 코사인 유사성을 계산해 해당 점수가 가장 높은
  키워드, 즉 유사한 키워드를 추출하는 방법입니다.
  ''')

if a == '1. 기후변화 관련 법안, 누가 많이 발의했나':
  st.header('기후변화 관련 법안, 누가 많이 발의했나')
  st.markdown('''
  국회는 기후변화와 관련해 어떠한 법을 제정하기 위해 노력했을까요? 이를 알아보기 위해, 노무현 정권부터 문재인 정권 내에 발의된 법안 905개를 모아 분석했습니다. 
  ''')
  st.subheader('녹색성장, 탄소중립 … 정권별 발의건수 패턴은 정권의 기조와 직결됐다')
  st.markdown('''
  발의건수를 정권별로 확인한 결과, **문재인 정권 510건, 이명박 정권 200건, 박근혜 정권 152건, 노무현 정권 29건 순**으로 발의 건수가 높았습니다. 이는 **문재인 정권의 ‘탄소중립’, 이명박 정권의 ‘녹색성장’ 기조가 반영된 결과**라고 해석할 수 있습니다. \n\n
  ''')
  yy['age'] = [16,16,20,20,18,18,17,17]
  yy = yy.sort_values(by='age')

  fig00 = px.histogram(yy, x="pres", y="sum",
              color='yeoya', barmode='group',
              height=400).update_layout(xaxis_title="정권", yaxis_title="정권별 발의건수", 
                                        yaxis = dict(
                                            tickmode = 'linear',
                                            tick0 = 0,
                                            dtick = 100
      ))
  st.plotly_chart(fig00, use_container_width=True)
  st.markdown('''
  흥미로운 것은 정권별 여당 야당의 발의건수 패턴입니다. **박근혜 정권을 제외하고는, 여당이 기후변화에 대한 법적 논의를 견인한 것**을 확인할 수 있었습니다. 일반적으로, 진보 성향의 정당이 기후변화 관련 법안을 많이 발의할 것이라는 통념과 달리, 이명박 정부에서는 여당이었던 한나라당(79건)과 새누리당(32건)이 많은 법안을 발의했습니다.  즉, 국회가 독립적으로 기후변화에 대한 논의를 전개하기보다는, 정부의 정책기조를 따라가는 패턴이 발견되었습니다. 박근혜 정권의 경우, [이명박 정부에서 추진되었던 녹색성장 정책을 지우려한]([https://www.pressian.com/pages/articles/64964](https://www.pressian.com/pages/articles/64964)) 것과 연관이 있다고 해석할 수 있습니다. 실제로, [박근혜 정부의 환경·에너지 정책은 학계와 시민사회단체 전문가 평가에서 5점 만점에 1.48점의 낙제점]([https://www.hani.co.kr/arti/society/environment/783696.html](https://www.hani.co.kr/arti/society/environment/783696.html))을 받았으며, 녹색성장위원회는 대통령 소속에서 국무총리 산하로 위상이 격하되었습니다. 문재인 정권에서는 진보성향의 여당인 더불어민주당이 315건으로, 뒤를 잇는 국민의힘(65건), 새누리당(54건)에 비해 압도적으로 많은 발의를 했습니다.
  ''')

  st.subheader('발의를 많이한 의원이 기후변화에 많은 관심? 발의 내용이 중요')
  st.markdown('''
  우리는 흔히 기후변화에 관심을 많이 가지는 의원이 많이 발의할 것을 기대합니다. 그러나 분석 결과, 발의량이 기후변화 관심도의 바로미터라고 보기 어렵다는 해석이 나왔습니다. 국회 대수별로 발의를 많이한 의원을 확인한 결과, 19대 김동철 의원(민주통합당), 20대 황주홍 의원(국민의당) 그리고 21대 허영 의원(더불어민주당)이 각각 8건, 20건, 13건으로 가장 많이 발의했습니다. \n\n
  ''')
  st.dataframe(hwang_ex)
  st.text('21대 황주홍의원의 발의안. 주요 제안이유 셀을 더블클릭하면 내용 전체를 확인할 수 있습니다.')
  st.markdown('')

  st.markdown('''
  그러나 발의안을 실제로 살펴본 결과, **김동철 의원과 황주홍 의원의 많은 발의안은 하나의 주제**만을 가리키고 있었습니다. 김동철 의원은 전기자동차 관련 세금 및 통행료 감면이 필요하다는 맥락에서 여러 법률안을 발의했습니다. 황주홍 의원은 농어촌지역의 기후변화로 인한 농작물 작황 부진을 고려해 조세특례를 지속해야한다는 맥락에서 조세특례제한법 일부개정법률안 등을 여러 차례 발의했습니다. 허영 의원의 경우, 논의의 결이 조금 달라집니다. 기후변화인지 예·결산제도 관련 법안을 많이 발의하였지만, 그린리모델링 사업, 국가정원 확충 등의 온실가스 감축과 관련된 법안 역시 많이 발의하였다는 점에서 차이가 있습니다. \n\n
  이외에도 발의안 소관 상임위원회별 발의건수를 확인한 결과,  환경노동위원회(181건), 국토교통위원회 (101건), 기획재정위원회(99건)가 상위 결과에 속했습니다. 
  ''')
  st.subheader('대부분의 법안 계류 -> 폐기의 수순을 거쳐, 다만 21대 국회 본회의 상정 안건 증가')
  st.markdown('''
  전체 905건의 의안 중 307건이 임기만료 폐기를 맞이하였고, 현재 21대 국회에서는 223건이 계류 중입니다 본회의 상정 안건은 전체 안건 중 **9.6%에 그쳤습니다**. 다만, 법률안이 계류 후 폐기를 맞이하는 것은 [전반적인 의안에 대한 국회의 고질적 문제](https://m.lawtimes.co.kr/Content/Article?serial=161691)이기 때문에, ‘기후변화’ 발의안에 한정해 나타나는 패턴이라고 보기에는 어렵습니다. 하지만, 21대 국회는 현재 진행 중임을 고려할 때, 최근 국회로 올수록 본회의에 상정되는 안건이 증가하는 추세입니다. 
  ''')

if a == '2. 전기자동차부터 탄소 배출량 감축까지':
  st.header('2. 전기자동차부터 탄소 배출량 감축까지')
  st.markdown('''
  지난 챕터까지 발의건수에 집중에 살펴보았다면, 이제 본격적으로 어떤 내용의 발의안이 많이 나왔나 살펴보려합니다. 이를 위해 의안별 ‘제안이유 및 주요내용’을 Sentence transformer을 활용해 임베딩하여 거리가 가까운 발언들끼리 클러스터로 묶어주었습니다. 토픽 클러스터는 다음과 같습니다.
  ''')
  st.dataframe(topic_intro)
  st.markdown('''
  문재인 정권 때 압도적으로 발의안 수가 많았기 때문에, 대부분의 주제들이 박근혜 정권 때 소폭 감소하고 문재인 정권 때 큰 폭의 상승을 보였습니다. (노무현 정권 발의안이 29건으로 다른 정권에 비해 현저히 적기 때문에, 이번 분석에서는 제외합니다.) 주제 클러스터별로, 발의 추이를 살펴본 결과 몇가지 흥미로운 결과를 찾아볼 수 있었습니다. 
  ''')

  st.subheader('폭염, 폭우, 가뭄 … 모든 정권이 법적 대책을 고민해')
  topic_rank_1 = topic_rank[(topic_rank['content_topic'] == 2) | (topic_rank['content_topic'] == 3)]
  fig_rank_1 = px.line(topic_rank_1,x='pres',y='count',facet_col='content_topic', facet_col_wrap=2, markers=True,width=900)
  fig_rank_1.update_layout(font_family="Pretendard",xaxis_title='발의건수', yaxis_title='',margin_pad=10)
  fig_rank_1.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
  st.plotly_chart(fig_rank_1)
  st.markdown('''
  각 정권 상위권 토픽(3위 이내)에 2번 이상 랭킹된 주제를 분석한 결과, 폭우, 가뭄 피해 대책 관련 의안(2번)이  박근혜 정권에서 3위, 이명박 정권에서 2위를 차지하였고, 폭염 대책 관련 의안(3번)이 각각이명박 정권에서 3위, 문재인 정권에서 3위를 차지한 것을 밝혀냈습니다. 즉, 폭염 그리고 폭우, 가뭄에 대해 모든 정권이 법적인 예방 내지 해결책을 도모하였다고 해석할 수 있습니다. 특히, 문재인 정권에서는 3번 주제 클러스터에 기후보건건강영향평가, 기후변화 인지 예결산 제도 관련 법안 발의가 추가된 것이 특징입니다. 
  ''')


  st.subheader('이명박 정부 당시 국회의 핵심 논의는 친환경 교통 수단 중심')
  topic_rank_2 = topic_rank[(topic_rank['content_topic'] == 1) | (topic_rank['content_topic'] == 6)| (topic_rank['content_topic'] == 10)]
  fig_rank_2 = px.line(topic_rank_2,x='pres',y='count',facet_col='content_topic', facet_col_wrap=3, markers=True,width=900)
  fig_rank_2.update_layout(font_family="Pretendard",xaxis_title='발의건수', yaxis_title='',margin_pad=10)
  fig_rank_2.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
  st.plotly_chart(fig_rank_2)
  st.markdown('''
  이명박 정권은 ‘녹색성장’을 핵심 정책으로 내세운 정부이기 때문에, 특히 주목해서 볼 필요가 있습니다. 이명박 정부에서 발의한 기후변화 발의안 중, 가장 많은 주제를 차지한 것은 ‘전기자동차’(1번)였습니다. 해당 정권 때 특히 하이브리드 차량, 전기자동차 관련 법안을 마련하고자 하는 움직임이 컸음을 알 수 있습니다. 실제로 이명박 정부는 [청와대에서 전기자동차 시승을 진행](https://www.ytn.co.kr/_ln/0101_201009091604133712)하는 등 전기자동차에 대한 큰 관심을 보였습니다. 박근혜 정부에서 관련 의안 발의가 감소한 후, 문재인 정권 때 다시 증가해 4위 토픽으로 부상했습니다. 이어, 이명박 정권에서 관심을 가진 주제는 ‘산림 보호 및 임업 지원’으로, 관련하여 21건의 법률안이 발의되었습니다. 
  ''')
  st.markdown('''
  이명박 정권 이후 꾸준히 감소한 주제도 있었습니다. 바로 10번, 저탄소 친환경 대중 교통 수단을 다룬 법안 클러스터였습니다. 저탄소 녹색성장의 교통수단 ‘노면전차’를 도입하자는 목소리와 자전거 이용 및 자전거 산업을 활성화하자는 움직임과 맞물려 등장했습니다. 특히, [자전거 도로는 이명박 정부의 핵심 사업이었던 만큼](https://www.hankyung.com/society/article/2017052271297) 정부의 핵심 사업이 법안 발의에 큰 영향을 주었음을 시사합니다. 
  ''')

  st.subheader('탄소 배출량 감축, 문재인 정부 들어 본격 논의 시작')
  topic_rank_3 = topic_rank[(topic_rank['content_topic'] == 0) | (topic_rank['content_topic'] == 4)| (topic_rank['content_topic'] == 13)| (topic_rank['content_topic'] == 15) | (topic_rank['content_topic'] == 16)]
  fig_rank_3 = px.line(topic_rank_3,x='pres',y='count',facet_col='content_topic', facet_col_wrap=3, markers=True,width=900,height=600)
  fig_rank_3.update_layout(font_family="Pretendard",xaxis_title='발의건수', yaxis_title='',margin_pad=10)
  fig_rank_3.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
  st.plotly_chart(fig_rank_3)
  st.markdown('''
  문재인 정부 들어 기후변화 관련 발의가 대폭 증가한 것은 사실입니다. 그러나, 특히 전 정권 대비 새로 등장한 토픽, 또는 증가율이 높은 주제의 의안에는 무엇이 있을까요? 이를 알아보기 위해, 박근혜 정권 대비 증가율 500% 이상인 동시에 이명박 정권 대비 증가율 100% 이상인 주제를 추려보았습니다. 
  ''')
  st.markdown('''
  우선 온실가스 감축을 다룬 의안들(0번)이 압도적으로 많이 증가한 것을 확인할 수 있었습니다. 전 정권에서, 2건 → 7건 → 9건에 머물렀던 의안 수는 문재인 정부에서 57건으로 큰 상승폭을 그리며 문정부 전체 기후변화 의안 주제 중 1위를 달성했습니다. 즉, 온실가스, 특히 탄소 배출 저감에 대한 본격적인 법적 논의가 진행되었음을 알 수 있습니다. 더불어, 문정부에서 강조한 ‘탄소중립’과도 큰 연관이 있어보입니다. 이처럼 정부의 정책과 연관이 있는 토픽 클러스터를 더 확인해 볼 수 있습니다. 수소경제 관련 의안(21건, 15번)과 탄소중립에 따른 일자리 전환 대응 관련 의안(20건, 16번)은 전 정권에서 등장하지 않았던, 혹은 1건 이하로 등장했던 주제입니다. 이는 문정부가 수소경제와 그린 뉴딜 사업을 강조했던 것의 연장선이라고 보여집니다.  
  ''')
  st.markdown('''
  신재생 에너지 관련 의안(39건, 4번)과 기후변화에 따른 농어업 부진에 대한 대책(26건, 13번)을 다룬 의안 수도 증가했습니다. 다만, 후자의 토픽은 앞선 챕터에서 다룬 황주홍 의원(전남 고흥군보성군장흥군강진군)이 19건 발의했다는 점을 고려해야합니다. 
  ''')



if a == '3. 회의록 분석':
  st.header('3. 회의록 분석')
  st.subheader("정권별로 기후 변화 관련 **키워드**는 어떻게 달라질까?")
  st.markdown("분석 결과 정권별 키워드는 크게 기후변화 혹은 대응과 같은 단순 관련 단어, 기후변화협약이나 탄소배출권과 같이 **국제 사회 의제**와 관련된 분류, 녹색성장이나 탄소중립과 같이 **정부 차원의 대응 전략**에 관련된 분류로 나뉘었습니다. 각 정권별로 노무현 정권에서는 **기후변화협약**, 이명박 정권에서는 **녹색성장**, 박근혜 정권에서는 **탄소배출권**, 문재인 정권에서는 **탄소중립**이 중요하게 언급됐다. 단순히 대응, 변화가 키워드인 노무현, 박근혜 정부에 비해 이명박, 문재인 정부에서 특징적인 키워드가 더 많이 나타났습니다.")
  multi_select = st.multiselect('정권별 기후 변화 키워드 확인하기',
                              ['노무현', '이명박', '박근혜', '문재인'],
                              default = ['노무현', '이명박', '박근혜', '문재인'])
  col1,col2,col3,col4= st.columns(4)
  if '노무현' in multi_select:
    col1.image(wc1, caption = '노무현 정권 회의록')
  if '이명박' in multi_select:
    col2.image(wc2, caption = '이명박 정권 회의록')
  if '박근혜' in multi_select:
    col3.image(wc3, caption = '박근혜 정권 회의록')
  if '문재인' in multi_select:
    col4.image(wc4, caption = '문재인 정권 회의록')
  st.markdown('''
  환경 관련 이슈가 국회에서 가장 많이 논의되었던 시기는 21대, 18대였습니다. 또한 회의록 전체 발언의 48%는 보수성향의 의원들로부터, 46%는 진보성향의 의원들로부터 나오고 있었는데요, 정치 성향에 따라 관심을 가지는 토픽은 다를 수 있지만, 보수와 진보 모두 비슷한 수준으로 환경 이슈에 목소리를 내고 있다고 평가할 수 있습니다. 국회 대수, 의원의 정치성향 뿐만 아니라 당시 임기 대통령, 다수당 여부, 여당 여부 등이 국회 발언 수에 영향을 미치는 변수였는데, 이는 OLS(최소자승법) 분석 결과 중 P-Value가 0.05 이하임을 통해 확인할 수 있었습니다.
  ''')
  ##### 회의록 클러스터

  st.subheader("전지적 관찰자 시점: 클러스터링으로 바라본 환경/기후변화 토픽")
  st.markdown('''
  이러한 변수들에 따라 의원들이 관심을 가지는 토픽이 달라지기도 했습니다. 먼저 아래쪽에 보이는 그림은 회의록의 발언들을 클러스터링 해, 그 벡터값을 2차원 평면에 매핑한 그래프입니다. 각 점들은 각각의 발언을, 그 위에 입혀진 색깔은 해당 발언이 속한 토픽 클러스터를 의미합니다. 
  ''')
  # scatter plot
  fig = px.scatter(clstr, x =  "x" , y = "y", color="labels", hover_data=["labels","doc"], 
                  opacity=0.5,
                  width=800,height=600,
                  color_continuous_scale="inferno")
  fig.update_traces(marker_size=5)
  fig.update_layout(
      hovermode="closest",
                    hoverlabel=dict(bgcolor="white", font_size=10))
  st.plotly_chart(fig, use_container_width=True)

  st.markdown('''
  여기서 재미있는 지점은, 12번과 13번 클러스터의 경우, 발언들이 모두 ‘탄소중립'이라는 큰 키워드 아래 묶여있지만 클러스터 자체가 가지고 있는 특징은 상당히 다른 양상을 띠고 있다는 것입니다. 12번 토픽은 문재인 대통령 임기 시절에 논의가 주로 이루어진 진보진영의 의제이며, 이와 반대로 13번 토픽은 이명박 대통령 시절의 보수진영 의제입니다. 각 클러스터에 속해있는 발언들을 자세히 들여다보면, 두 클러스터는 탄소중립 문제를 서로 다른 시각에서 바라보고 있다는 것 또한 확인할 수 있습니다. 각 클러스터를 Kebert를 활용해 키워드 분석해 본 결과, 12번 토픽의 키워드는 ‘온실가스 감축', ‘기후변화협약' 등 기후변화 방지 대책과 관련된 내용들이었던 반면, 13번 토픽은 ‘탄소배출권', ‘탄소 시장' 등에 관해 에너지 관세 및 정책 차원에서의 논의였습니다.
  ''')


  ##### 히트맵
  st.subheader("코사인 유사도로 집권 대통령, 정당별 논의 특징 알아보기")
  st.markdown('''
  좀 더 거시적인 관점에서 환경 및 기후변화와 관련한 15개의 토픽에 대해 의원들이 어떤 방식으로 논의해왔는지 확인해보기 위해, 같은 토픽 안에 있는 발언들 간의 코사인 유사도를 살펴볼 수도 있습니다. 코사인 유사도란, 쉽게 얘기하면 각 발언들이 서로 같은 방향을 향해있는지, 반대의 방향을 바라보고 있는지를 보여주는 지표입니다. 유사도가 1에 가까울수록 의원들이 같은 방향으로 논의를 진전해나가고 있다고 해석할 수 있고, -1에 가까울수록 특정 토픽에 대해 대립되는 의견들이 많이 존재하다고 볼 수 있습니다. 같은 클러스터 안에 있는 발언들 간의 코사인 유사도를 분석한 후, 정당 정권별로 평균을 내본 그래프가 아래에 있습니다.
  ''')
  # 데이터 불러오기
  pres = np.load('./data/cos_pres_arr.npy', allow_pickle=True)
  politic = np.load('./data/cos_politic_arr.npy', allow_pickle=True)
  # 정권별
  president = ['노무현','이명박','박근혜','문재인']
  topic_list = ['토픽 0','토픽 1','토픽 2','토픽 3','토픽 4','토픽 5','토픽 6','토픽 7','토픽 8','토픽 9','토픽 10','토픽 11','토픽 12','토픽 13','토픽 14']
  trace = go.Heatmap(
    x = president,
    y = topic_list,
    z = pres,
    type = 'heatmap'
  )
  data= [trace]
  fig2 = go.Figure(data = data)
  st.plotly_chart(fig2, use_container_width=True)
  st.markdown('''
  앞서 얘기했던 12번째, 13번째 토픽에 대해서는 코사인 유사도가 상대적으로 높게 나타났는데, 그 이유는 정치적인 맥락에 따라 다양하게 해석될 수 있습니다. 이명박 대통령은 4대강 사업의 실패 이후 환경과 관련한 비판을 마주했고, 그 상황을 타개하기 위한 정치적인 전략을 모색했습니다. 이러한 관점에서 볼 때, 당시 여당이었던 보수정당을 중심으로 탄소중립 논의가 활발해진 것은, 이러한 전략을 소구하기 위한 한 과정이었다고 해석할 수 있을 것입니다. 문재인 대통령 시기 12번째 토픽의 경우에도 코사인 유사도가 상대적으로 높게 나타났는데, 문재인 대통령은 집권과 함께 국무회의에서 ‘기후위기 대응을 위한 탄소중립, 녹색성장 기본법'을 시행했습니다. 주요 정치 공약이었던만큼, 해당 의제를 관철시키기 위한 정치적인 과정에서 마찬가지로 여당 중심으로 국회 논의가 이루어졌다고 평가할 수 있습니다.
  ''')

  # 정당별
  party = ['보수','진보','기타']
  topic_list = ['토픽 0','토픽 1','토픽 2','토픽 3','토픽 4','토픽 5','토픽 6','토픽 7','토픽 8','토픽 9','토픽 10','토픽 11','토픽 12','토픽 13','토픽 14']
  trace = go.Heatmap(
    x = party,
    y = topic_list,
    z = politic,
    type = 'heatmap'  
  )
  data= [trace]
  fig3 = go.Figure(data = data)
  st.plotly_chart(fig3, use_container_width=True)
  st.markdown('''
  정당별 국회 회의록 발언의 코사인 유사도에서는 유의미한 결과를 발견하진 못했지만, 토픽별 발언의 유사도를 분석할 때보다 토픽-정당별로 유사도를 분석할 때 값이 더 낮아진다는 것을 알 수 있었습니다. 정치 성향이 같아도, 기후변화/환경 관련 서로 다른 토픽에 대해 다양한 방향의 의견을 개진하고 있다고도 볼 수 있을 것입니다.
  ''')

  st.write("**[데이터셋]**")
  if st.button("회의록 데이터 확인하기"):
        st.info(
          """
          출처: <국회회의록 빅데이터> (https://dataset.nanet.go.kr/)
          """)
        st.dataframe(df.head(5))