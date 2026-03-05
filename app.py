import streamlit as st
import time
import random
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats  # 用于计量模型相关性分析
from plotly.subplots import make_subplots

# ==========================================
# 页面配置与全局样式（修复侧边栏不可见Bug）
# ==========================================
# 修复1：增加 initial_sidebar_state="expanded"，强制页面一加载就打开侧边栏
st.set_page_config(
    page_title="颐幼全龄通 | 智能调度与预约", 
    page_icon="📱", 
    layout="wide",
    initial_sidebar_state="expanded" 
)

# 修复2：修正 CSS 语法，并释放 header（否则展开按钮会消失）
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            /* header {visibility: hidden;}  <- 必须注释或删掉这行，否则侧边栏展开按钮会消失 */
            .main .block-container {padding-top: 2rem;}
            /* 修复了原本错误的 # 注释，CSS注释必须用斜杠星号 */
            section[data-testid="stSidebar"] {min-width: 250px !important;}  
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'vitality_points' not in st.session_state:
    st.session_state.vitality_points = 0
if 'family_members' not in st.session_state:
    st.session_state.family_members = []

# ==========================================
# 侧边栏：系统视角切换
# ==========================================
with st.sidebar:
    st.image("https://img.icons8.com/color/150/000000/family.png", width=60)
    st.markdown("### 颐幼全龄通系统")
    st.caption("东林养老院（玉林试点） | 响应“十五五”国家战略，科技赋能代际连接")
    view_mode = st.radio("切换系统视图：", ["📱 C端 - 家庭智能预约", "📊 B端 - 机构数据驾驶舱"])
    st.divider()
    st.markdown("🔒 **底座支持**：AIGC量化风控中台 & 物联网IoT监测 | 代际融合匹配模型")

# （...下方的 C端 和 B端 函数代码保持你原来的不变即可...）
