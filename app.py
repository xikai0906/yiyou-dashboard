import streamlit as st
import time
import random

# ==========================================
# 页面配置 (适配移动端视觉，贴合C端用户体验)
# ==========================================
st.set_page_config(page_title="颐幼全龄通 | 家庭“一老一小”智能预约", page_icon="📱", layout="centered")

# 隐藏 Streamlit 默认的顶部菜单和底部水印，让它更像原生 App
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            /* 限制最大宽度，在电脑上打开也像手机屏幕 */
            .main .block-container {max-width: 450px; padding-top: 2rem;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# ==========================================
# 初始化会话状态 (控制页面流转，模拟用户家庭预约)
# ==========================================
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'price' not in st.session_state:
    st.session_state.price = 0
if 'family_members' not in st.session_state:
    st.session_state.family_members = []  # 存储家庭成员选择，支持多选代际连接

# ==========================================
# 页面 1：预约主界面 (家庭全生命周期视角，强调代际连接)
# ==========================================
def render_home():
    st.image("https://img.icons8.com/color/150/000000/family.png", width=80)
    st.title("颐幼全龄通")
    st.markdown("**家庭全生命周期“一老一小”综合解决方案** | 东林养老院（玉林试点） | 响应“十五五”国家战略，科技赋能预约照护，重塑家庭代际连接")
    st.divider()
    
    # 1. 家庭成员选择 (支持“一老一小”多选，体现代际连接)
    st.subheader("1. 请选择家庭服务对象 (可多选)")
    st.info("💡 支持“一老一小”联合预约，促进代际互动，释放女性劳动力并创造高质量就业")
    senior_selected = st.checkbox("👴 长者服务 (Senior)")
    toddler_selected = st.checkbox("👶 幼儿托育 (Toddler)")
    
    if not senior_selected and not toddler_selected:
        st.warning("请至少选择一位家庭成员")
        return
    
    st.session_state.family_members = []
    if senior_selected:
        st.session_state.family_members.append("长者 (Senior)")
    if toddler_selected:
        st.session_state.family_members.append("幼儿 (Toddler)")
    
    # 2. 动态联动服务项目与价格绑定
    st.subheader("2. 请选择服务项目")
   
    # 构建服务与价格的字典映射
    service_price_map = {
        "日间照料床位 (￥80/次)": 80,
        "康复理疗中心 (合作私立医院) (￥150/次)": 150,
        "全日托育早教 (￥120/次)": 120,
        "感统训练室 (合作医疗器械) (￥100/次)": 100,
        "【老幼同乐】园艺手工 (代际连接专区) (￥50/次)": 50
    }
   
    available_services = []
    if "长者 (Senior)" in st.session_state.family_members:
        available_services.extend(["日间照料床位 (￥80/次)", "康复理疗中心 (合作私立医院) (￥150/次)"])
    if "幼儿 (Toddler)" in st.session_state.family_members:
        available_services.extend(["全日托育早教 (￥120/次)", "感统训练室 (合作医疗器械) (￥100/次)"])
    if len(st.session_state.family_members) == 2: # 代际互动专享服务
        available_services.append("【老幼同乐】园艺手工 (代际连接专区) (￥50/次)")
       
    selected_service = st.selectbox("当前可用服务 (试点覆盖200+家庭，转化率85%)", available_services)
   
    # 动态获取用户所选具体服务的基准价格
    base_price = service_price_map[selected_service]
    
    # 3. 选择分时复用时段 (强调安全边界：错峰、隔离、消毒)
    st.subheader("3. 预约时段")
    st.info("💡 系统严格分时复用：上午长者为主、下午幼儿为主、夜间清场消毒；物理隔离+独立通风+每日2次专业消毒，符合卫健委指南，交叉感染风险受控")
    time_slot_options = [
        "08:00 - 10:00 (长者优先，空闲，低风险)",
        "10:00 - 12:00 (长者优先，繁忙，中风险)",
        "14:00 - 16:00 (幼儿优先，适中，低风险)",
        "16:00 - 18:00 (幼儿优先，空闲，低风险)"
    ]
    time_slot = st.radio("选择可用时段 (AIGC动态风控已接入)", time_slot_options)
    
    st.divider()
    
    # 4. 提交按钮与动态计算动画 (模拟AIGC风控)
    if st.button("立即预约 🚀", use_container_width=True, type="primary"):
        # 记录用户选择
        st.session_state.service = selected_service
        st.session_state.time_slot = time_slot
        
        # 模拟 AIGC 动态定价演算过程（融入PROC GLM等效逻辑）
        with st.spinner('正在连接 AIGC 风控中台 (SAS+Python+PROC GLM) 计算动态价格与风险...'):
            time.sleep(1.5)  # 模拟网络延迟
            
            # 简单的模拟计价逻辑 (贴合风险矩阵)
            multiplier = 1.0
            risk_status = "正常"
            if "繁忙" in time_slot or "中风险" in time_slot:
                multiplier = 1.25  # 高峰溢价，防挤兑
                risk_status = "高风险：触发溢价与限流"
            elif "空闲" in time_slot or "低风险" in time_slot:
                multiplier = 0.85  # 闲时折扣，促进复用
                risk_status = "低风险：闲时折扣"
            
            st.session_state.price = base_price * multiplier
            st.session_state.risk_status = risk_status
            st.session_state.page = 'success'
            st.rerun()

# ==========================================
# 页面 2：预约成功（凭证页，强调社会价值与扩展）
# ==========================================
def render_success():
    st.success("🎉 预约成功！")
    st.markdown("### 您的家庭数字服务凭证 (试点月复购率72%)")
    
    # 凭证卡片 (家庭视角)
    family_info = ", ".join(st.session_state.family_members)
    st.info(f"""
    **👤 家庭成员**：{family_info}
    **📦 预约项目**：{st.session_state.service}
    **⏰ 预约时段**：{st.session_state.time_slot}
    **🛡️ 风险状态**：{st.session_state.risk_status} (应急预案全覆盖，商业保险支持)
    """)
    
    # 价格展示 (突出 AIGC 定价效果)
    st.metric(label="最终核销金额 (AIGC动态计价)", value=f"￥{st.session_state.price:.2f}")
    
    if st.session_state.price % 10 != 0:  # 如果触发了非整数的溢价/折扣
        st.caption("📈 *注：当前时段已触发 AIGC 动态定价风控模型调节，基于数据底座量化模拟。*")
    
    st.divider()
    
    # 模拟生成的核销码
    st.markdown("<p style='text-align: center; color: gray;'>核销码：YYQLT-" + str(random.randint(10000, 99999)) + "</p>", unsafe_allow_html=True)
    
    # 社会价值提示 (贴合愿景)
    st.markdown("**社会价值**：您的预约助力重塑家庭代际连接，5年内惠及10万家庭，社会价值超5000万元。扩展中：广西区域、全国+东盟 (SaaS授权)")
    
    if st.button("返回首页", use_container_width=True):
        st.session_state.page = 'home'
        st.session_state.family_members = []  # 重置家庭成员
        st.rerun()

# ==========================================
# 路由控制
# ==========================================
if st.session_state.page == 'home':
    render_home()
elif st.session_state.page == 'success':
    render_success()
