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
# 页面配置与全局样式（优化侧边栏可见性）
# ==========================================
st.set_page_config(page_title="颐幼全龄通 | 智能调度与预约", page_icon="📱", layout="wide")  # 改为wide，避免centered挤压侧边栏
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .main .block-container {padding-top: 2rem;}
            section[data-testid="stSidebar"] {visibility: visible !important; min-width: 250px;}  # 强制侧边栏可见
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
# 侧边栏：系统视角切换（添加调试）
# ==========================================
with st.sidebar:
    st.markdown("**侧边栏调试：如果看到此句，侧边栏已渲染**")  # 调试提示
    st.image("https://img.icons8.com/color/150/000000/family.png", width=60)
    st.markdown("### 颐幼全龄通系统")
    st.caption("东林养老院（玉林试点） | 响应“十五五”国家战略，科技赋能代际连接")
    view_mode = st.radio("切换系统视图：", ["📱 C端 - 家庭智能预约", "📊 B端 - 机构数据驾驶舱"])
    st.divider()
    st.markdown("🔒 **底座支持**：AIGC量化风控中台 & 物联网IoT监测 | 代际融合匹配模型")

# ...（其余代码保持不变，包括render_c_end_home()、render_c_end_success()和render_b_end_dashboard()）
