import streamlit as st
import pandas as pd
import os

# --- 1. 页面配置 ---
st.set_page_config(page_title="2026 汽车销售系统", page_icon="🏆", layout="centered")

# --- 2. 数据管理函数 ---
DATA_FILE = "sales_data.csv"

def init_data():
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=["日期", "销售员", "客户姓名", "车牌号", "车型", "成本价", "售价", "利润"])
        df.to_csv(DATA_FILE, index=False)

def load_data():
    init_data()
    return pd.read_csv(DATA_FILE)

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# --- 3. 现代化 CSS 样式 ---
def local_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
        
        html, body, [class*="css"]  {
            font-family: 'Inter', sans-serif;
            background-color: #f4f7fa;
        }

        /* 隐藏默认菜单 */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* 登录卡片美化 */
        .login-box {
            background: white;
            padding: 2.5rem;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.08);
            text-align: center;
            margin-bottom: 2rem;
        }
        
        /* 排行榜区域美化 */
        .ranking-container {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-top: 20px;
        }
        
        .rank-card {
            background: white;
            border-radius: 15px;
            padding: 15px;
            width: 120px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.05);
            border: 1px solid #e0e0e0;
            transition: transform 0.2s;
        }
        .rank-card:hover { transform: translateY(-5px); }
        
        .rank-1 { border-top: 4px solid #FFD700; } /* 金 */
        .rank-2 { border-top: 4px solid #C0C0C0; } /* 银 */
        .rank-3 { border-top: 4px solid #CD7F32; } /* 铜 */
        
        .rank-pos { font-size: 24px; font-weight: 800; margin-bottom: 5px; }
        .rank-name { font-weight: 600; color: #333; font-size: 14px; }
        .rank-stat { font-size: 12px; color: #666; margin-top: 5px; }
        
        h1 { color: #1f2937; font-weight: 800; letter-spacing: -1px; }
        </style>
    """, unsafe_allow_html=True)

# --- 4. 销冠排行榜组件 ---
def show_rankings():
    df = load_data()
    
    st.markdown("### 🏆 本月销冠荣耀榜")
    
    if df.empty:
        st.info("暂无销售数据，快去录入第一单吧！")
        return

    # 按销售员分组统计
    stats = df.groupby("销售员").agg(
        总销量=("销售员", "count"),
        总利润=("利润", "sum")
    ).reset_index()

    # 综合评分排序 (这里我们主要按销量排，销量一样按利润排)
    stats = stats.sort_values(by=["总销量", "总利润"], ascending=False)
    
    # 取前三名
    top_3 = stats.head(3)
    
    # 如果不足3人，补全空位以免界面错位
    while len(top_3) < 3:
        top_3 = pd.concat([top_3, pd.DataFrame([{"销售员": "暂无", "总销量": 0, "总利润": 0}])], ignore_index=True)

    # 定义奖杯图标
    medals = ["🥇", "🥈", "🥉"]
    classes = ["rank-1", "rank-2", "rank-3"]

    # 使用HTML列布局展示
    cols = st.columns(3)
    for i, row in top_3.iterrows():
        with cols[i]:
            # 使用HTML渲染卡片
            st.markdown(f"""
                <div class="rank-card {classes[i]}">
                    <div class="rank-pos">{medals[i]} No.{i+1}</div>
                    <div class="rank-name">{row['销售员']}</div>
                    <div class="rank-stat">销量: {int(row['总销量'])} 台</div>
                    <div class="rank-stat">利润: ¥{int(row['总利润']):,}</div>
                </div>
            """, unsafe_allow_html=True)

# --- 5. 登录页面 ---
def login_screen():
    local_css() # 加载样式
    
    # 页面标题
    st.markdown("<h1 style='text-align: center; margin-top: 2rem;'>🚗 汽车销售管理系统</h1>", unsafe_allow_html=True)
    
    # 居中登录框
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container():
            st.markdown('<div class="login-box">', unsafe_allow_html=True)
            st.subheader("员工登录")
            
            username = st.text_input("工号/用户名", placeholder="请输入 admin")
            password = st.text_input("密码", type="password", placeholder="请输入 123456")
            
            login_btn = st.button("立即登录", use_container_width=True)
            
            if login_btn:
                if username == "admin" and password == "123456":
                    st.session_state['logged_in'] = True
                    st.rerun()
                else:
                    st.error("账号或密码错误！")
            
            st.markdown('</div>', unsafe_allow_html=True)

    # 在登录框下方展示排行榜
    show_rankings()

# --- 6. 主应用页面 ---
def main_app():
    # 侧边栏
    with st.sidebar:
        st.header("🛠️ 导航菜单")
        page = st.radio("切换页面", ["📊 数据总览", "📝 录入新订单"])
        
        st.divider()
        if st.button("退出登录"):
            st.session_state['logged_in'] = False
            st.rerun()

    df = load_data()

    # --- 录入页面 ---
    if page == "📝 录入新订单":
        st.subheader("📝 录入新订单")
        
        # 使用表单和列布局让录入更好看
        with st.form("sales_form"):
            c1, c2 = st.columns(2)
            with c1:
                seller = st.text_input("销售员姓名", value="admin") # 默认当前登录用户
                customer = st.text_input("客户姓名")
                model = st.text_input("车型 (如 Model Y)")
                plate = st.text_input("车牌号")
            with c2:
                cost = st.number_input("成本价 (¥)", min_value=0, step=1000)
                price = st.number_input("售价 (¥)", min_value=0, step=1000)
                date = st.date_input("销售日期")
            
            # 自动计算利润
            profit = price - cost
            st.info(f"💰 预计利润: **¥{profit:,.2f}**")
            
            submitted = st.form_submit_button("💾 保存订单")
            if submitted:
                if customer and model:
                    new_data = pd.DataFrame([{
                        "日期": date,
                        "销售员": seller,
                        "客户姓名": customer,
                        "车牌号": plate,
                        "车型": model,
                        "成本价": cost,
                        "售价": price,
                        "利润": profit
                    }])
                    df = pd.concat([df, new_data], ignore_index=True)
                    save_data(df)
                    st.success("订单录入成功！")
                    st.rerun()
                else:
                    st.warning("请填写必填项")

    # --- 数据总览页面 ---
    else:
        st.subheader("📊 销售数据总览")
        
        if not df.empty:
            # 顶部关键指标
            m1, m2, m3 = st.columns(3)
            m1.metric("总销量", f"{len(df)} 台")
            m2.metric("总营收", f"¥{df['售价'].sum():,.0f}")
            m3.metric("总利润", f"¥{df['利润'].sum():,.0f}", delta_color="normal")
            
            st.divider()
            
            # 数据表格
            st.dataframe(
                df.sort_values(by="日期", ascending=False),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("暂无数据")

# --- 7. 程序入口 ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if st.session_state['logged_in']:
    main_app()
else:
    login_screen()
