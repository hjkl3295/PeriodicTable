import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# 1. 데이터 불러오기
# !! 파일 이름은 대소문자까지 일치
#df = pd.read_csv('D:\OneDrive\Data_ML\PeriodicTable\Data_in\periodictable_0509.CSV')
#df = pd.read_csv(r'D:\OneDrive\Data_ML\PeriodicTable\Data_in\periodictable_0509.CSV', encoding='cp949')
df = pd.read_csv('n\PeriodicTable_0509.CSV', encoding='cp949')


# 2. 웹 화면 설정
st.title("🧪 학생들을 위한 3D 원소 성질 시각화")
column_to_viz = st.selectbox("시각화할 성질을 선택하세요", 
                            ['원자반지름(A)', '표준환원전위', '1차 이온화에너지', '전기음성도'])

# 데이터 전처리: 결측치는 0으로 처리
df[column_to_viz] = pd.to_numeric(df[column_to_viz], errors='coerce').fillna(0)

# 3. 3D 막대(직육면체) 생성 함수
def create_3d_bar(x, y, z, width=0.8):
    # 직육면체의 8개 꼭짓점 정의
    return go.Mesh3d(
        x=[x-width/2, x+width/2, x+width/2, x-width/2, x-width/2, x+width/2, x+width/2, x-width/2],
        y=[y-width/2, y-width/2, y+width/2, y+width/2, y-width/2, y-width/2, y+width/2, y+width/2],
        z=[0, 0, 0, 0, z, z, z, z],
        i=[7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
        j=[3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
        k=[0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
        opacity=0.8,
        color='royalblue' if z >= 0 else 'crimson' # 환원전위가 음수면 빨간색
    )

# 4. 그래프 그리기
fig = go.Figure()

for i, row in df.iterrows():
    # 데이터 상의 주기가 x, 족이 y로 되어 있으므로 그대로 매핑
    fig.add_trace(create_3d_bar(row['족 (y좌표)'], row['주기 (x좌표)'], row[column_to_viz]))

# 레이아웃 설정
fig.update_layout(
    scene=dict(
        xaxis_title='Group (족)',
        yaxis_title='Period (주기)',
        zaxis_title=column_to_viz,
        yaxis=dict(autorange="reversed") # 주기가 위에서 아래로 흐르도록
    ),
    margin=dict(l=0, r=0, b=0, t=40)
)

st.plotly_chart(fig)