import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import plotly.colors

# 1. 데이터 불러오기
# 파일이 같은 경로에 있다고 가정합니다.
try:
    df = pd.read_csv('PeriodicTable_0509.CSV', encoding='cp949')
    #df = pd.read_csv(r'D:\OneDrive\Data_ML\PeriodicTable\Data_in\periodictable_0509.CSV', encoding='cp949')

except FileNotFoundError:
    st.error("파일을 찾을 수 없습니다. 파일명을 확인해주세요.")
    st.stop()

# 2. 웹 화면 설정
st.set_page_config(page_title="3D Periodic Table Viz", layout="wide")
st.title("🧪 원소 성질 3D 시각화 도구")
st.markdown("주기율표의 성질을 3D 막대 그래프로 확인해보세요. 높이와 색상이 해당 성질의 세기를 나타냅니다. (coded by 김형민/정다민)")

column_to_viz = st.selectbox("시각화할 성질을 선택하세요", 
                             ['원자반지름(A)', '표준환원전위', '1차 이온화에너지', '전기음성도'])

# 데이터 전처리: 결측치는 0으로 처리하고 숫자형으로 변환
df[column_to_viz] = pd.to_numeric(df[column_to_viz], errors='coerce').fillna(0)

# 색상 매핑을 위한 정규화 (0~1 사이 값으로 변환)
min_val = df[column_to_viz].min()
max_val = df[column_to_viz].max()

def get_color(val, min_v, max_v):
    # 값이 모두 같을 경우 예외 처리
    if max_v == min_v:
        return "royalblue"
    # 0~1 사이로 정규화
    norm_val = (val - min_v) / (max_v - min_v)
    # Plotly의 'Viridis' 또는 'Plasma' 컬러셋에서 색상 추출
    return plotly.colors.sample_colorscale("Viridis", norm_val)[0]

# 3. 3D 막대(정사각 기둥) 생성 함수
def create_3d_bar(x, y, z, color, width=0.7):
    # 정사각 밑면을 만들기 위해 x_half, y_half를 동일하게 설정
    w = width / 2
    return go.Mesh3d(
        x=[x-w, x+w, x+w, x-w, x-w, x+w, x+w, x-w],
        y=[y-w, y-w, y+w, y+w, y-w, y-w, y+w, y+w],
        z=[0, 0, 0, 0, z, z, z, z],
        i=[7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
        j=[3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
        k=[0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
        color=color,
        opacity=0.9,
        flatshading=True, # 면의 경계를 더 뚜렷하게
        name=f"값: {z}",
        hoverinfo='all'
    )

# 4. 그래프 생성
fig = go.Figure()

for i, row in df.iterrows():
    # 데이터에 '원소기호'나 '명칭' 컬럼이 있다고 가정하고 툴팁 추가 가능
    element_name = row.get('원소명', f"Index {i}")
    
    # 색상 계산
    bar_color = get_color(row[column_to_viz], min_val, max_val)
    
    # 막대 추가
    fig.add_trace(create_3d_bar(
        x=row['족 (y좌표)'], 
        y=row['주기 (x좌표)'], 
        z=row[column_to_viz],
        color=bar_color
    ))

# 레이아웃 설정
fig.update_layout(
    scene=dict(
        xaxis=dict(title='Group (족)', dtick=1, range=[0, 19]),
        yaxis=dict(title='Period (주기)', dtick=1, autorange="reversed"),
        zaxis=dict(title=column_to_viz),
        aspectmode='manual',
        aspectratio=dict(x=2, y=1, z=0.5) # 그래프의 전체적인 비율 조정
    ),
    margin=dict(l=0, r=0, b=0, t=40),
    height=700,
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

# 5. 데이터 요약 통계 (추가)
with st.expander("데이터 요약 보기"):
    st.dataframe(df[['주기 (x좌표)', '족 (y좌표)', column_to_viz]].describe())