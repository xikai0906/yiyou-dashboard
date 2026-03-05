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
# ==========================================
# C端：家庭智能预约 (精细化服务与代际连接，强化匹配与积分抵扣)
# ==========================================
def render_c_end_home():
    st.title("家庭照护一键预约")
    st.caption("科技赋能“一老一小”代际融合，解决长者孤独与幼儿托育痛点，重塑家庭连接")
    st.divider()
   
    # 模块 A：基础信息与精细化人群分层 (支持代际匹配评估)
    st.subheader("1. 建立家庭服务档案   （双选时可使用老幼同乐服务）")
    col1, col2 = st.columns(2)
    with col1:
        senior_selected = st.checkbox("👴 长者 (Senior)")
    with col2:
        toddler_selected = st.checkbox("👶 幼儿托育 (Toddler)")
       
    if not senior_selected and not toddler_selected:
        st.warning("请勾选需要预约的家庭成员以获取匹配服务")
        return
   
    st.session_state.family_members = []
   
    if senior_selected:
        senior_profile = st.selectbox("长者状态评估 (用于代际匹配)", ["60-69岁 (活力长者，有表达欲/特长)", "70-79岁 (介助长者，需陪伴防孤独)", "80岁以上 (介护长者，需温和互动)"])
        st.session_state.family_members.append("长者")
       
    if toddler_selected:
        toddler_profile = st.selectbox("幼儿托育阶段 (用于代际匹配)", ["6-12个月 (婴儿期：需温柔陪伴)", "1-2岁 (幼儿期：需语言启蒙)", "2-3岁 (学前期：需社交开发)"])
        st.session_state.family_members.append("幼儿")
    diet_pref = st.selectbox("个性化餐饮调度 (对接中央厨房)", ["常规营养均衡餐", "素食/无肉餐", "低脂低糖控糖餐", "流食/高能量软烂辅食"])
   
    # 模块 B：下沉服务选项 (强调代际融合，精准匹配，文案自然化)
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
            "【老幼同乐】园艺种植代际互动 (￥60/次，匹配长者特长与幼儿需求)",
            "【老幼同乐】传统手工剪纸与儿歌共赏 (￥50/次，促进幼儿社交能力发展)",
            "综合全日托管 (分室照料 + 互动时段) (￥200/天，积分抵扣可用)"
        ])
        st.info("💡 代际融合模式已启用：系统将精准匹配长者表达欲与幼儿启蒙需，产生化学反应，量化证明长者孤独下降、幼儿社交上升")
       
    selected_service = st.selectbox("选择具体服务项目", available_services)
   
    # 模块 C：通勤与时段 (安全边界强化)
    st.subheader("3. 运力调度与时段")
    transport = st.radio("接送服务选择", [
        "家属自行接送",
        "站点班车：玉州区-中心广场接送点 (+￥15)",
        "站点班车：玉东新区-万达接送点 (+￥15)",
        "专车上门接送 (后台自动测算最优路线, +￥30起)"
    ])
   
    time_slot = st.selectbox("预约时段 (分时复用：上午长者、下午幼儿、夜间消毒)", [
        "上午场 08:30 - 11:30 (含早点，长者优先)",
        "下午场 14:00 - 17:00 (含午休与下午茶，幼儿优先)",
        "全天场 08:30 - 17:00 (含三餐两点，代际互动时段)"
    ])
   
    # === 关键修复：医疗级安全承诺区 ===
    st.divider()
    st.subheader("4. 健康申报与安全隔离承诺")
    with st.expander("🛡️ 查阅《东林康养：医疗级卫生与代际互动安全规范》", expanded=False):
        st.markdown("""
        **1. 绝对物理隔离**：长者区与幼儿区独立新风系统，互不交叉  
        **2. 医疗级准入筛查**：所有老幼同乐参与者均持绿码，系统自动拦截发热/流感风险人员  
        **3. 非强制互动**：算法精准匹配，幼儿出现抵触情绪立即终止  
        **4. 双向保险保障**：已包含交叉感染险与意外险
        """)
    
    # 强制勾选（必须在按钮之前，且用 session_state 存储）
    if 'health_promise' not in st.session_state:
        st.session_state.health_promise = False
    st.session_state.health_promise = st.checkbox(
        "☑️ 我已阅读上述规范，并承诺本次预约家庭成员近期无发热、咳嗽及其他传染性疾病"
    )

    st.divider()
   
    if st.button("生成预约方案与动态报价", use_container_width=True, type="primary"):
        if not st.session_state.health_promise:
            st.error("⚠️ 请先勾选健康安全承诺，否则无法提交预约")
            return
        
        st.session_state.service = selected_service
        st.session_state.time_slot = time_slot
        st.session_state.transport = transport
        st.session_state.diet = diet_pref
        
        with st.spinner('AIGC代际匹配模型演算中：精准匹配长幼，进行效果量化与积分抵扣...'):
            time.sleep(1.5)
            base_price = int(selected_service.split("￥")[1].split("/")[0].split(")")[0])
            if "+￥" in transport:
                base_price += int(transport.split("+￥")[1].split(")")[0].replace("起", ""))
           
            # 模拟计量定价与积分抵扣
            multiplier = 1.15 if "全天" in time_slot else 0.95
            points_deduct = min(st.session_state.vitality_points // 10, base_price * 0.1)  # 积分抵扣最多10%
            st.session_state.price = (base_price * multiplier) - points_deduct
           
            # 代际互动积分激励 (时间银行概念)
            if "老幼同乐" in selected_service:
                st.session_state.vitality_points += 50
                st.info("✅ 代际时间银行激活：陪伴积分可抵扣护理/餐饮费，形成互助闭环")
               
            st.session_state.page = 'success'
            st.rerun()

def render_c_end_success():
    st.success("✅ 方案生成成功！代际匹配已锁定，效果量化跟踪启动。")
   
    st.markdown("### 电子服务凭证")
    st.info(f"""
    **👥 服务对象**：{', '.join(st.session_state.family_members)}
    **🍱 餐饮调度**：{st.session_state.diet}
    **📋 核心服务**：{st.session_state.service}
    **🚌 运力安排**：{st.session_state.transport}
    **⏰ 预约时段**：{st.session_state.time_slot}
    """)
   
    col1, col2 = st.columns(2)
    col1.metric(label="系统核算预估费用 (积分抵扣后)", value=f"￥{st.session_state.price:.2f}")
    col2.metric(label="家庭代际活力积分 (时间银行)", value=f"{st.session_state.vitality_points} 分", delta="+50" if "老幼同乐" in st.session_state.service else "0")
   
    st.markdown("---")
    st.markdown("#### 🛡️ 机构风控与医疗生态保障")
    st.caption("✔️ **IoT体征监测**：已开通后台实时心率/防跌倒雷达监测接口。")
    st.caption("✔️ **绿色医疗通道**：照护期间享有合作医院专属免排队急诊权限。")
    st.caption("✔️ **微保险覆盖**：本次服务已自动嵌入单日照护意外险与交叉感染险。")
    st.caption("✔️ **安全边界**：物理隔离+每日消毒+24h医护，符合卫健委指南。")
   
    st.markdown("<br><p style='text-align: center; color: gray; font-size: 0.8rem;'>凭证号：YY-" + str(random.randint(100000, 999999)) + "</p>", unsafe_allow_html=True)
   
    if st.button("返回首页", use_container_width=True):
        st.session_state.page = 'home'
        st.rerun()

# ==========================================
# B端：机构数据驾驶舱 (新增代际融合量化看板，体现模式创新)
# ==========================================
def render_b_end_dashboard():
    st.title("机构运营驾驶舱")
    st.caption("量化数据分析与代际融合智能调度看板 | 证明代际互动价值")
    st.divider()
    
    # 顶部核心指标 (整合试点数据)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("今日总订单数", "128单", "12% 同比增长")
    col2.metric("当前护工配比缺口", "0人", "资源配置最优")
    col3.metric("预计日结流水", "￥18,450", "8.5% 溢价收益")
    col4.metric("代际匹配成功率", "92%", "转化率85%，复购72%")
    
    # 多标签页：原有需求预测 + 新增代际融合看板
    tab1, tab2 = st.tabs(["📈 床位需求预测与动态溢价", "🤝 代际融合量化与智能调度"])
    
    with tab1:
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
    
    with tab2:
        st.subheader("代际融合量化看板：科技证明社会温度")
        st.markdown("利用算法精准匹配长者特长与幼儿需求，量化互动效果，形成时间银行互助闭环")
        
        # 1. 智能代际匹配模型展示 (模拟匹配结果)
        st.markdown("#### 1. 智能匹配结果 (基于表达欲/启蒙需)")
        match_df = pd.DataFrame({
            "长者ID": ["S001", "S002", "S003"],
            "长者特长": ["故事讲述", "手工指导", "园艺经验"],
            "匹配幼儿ID": ["T001", "T002", "T003"],
            "幼儿需求": ["语言启蒙", "社交开发", "感官训练"],
            "匹配分数": [0.92, 0.85, 0.88]
        })
        st.table(match_df)
        st.caption("算法：基于PROC GLM等效模型，匹配后互动率提升30%")
        
        # 2. 康复效果量化：折线图 + 计量相关性分析 (优化为metric展示)
        st.markdown("#### 2. 互动效果量化 (长者孤独下降、幼儿社交上升)")
        weeks = np.arange(1, 9)
        senior_loneliness = np.linspace(75, 45, 8) + np.random.normal(0, 2, 8)  # 下降
        toddler_social = np.linspace(60, 85, 8) + np.random.normal(0, 2, 8)  # 上升
        
        effect_df = pd.DataFrame({
            "周次": weeks,
            "长者孤独指数 (%)": senior_loneliness,
            "幼儿社交评分 (%)": toddler_social
        })
        
        fig_effect = px.line(effect_df, x="周次", y=["长者孤独指数 (%)", "幼儿社交评分 (%)"],
                             title="代际互动前后效果追踪 (几周后量化变化)",
                             color_discrete_map={"长者孤独指数 (%)": "red", "幼儿社交评分 (%)": "green"})
        st.plotly_chart(fig_effect, use_container_width=True)
        
        # 计量模型：相关性分析 (证明正相关，用metric强化展示)
        corr, p_val = stats.pearsonr(-senior_loneliness, toddler_social)  # 孤独下降与社交上升的相关
        col1, col2 = st.columns(2)
        col1.metric("Pearson相关系数", f"{corr:.2f}", "证明正相关")
        col2.metric("显著性P值", f"{p_val:.4f}", "P<0.05显著")
        
        # 3. 代际时间银行/积分系统
        st.markdown("#### 3. 时间银行积分统计 (陪伴积分抵扣费用)")
        points_df = pd.DataFrame({
            "用户类型": ["长者", "幼儿家庭", "总计"],
            "累计积分": [1200, 800, 2000],
            "已抵扣金额 (￥)": [120, 80, 200],
            "互助闭环价值": ["护理费减免", "托育优惠", "社会价值5000万+"]
        })
        st.table(points_df)
        st.caption("积分机制：长者陪伴产生积分，直接抵扣费用，形成可持续互助，释放女性劳动力")

    # === 新增/替换：深度医疗风控与交叉感染防范大屏 ===
    st.markdown("### ⚠️ 医疗级风控与交叉感染防范系统")
    st.caption("实时对接医疗机构 HIS 系统，全天候守护代际互动安全底线")
    
    risk_col1, risk_col2, risk_col3 = st.columns(3)
    risk_col1.metric("今日园区交叉感染率", "0.00%", "连续 128 天零感染")
    risk_col2.metric("互动长者绿码核验", "100% 达标", "已拦截 2 名流感风险长者")
    risk_col3.metric("第三空间空气洁净度", "优 (PM2.5: 12)", "新风与紫外消毒运行中")

    with st.expander("🔍 展开查看实时医疗风控与拦截日志", expanded=True):
        st.success("🟢 **入园闸机拦截系统**：08:15 成功拦截一位体温异常 (37.6℃) 的长者，已自动取消其今日代际互动资格，并触发私立医院发热门诊绿通。")
        st.info("🔵 **分时复用与空间消杀**：11:30 上午场结束。系统已自动闭锁代际活动室，正在执行 60 分钟的高强度臭氧+紫外线无人消杀，为下午场幼儿托育做准备。")
        st.warning("🟡 **幼儿情绪监控预警**：昨日 15:20，监控分析模型捕捉到一幼儿在手工课上出现哭闹情绪，系统已自动判定“匹配度失效”，护工在 30 秒内已将幼儿安全带回专属早教区。")

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
