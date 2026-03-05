import streamlit as st
import time
import random
import pandas as pd
import numpy as np
import plotly.express as px

# ==========================================
# 页面配置与全局样式
# ==========================================
st.set_page_config(page_title="颐幼全龄通 | 智能调度与预约", page_icon="📱", layout="centered")

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .main .block-container {padding-top: 2rem;}
            div[data-testid="stMarkdownContainer"] > p {font-size: 0.95rem; margin-bottom: 0.5rem;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'vitality_points' not in st.session_state:
    st.session_state.vitality_points = 0

# ==========================================
# 侧边栏：系统视角切换
# ==========================================
with st.sidebar:
    st.image("https://img.icons8.com/color/150/000000/family.png", width=60)
    st.markdown("### 颐幼全龄通系统")
    st.caption("东林养老院（玉林试点）")
    view_mode = st.radio("切换系统视图：", ["📱 C端 - 家庭智能预约", "📊 B端 - 机构数据驾驶舱"])
    st.divider()
    st.markdown("🔒 **底座支持**：量化风控中台 & 物联网IoT监测")

# ==========================================
# C端：家庭智能预约 (精细化服务与代际连接)
# ==========================================
def render_c_end_home():
    st.title("家庭照护一键预约")
    st.caption("提供定制化“一老一小”综合解决方案与代际互动服务")
    st.divider()
    
    # 模块 A：基础信息与精细化人群分层
    st.subheader("1. 建立家庭服务档案")
    col1, col2 = st.columns(2)
    with col1:
        senior_selected = st.checkbox("👴 长者 (Senior)")
    with col2:
        toddler_selected = st.checkbox("👶 幼儿 (Toddler)")
        
    if not senior_selected and not toddler_selected:
        st.warning("请勾选需要预约的家庭成员以获取匹配服务")
        return

    st.session_state.family_members = []
    
    if senior_selected:
        st.selectbox("长者状态评估 (决定IoT监测级别)", ["60-69岁 (活力长者，生活自理)", "70-79岁 (介助长者，需防跌倒手环监测)", "80岁以上 (介护长者，需全面医护巡诊)"])
        st.session_state.family_members.append("长者")
        
    if toddler_selected:
        st.selectbox("幼儿托育阶段 (决定早教流派)", ["6-12个月 (婴儿期：睡眠监测与抚育)", "1-2岁 (幼儿期：双语启蒙与大动作)", "2-3岁 (学前期：蒙氏感官与社交)"])
        st.session_state.family_members.append("幼儿")

    diet_pref = st.selectbox("个性化餐饮调度 (对接中央厨房)", ["常规营养均衡餐", "素食/无肉餐", "低脂低糖控糖餐", "流食/高能量软烂辅食"])
    
    # 模块 B：下沉服务选项
    st.subheader("2. 核心增值服务")
    available_services = []
    
    if senior_selected and not toddler_selected:
        available_services.extend([
            "【颐养】棋牌书画与社交活动室 (￥40/半天)", 
            "【康养】慢病管理与康复理疗直通车 (￥150/次)",
            "【研学】长者智能手机与防诈骗微课堂 (￥30/次)"
        ])
    elif toddler_selected and not senior_selected:
        available_services.extend([
            "【早教】蒙特梭利感官启蒙小班 (￥120/半天)", 
            "【早教】双语绘本共读与语言开发 (￥100/半天)",
            "【体适能】幼儿感统协调训练 (￥110/次)"
        ])
    elif senior_selected and toddler_selected:
        available_services.extend([
            "【老幼同乐】园艺种植代际互动 (￥60/次) 🌟送代际积分",
            "【老幼同乐】传统手工剪纸与儿歌共赏 (￥50/次) 🌟送代际积分",
            "综合全日托管 (分室照料 + 互动时段) (￥200/天)"
        ])
        
    selected_service = st.selectbox("选择具体服务项目", available_services)
    
    # 模块 C：通勤与时段
    st.subheader("3. 运力调度与时段")
    transport = st.radio("接送服务选择", [
        "家属自行接送", 
        "站点班车：玉州区-中心广场接送点 (+￥15)", 
        "站点班车：玉东新区-万达接送点 (+￥15)",
        "专车上门接送 (后台自动测算最优路线, +￥30起)"
    ])
    
    time_slot = st.selectbox("预约时段", [
        "上午场 08:30 - 11:30 (含早点)",
        "下午场 14:00 - 17:00 (含午休与下午茶)",
        "全天场 08:30 - 17:00 (含三餐两点)"
    ])
    
    st.divider()
    
    if st.button("生成预约方案与动态报价", use_container_width=True, type="primary"):
        st.session_state.service = selected_service
        st.session_state.time_slot = time_slot
        st.session_state.transport = transport
        st.session_state.diet = diet_pref
        
        with st.spinner('计量风控模型演算中：进行床位资源博弈与动态定价...'):
            time.sleep(1.5)
            base_price = int(selected_service.split("￥")[1].split("/")[0].split(")")[0])
            if "+￥" in transport:
                base_price += int(transport.split("+￥")[1].split(")")[0].replace("起", ""))
            
            # 模拟计量定价
            multiplier = 1.15 if "全天" in time_slot else 0.95
            st.session_state.price = base_price * multiplier
            
            # 代际互动积分激励
            if "老幼同乐" in selected_service:
                st.session_state.vitality_points += 50
                
            st.session_state.page = 'success'
            st.rerun()

def render_c_end_success():
    st.success("✅ 方案生成成功！床位资源已锁定。")
    
    st.markdown("### 电子服务凭证")
    st.info(f"""
    **👥 服务对象**：{', '.join(st.session_state.family_members)}  
    **🍱 餐饮调度**：{st.session_state.diet}  
    **📋 核心服务**：{st.session_state.service}  
    **🚌 运力安排**：{st.session_state.transport}  
    **⏰ 预约时段**：{st.session_state.time_slot}
    """)
    
    col1, col2 = st.columns(2)
    col1.metric(label="系统核算预估费用", value=f"￥{st.session_state.price:.2f}")
    col2.metric(label="家庭代际活力积分", value=f"{st.session_state.vitality_points} 分", delta="+50" if "老幼同乐" in st.session_state.service else "0")
    
    st.markdown("---")
    st.markdown("#### 🛡️ 机构风控与医疗生态保障")
    st.caption("✔️ **IoT体征监测**：已开通后台实时心率/防跌倒雷达监测接口。")
    st.caption("✔️ **绿色医疗通道**：照护期间享有合作医院专属免排队急诊权限。")
    st.caption("✔️ **微保险覆盖**：本次服务已自动嵌入单日照护意外险与交叉感染险。")
    
    st.markdown("<br><p style='text-align: center; color: gray; font-size: 0.8rem;'>凭证号：YY-" + str(random.randint(100000, 999999)) + "</p>", unsafe_allow_html=True)
    
    if st.button("返回首页", use_container_width=True):
        st.session_state.page = 'home'
        st.rerun()

# ==========================================
# B端：机构数据驾驶舱 (体现金融科技与量化分析能力)
# ==========================================
def render_b_end_dashboard():
    st.title("机构运营驾驶舱")
    st.caption("量化数据分析与护工资源动态调度看板")
    st.divider()

    # 顶部核心指标
    col1, col2, col3 = st.columns(3)
    col1.metric("今日总订单数", "128单", "12% 同比增长")
    col2.metric("当前护工配比缺口", "0人", "资源配置最优")
    col3.metric("预计日结流水", "￥18,450", "8.5% 溢价收益")

    st.markdown("### 📈 床位需求预测与动态溢价指数")
    st.markdown("<span style='font-size: 0.85rem; color: gray;'>基于计量经济学时间序列模型，预测日内需求波动并触发调价指令。</span>", unsafe_allow_html=True)
    
    # 使用 Pandas 和 Numpy 生成模拟数据，使用 Plotly 绘制高级图表
    hours = [f"{i}:00" for i in range(8, 19)]
    base_demand = np.array([20, 45, 80, 75, 50, 40, 60, 85, 90, 65, 30])
    noise = np.random.normal(0, 5, len(hours))
    actual_demand = np.clip(base_demand + noise, 10, 100)
    
    # 溢价乘数逻辑 (需求大于70时触发溢价，小于40触发折扣)
    price_multiplier = np.where(actual_demand > 70, 1.2, np.where(actual_demand < 40, 0.85, 1.0))
    
    df = pd.DataFrame({
        "时间": hours,
        "床位需求热度": actual_demand,
        "动态溢价乘数": price_multiplier
    })
    
    # 绘制 Plotly 双轴图表
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Bar(x=df["时间"], y=df["床位需求热度"], name="需求热度", marker_color='rgba(55, 128, 191, 0.6)'),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(x=df["时间"], y=df["动态溢价乘数"], name="溢价乘数 (风险对冲)", mode='lines+markers', line=dict(color='red', width=2)),
        secondary_y=True,
    )
    fig.update_layout(height=400, margin=dict(l=0, r=0, t=30, b=0), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    fig.update_yaxes(title_text="需求热度 (人次)", secondary_y=False)
    fig.update_yaxes(title_text="价格乘数", secondary_y=True, range=[0.5, 1.5])
    
    st.plotly_chart(fig, use_container_width=True)

    # 底部预警与调度
    st.markdown("### ⚠️ AIGC 供应链与风控预警")
    with st.expander("展开查看实时预警流水", expanded=True):
        st.success("🟢 **医疗物联网**：当前在园 84 位长者，体征数据均在正常波动域内。")
        st.warning("🟡 **供应链金融**：本月康复耗材采购金占用率达 75%，建议启动下一期应收账款保理流转。")
        st.info("🔵 **交叉感染防范**：14:00-16:00 幼儿场次即将开始，B区紫外线消毒与新风置换已完成。")

# ==========================================
# 路由控制
# ==========================================
if view_mode == "📱 C端 - 家庭智能预约":
    if st.session_state.page == 'home':
        render_c_end_home()
    elif st.session_state.page == 'success':
        render_c_end_success()
else:
    # 切换到 B 端时重置 C 端的页面状态
    st.session_state.page = 'home'
    render_b_end_dashboard()
