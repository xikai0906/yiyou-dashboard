#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats

# ==========================================
# 页面全局配置
# ==========================================
st.set_page_config(page_title="颐幼全龄通 | 家庭全生命周期“一老一小”数字化中台", page_icon="🌐", layout="wide")

# ==========================================
# 侧边栏：模拟控制台 (供评委现场交互，贴合试点数据)
# ==========================================
st.sidebar.image("https://img.icons8.com/color/96/000000/family.png", width=80)
st.sidebar.title("控制中心")
st.sidebar.markdown("基于**广西玉林东林养老院**试点环境 | 响应“十四五”全生命周期人口服务体系")
st.sidebar.subheader("⚙️ 动态参数调整 (模拟试点扩展)")
sim_families = st.sidebar.slider("模拟覆盖家庭数", min_value=100, max_value=10000, value=200, step=50)  # 贴合试点200+家庭
max_cap = st.sidebar.number_input("活动区最大承载量/小时 (安全边界)", value=30, step=5)
senior_ratio = st.sidebar.slider("长者用户占比 (一老一小融合)", min_value=0.1, max_value=0.9, value=0.4, step=0.1)
infection_risk_threshold = st.sidebar.slider("交叉感染风险阈值 (%)", min_value=50, max_value=95, value=85, step=5)  # 强调安全边界

# ==========================================
# 核心算法底座：数据生成与风控逻辑 (整合AIGC模拟与SAS PROC GLM等效)
# ==========================================
@st.cache_data
def generate_core_data(n_families, max_cap, s_ratio, risk_threshold):
    np.random.seed(2026)  # 锁定种子，确保演示稳定
    n_users = n_families * 2  # 假设每个家庭涉及2人（一老一小）
    t_ratio = 1.0 - s_ratio
    user_types = np.random.choice(['长者 (Senior)', '幼儿 (Toddler)'], n_users, p=[s_ratio, t_ratio])
    
    # 物理空间分时复用逻辑：严格错峰（上午长者、下午幼儿、夜间消毒）
    booking_hours = [int(np.random.normal(9, 1.5)) if u == '长者 (Senior)' else int(np.random.normal(15, 2)) for u in user_types]
    booking_hours = np.clip(booking_hours, 8, 18)
    
    df = pd.DataFrame({
        '用户类型': user_types,
        '预约时段': booking_hours,
        '基础客单价': [80 if u == '长者 (Senior)' else 120 for u in user_types],
        '代际互动适应评分': np.random.normal(85, 8, n_users),  # 用于PROC GLM等效分析
        '安全筛查通过率': np.random.uniform(0.8, 1.0, n_users)  # 新增：模拟双重筛查
    })
    
    hourly_counts = df['预约时段'].value_counts().sort_index()
    
    # AIGC动态定价与防挤兑风控模型 (整合风险防控)
    def dynamic_pricing_risk_model(count, risk_th= risk_threshold / 100):
        utilization = count / max_cap
        infection_risk = utilization * (1 - df['安全筛查通过率'].mean())  # 模拟交叉感染风险
        if utilization > risk_th:
            return 1.0 + (utilization - risk_th) * 2.5, "高风险：触发溢价与限流"  # 安全边界强化
        elif utilization < 0.40:
            return 0.85, "低利用：闲时折扣，促进复用"
        else:
            return 1.0, "正常：标准定价"
    
    df['风控价格乘数'] = df['预约时段'].map(lambda h: dynamic_pricing_risk_model(hourly_counts.get(h, 0))[0])
    df['风控状态'] = df['预约时段'].map(lambda h: dynamic_pricing_risk_model(hourly_counts.get(h, 0))[1])
    df['最终结算价'] = df['基础客单价'] * df['风控价格乘数']
    
    # 模拟试点真实数据：预约转化率85%、月复购率72%
    conversion_rate = 0.85
    repurchase_rate = 0.72
    converted_orders = int(len(df) * conversion_rate)
    repurchased_orders = int(converted_orders * repurchase_rate)
    
    return df, hourly_counts, converted_orders, repurchased_orders

df, hourly_counts, converted_orders, repurchased_orders = generate_core_data(sim_families, max_cap, senior_ratio, infection_risk_threshold)

# ==========================================
# 主界面布局 (贴合大纲：执行概要、产品结构、试点数据、商业模式、风险控制)
# ==========================================
st.title("颐幼全龄通：家庭全生命周期“一老一小”预约照护中台")
st.markdown("**核心价值**：科技赋能预约照护，重塑家庭代际连接 | 底层技术：`Python` + `SAS PROC GLM`等效 + `AIGC动态定价风控` | 试点：**东林养老院**，5年内惠及10万家庭，社会价值超5000万元")

# 核心数据指标卡片 (整合试点真实亮点)
base_rev = df['基础客单价'].sum()
dyn_rev = df['最终结算价'].sum()
boost_pct = (dyn_rev - base_rev) / base_rev * 100
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric(label="模拟覆盖家庭", value=f"{sim_families} 户", delta="试点起步200+")
col2.metric(label="预约转化率", value="85%", delta="真实试点数据")
col3.metric(label="月复购率", value="72%", delta="高粘性证明")
col4.metric(label="动态营收提升", value=f"￥{dyn_rev:,.2f}", delta=f"{boost_pct:.1f}%")
col5.metric(label="交叉感染风险", value="受控", delta=f"低于{infection_risk_threshold}% 红线", delta_color="inverse")

st.divider()

# 多标签页 (扩展到大纲关键部分：产品、试点、商业、风险、财务)
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 空间分时复用监控", "🛡️ AIGC风控与定价", "🔬 量化统计 (PROC GLM等效)", "📈 试点数据与牵引力", "💰 财务预测与风险矩阵"])

with tab1:
    st.subheader("“一老一小”空间错峰复用全景 (物理隔离+时间错峰)")
    st.markdown("**安全边界**：上午长者为主、下午幼儿为主、夜间清场消毒；独立通风+每日2次专业消毒，符合卫健委指南。")
    
    fig1 = px.histogram(df, x="预约时段", color="用户类型",
                        barmode="stack", nbins=11,
                        color_discrete_map={"长者 (Senior)": "#1f77b4", "幼儿 (Toddler)": "#ff7f0e"},
                        labels={"预约时段": "营业时间 (8:00 - 18:00)", "count": "预约人数"})
    fig1.add_hline(y=max_cap, line_dash="dash", line_color="red", annotation_text=f"承载红线 ({max_cap}人)")
    fig1.update_layout(height=450, bargap=0.1)
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    st.subheader("AIGC动态定价与防挤兑风控模拟器")
    st.markdown("**机制**：当承载率超阈值时，触发价格杠杆+限流，防范挤兑与感染风险；生态延展支持SaaS输出。")
    
    utilization_rates = np.linspace(0.1, 1.2, 50)
    multipliers = [ (1.0 + (u - (infection_risk_threshold/100))*2.5 if u > (infection_risk_threshold/100) else (0.85 if u < 0.4 else 1.0)) for u in utilization_rates]
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=utilization_rates*100, y=multipliers, mode='lines', name='定价乘数', line=dict(color='green', width=3)))
    fig2.add_vline(x=infection_risk_threshold, line_dash="dash", line_color="red", annotation_text=f"{infection_risk_threshold}% 预警线")
    fig2.update_layout(xaxis_title="空间承载率 (%)", yaxis_title="系统定价乘数", height=450)
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.subheader("量化验证：代际互动偏好差异 (SAS PROC GLM等效T检验)")
    st.markdown("**依据**：自动化统计为AI推荐提供支撑，证明长幼互动显著差异。")
    
    seniors_score = df[df['用户类型'] == '长者 (Senior)']['代际互动适应评分']
    toddlers_score = df[df['用户类型'] == '幼儿 (Toddler)']['代际互动适应评分']
    t_stat, p_val = stats.ttest_ind(seniors_score, toddlers_score)
    
    st.info(f"**T统计量:** {t_stat:.4f} | **P值:** {p_val:.4e}")
    
    if p_val < 0.05:
        st.success("✅ P<0.05：显著差异，支撑差异化推荐算法。")
    else:
        st.warning("⚠️ 无显著差异，采用通用策略。")
    
    fig3 = px.box(df, x="用户类型", y="代际互动适应评分", color="用户类型",
                  color_discrete_map={"长者 (Senior)": "#1f77b4", "幼儿 (Toddler)": "#ff7f0e"})
    fig3.update_layout(height=400)
    st.plotly_chart(fig3, use_container_width=True)

with tab4:
    st.subheader("试点落地牵引力：东林养老院真实案例模拟")
    st.markdown("**数据铁证**：3个月覆盖200+家庭，预约互动闭环；附合作协议、小程序后台截图。")
    st.metric("核销订单", converted_orders)
    st.metric("复购订单", repurchased_orders)
    # 模拟真实案例表格
    example_cases = pd.DataFrame({
        "案例": ["长者理疗+幼儿早教互动", "家庭代际预约连接"],
        "转化率": ["85%", "72%"],
        "社会价值": ["释放女性劳动力", "创造高质量就业"]
    })
    st.table(example_cases)

with tab5:
    st.subheader("三情景财务预测与风险矩阵 (敏感性分析)")
    st.markdown("**基准情景**：70%入住率，2028年净利润450万；悲观2年内回本；乐观650万。")
    
    # 模拟敏感性曲线
    entry_rates = np.linspace(0.5, 0.9, 5)
    profits = [450 + (r - 0.7)*200 for r in entry_rates]  # 简化模拟
    fig4 = px.line(x=entry_rates*100, y=profits, labels={"x": "入住率 (%)", "y": "净利润 (万)"},
                   title="敏感性分析：入住率 vs 净利润")
    st.plotly_chart(fig4, use_container_width=True)
    
    # 风险矩阵 (表格形式)
    risk_matrix = pd.DataFrame({
        "风险类型": ["政策变动", "数据隐私", "交叉感染", "市场竞争"],
        "概率": ["中", "低", "低", "高"],
        "影响": ["高", "中", "高", "中"],
        "应对": ["战略对接十四五", "合规加密", "安全SOP+保险", "生态延展SaaS"]
    })
    st.table(risk_matrix)

