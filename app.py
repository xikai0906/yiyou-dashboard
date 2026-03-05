import streamlit as st
import time
import random

# ==========================================
# 页面配置
# ==========================================
st.set_page_config(page_title="颐幼全龄通 | 智能预约", page_icon="📱", layout="centered")

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .main .block-container {max-width: 500px; padding-top: 2rem;}
            div[data-testid="stMarkdownContainer"] > p {font-size: 0.95rem; margin-bottom: 0.5rem;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = 'home'

# ==========================================
# 页面 1：预约主界面 (极简风格，注重选项颗粒度)
# ==========================================
def render_home():
    st.title("颐幼全龄通")
    st.caption("东林养老院（玉林试点） | 智能预约与照护调度系统")
    st.divider()
    
    # 模块 A：基础信息与精细化人群分层
    st.subheader("1. 服务对象与档案")
    col1, col2 = st.columns(2)
    with col1:
        senior_selected = st.checkbox("👴 长者服务 (Senior)")
    with col2:
        toddler_selected = st.checkbox("👶 幼儿托育 (Toddler)")
        
    if not senior_selected and not toddler_selected:
        st.warning("请勾选需要预约的家庭成员")
        return

    st.session_state.family_members = []
    senior_age, toddler_age = None, None
    
    if senior_selected:
        senior_age = st.selectbox("长者年龄及状态评估", ["60-69岁 (活力长者，生活自理)", "70-79岁 (介助长者，需部分协助)", "80岁以上 (介护长者，需全面照护)"])
        st.session_state.family_members.append("长者")
        
    if toddler_selected:
        toddler_age = st.selectbox("幼儿月龄与托育阶段", ["6-12个月 (婴儿期：注重抚育与大动作)", "1-2岁 (幼儿期：注重语言与感官启蒙)", "2-3岁 (学前期：注重社交与蒙氏早教)"])
        st.session_state.family_members.append("幼儿")

    # 导师加分项：健康与餐饮个性化采集
    diet_pref = st.selectbox("偏好餐饮类型", ["常规营养均衡餐", "素食/无肉餐", "低脂低糖控糖餐", "流食/高能量软烂辅食"])
    
    # 模块 B：下沉服务选项
    st.subheader("2. 核心服务定制")
    available_services = []
    
    if senior_selected and not toddler_selected:
        available_services.extend([
            "【颐养】棋牌书画与社交活动室 (￥40/半天)", 
            "【康养】慢病管理与康复理疗 (￥150/次)",
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
            "【老幼同乐】园艺种植代际互动 (￥60/次)",
            "【老幼同乐】传统手工剪纸与儿歌共赏 (￥50/次)",
            "综合全日托管 (分室照料 + 互动时段) (￥200/天)"
        ])
        
    selected_service = st.selectbox("选择具体服务项目", available_services)
    
    # 模块 C：通勤与接送服务 (响应导师要求)
    st.subheader("3. 通勤与时段")
    transport = st.radio("接送服务选择", [
        "家属自行接送", 
        "站点班车：玉州区-中心广场接送点 (+￥15)", 
        "站点班车：玉东新区-万达接送点 (+￥15)",
        "专车上门接送 (需AIGC后台评估路线匹配度, +￥30起)"
    ])
    
    time_slot = st.selectbox("预约时段", [
        "上午场 08:30 - 11:30 (含早点)",
        "下午场 14:00 - 17:00 (含午休与下午茶)",
        "全天场 08:30 - 17:00 (含三餐两点)"
    ])
    
    st.divider()
    
    # 模块 D：量化风控与预约提交
    if st.button("生成预约方案与动态报价", use_container_width=True, type="primary"):
        st.session_state.service = selected_service
        st.session_state.time_slot = time_slot
        st.session_state.transport = transport
        st.session_state.diet = diet_pref
        
        # 模拟量化定价与资源调度计算
        with st.spinner('调用后台算法中：进行床位排班验证与 PROC GLM 动态资源定价...'):
            time.sleep(1.8)
            base_price = int(selected_service.split("￥")[1].split("/")[0])
            if "+￥" in transport:
                base_price += int(transport.split("+￥")[1].split(")")[0].replace("起", ""))
            
            st.session_state.price = base_price * (1.1 if "全天" in time_slot else 1.0)
            st.session_state.page = 'success'
            st.rerun()

# ==========================================
# 页面 2：预约凭证与业务风控反馈
# ==========================================
def render_success():
    st.success("✅ 方案生成成功！")
    
    st.markdown("### 电子服务凭证")
    st.info(f"""
    **👥 服务对象**：{', '.join(st.session_state.family_members)}  
    **🍱 餐饮要求**：{st.session_state.diet}  
    **📋 核心服务**：{st.session_state.service}  
    **🚌 交通方式**：{st.session_state.transport}  
    **⏰ 预约时段**：{st.session_state.time_slot}
    """)
    
    st.metric(label="系统核算预估费用", value=f"￥{st.session_state.price:.2f}")
    
    # 导师加分项：展示后台逻辑的复杂性
    st.markdown("---")
    st.markdown("#### ⚙️ 后台风控与调度状态 (模拟)")
    st.caption("✔️ **资源调度**：当前时段护工床位配比为 1:4，处于最佳负荷区间。")
    st.caption("✔️ **交叉感染阻断**：系统已将长者活动区与幼儿托育区进行物理动线隔离，独立新风系统已开启。")
    st.caption("✔️ **餐饮供应链**：特殊餐饮指令已下发至中央厨房，食材溯源正常。")
    
    st.markdown("<br><p style='text-align: center; color: gray; font-size: 0.8rem;'>凭证号：YY-" + str(random.randint(100000, 999999)) + "</p>", unsafe_allow_html=True)
    
    if st.button("返回修改预约", use_container_width=True):
        st.session_state.page = 'home'
        st.rerun()

if st.session_state.page == 'home':
    render_home()
elif st.session_state.page == 'success':
    render_success()
