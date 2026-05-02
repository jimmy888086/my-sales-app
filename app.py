import streamlit as st
import pandas as pd
import os
import random
from datetime import datetime, timedelta

# ---------------- 页面配置（必须是第一个 Streamlit 命令）----------------
st.set_page_config(
    page_title="AutoSales Pro | 汽车销售系统",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------- 双语系统 ----------------
if "language" not in st.session_state:
    st.session_state.language = "中文"

texts = {
    "中文": {
        "title": "🚗 汽车销售管理系统",
        "subtitle": "2026 专业版",
        "login_title": "员工登录",
        "username": "工号 / 用户名",
        "password": "密码",
        "login_btn": "🔐 立即登录",
        "placeholder_user": "请输入 admin",
        "placeholder_pass": "请输入 123456",
        "error": "❌ 账号或密码错误！",
        "champion_title": "🏆 本月销冠荣耀榜",
        "gold": "🥇 销冠",
        "silver": "🥈 亚军",
        "bronze": "🥉 季军",
        "units": "台",
        "demo_btn": "🔧 生成演示数据",
        "demo_success": "✅ 已生成15条测试数据！",
        "welcome": "欢迎回来",
        "dashboard": "📊 管理后台",
        "data_entry": "📝 数据录入",
        "all_orders": "📋 所有订单",
        "ranking": "🏆 销冠排行榜",
        "total_sales": "总销量",
        "total_profit": "总利润",
        "avg_price": "平均售价",
        "save": "💾 保存订单",
        "seller": "销售员",
        "customer": "客户姓名",
        "car_model": "车型",
        "plate": "车牌号",
        "cost": "成本价",
        "price": "售价",
        "expected_profit": "预计利润",
        "no_data": "暂无销售数据",
        "stats_detail": "详细数据排名",
    },
    "English": {
        "title": "🚗 Auto Sales Management",
        "subtitle": "2026 Professional",
        "login_title": "Employee Login",
        "username": "Employee ID",
        "password": "Password",
        "login_btn": "🔐 Sign In",
        "placeholder_user": "Enter admin",
        "placeholder_pass": "Enter 123456",
        "error": "❌ Invalid credentials!",
        "champion_title": "🏆 Sales Champions",
        "gold": "🥇 Champion",
        "silver": "🥈 Runner-up",
        "bronze": "🥉 Third Place",
        "units": "units",
        "demo_btn": "🔧 Generate Demo Data",
        "demo_success": "✅ 15 demo records generated!",
        "welcome": "Welcome Back",
        "dashboard": "📊 Dashboard",
        "data_entry": "📝 Data Entry",
        "all_orders": "📋 All Orders",
        "ranking": "🏆 Leaderboard",
        "total_sales": "Total Sales",
        "total_profit": "Total Profit",
        "avg_price": "Average Price",
        "save": "💾 Save Order",
        "seller": "Salesperson",
        "customer": "Customer",
        "car_model": "Model",
        "plate": "Plate",
        "cost": "Cost",
        "price": "Price",
        "expected_profit": "Expected Profit",
        "no_data": "No data yet",
        "stats_detail": "Detailed Rankings",
    },
}

def t(key):
    return texts[st.session_state.language][key]

# ---------------- 数据管理 ----------------
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

def generate_dummy_data():
    names = ["张伟", "王芳", "李强", "刘洋", "陈静", "杨军", "赵敏", "周杰", "吴磊", "徐丽"]
    cars = [
        "Tesla Model 3", "BMW i3", "Audi A4", "Mercedes C200", "Toyota Camry",
        "Honda Accord", "Ford Mustang", "Porsche 718", "Nio ET5", "Xpeng P7",
    ]
    data = []
    for i in range(15):
        seller = random.choice(names[:5])
        if i < 5:
            seller = random.choice(["张伟", "张伟", "王芳", "王芳", random.choice(names)])
        car = random.choice(cars)
        cost = random.randint(150000, 600000)
        price = cost + random.randint(20000, 80000)
        data.append({
            "日期": (datetime.now() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d"),
            "销售员": seller,
            "客户姓名": f"客户{random.randint(1,99):02d}",
            "车牌号": f"京A{random.randint(10000,99999)}",
            "车型": car,
            "成本价": cost,
            "售价": price,
            "利润": price - cost,
        })
    df = pd.DataFrame(data)
    df.to_csv(DATA_FILE, index=False)

# ---------------- 安全兼容的 UI 样式 ----------------
def local_css():
    st.markdown("""
    <style>
        /* 基础字体与背景 */
        html, body, [class*="css"] {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            color: #e0e0e0;
        }

        .stApp {
            background-color: #0b0f19;
        }

        /* 隐藏 Streamlit 默认元素 */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* 卡片容器 */
        .card {
            background-color: rgba(20, 25, 40, 0.85);
            border-radius: 20px;
            padding: 2rem;
            margin: 1rem 0;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 4px 20px rgba(0,0,0,0.5);
        }

        /* 大标题 */
        .main-title {
            font-size: 2.2rem;
            font-weight: 800;
            background: linear-gradient(135deg, #f472b6, #a855f7, #6366f1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.2rem;
        }

        .sub-title {
            font-size: 0.9rem;
            color: #8888aa;
            letter-spacing: 2px;
            text-transform: uppercase;
        }

        /* 领奖台 */
        .podium {
            display: flex;
            justify-content: center;
            align-items: flex-end;
            gap: 1rem;
            flex-wrap: wrap;
            margin: 1.5rem 0;
        }

        .podium-item {
            background: rgba(30, 35, 50, 0.7);
            border-radius: 16px;
            padding: 1.5rem 1rem 1rem;
            text-align: center;
            min-width: 100px;
            border: 1px solid rgba(255,255,255,0.1);
            transition: transform 0.2s;
        }

        .podium-item:hover {
            transform: translateY(-5px);
        }

        .podium-gold {
            background: linear-gradient(180deg, rgba(255,215,0,0.2) 0%, rgba(255,215,0,0.05) 100%);
            border-color: rgba(255,215,0,0.4);
        }
        .podium-silver {
            background: linear-gradient(180deg, rgba(192,192,192,0.15) 0%, rgba(192,192,192,0.03) 100%);
            border-color: rgba(192,192,192,0.3);
        }
        .podium-bronze {
            background: linear-gradient(180deg, rgba(205,127,50,0.15) 0%, rgba(205,127,50,0.03) 100%);
            border-color: rgba(205,127,50,0.3);
        }

        .rank-num {
            font-size: 2rem;
            font-weight: 800;
            display: block;
        }

        .seller-name {
            font-weight: 700;
            margin: 0.5rem 0;
            color: white;
        }

        .sales-count {
            font-size: 1.5rem;
            font-weight: 800;
            color: #ccc;
        }

        /* 输入框与按钮 */
        .stTextInput>div>div>input {
            background-color: rgba(255,255,255,0.05) !important;
            border: 1px solid rgba(255,255,255,0.15) !important;
            border-radius: 12px !important;
            color: white !important;
        }
        .stButton>button {
            border-radius: 12px !important;
            font-weight: 600 !important;
            transition: all 0.2s !important;
        }
        .stButton>button:hover {
            transform: scale(1.02);
        }

        /* 响应式 */
        @media (max-width: 600px) {
            .podium {
                flex-direction: column;
                align-items: center;
            }
        }
    </style>
    """, unsafe_allow_html=True)

# ---------------- 销冠排行榜 ----------------
def show_champions():
    df = load_data()
    if df.empty:
        st.info(t("no_data"))
        return

    stats = df.groupby("销售员").agg(销量=("车型", "count")).reset_index()
    stats = stats.sort_values(by="销量", ascending=False)
    top3 = stats.head(3)

    st.markdown(f"<div style='text-align:center;font-weight:700;margin:1rem 0;'>{t('champion_title')}</div>", unsafe_allow_html=True)
    st.markdown('<div class="podium">', unsafe_allow_html=True)

    medals = ["podium-gold", "podium-silver", "podium-bronze"]
    emojis = ["👑", "🥈", "🥉"]
    for i in range(3):
        if i < len(top3):
            row = top3.iloc[i]
            name = row["销售员"]
            count = int(row["销量"])
            st.markdown(f"""
            <div class="podium-item {medals[i]}">
                <span class="rank-num">{emojis[i]}</span>
                <div class="seller-name">{name}</div>
                <div class="sales-count">{count} <small>{t('units')}</small></div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- 登录页 ----------------
def login_screen():
    # 语言切换
    lang = "EN" if st.session_state.language == "中文" else "中文"
    if st.button(lang, key="lang"):
        st.session_state.language = "English" if st.session_state.language == "中文" else "中文"
        st.rerun()

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown(f"""
        <div class="card">
            <div class="main-title">{t('title')}</div>
            <div class="sub-title">{t('subtitle')}</div>
        </div>
        """, unsafe_allow_html=True)

        username = st.text_input(t("username"), placeholder=t("placeholder_user"))
        password = st.text_input(t("password"), type="password", placeholder=t("placeholder_pass"))

        if st.button(t("login_btn"), use_container_width=True):
            if username == "admin" and password == "123456":
                st.session_state["logged_in"] = True
                st.rerun()
            else:
                st.error(t("error"))

        if st.button(t("demo_btn")):
            generate_dummy_data()
            st.success(t("demo_success"))
            st.rerun()

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        show_champions()
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------- 后台 ----------------
def admin_dashboard():
    st.sidebar.title(t("dashboard"))
    menu = st.sidebar.radio("", [t("data_entry"), t("all_orders"), t("ranking")])

    if st.sidebar.button("EN" if st.session_state.language == "中文" else "中文"):
        st.session_state.language = "English" if st.session_state.language == "中文" else "中文"
        st.rerun()
    if st.sidebar.button("🚪 退出"):
        st.session_state["logged_in"] = False
        st.rerun()

    df = load_data()

    if menu == t("data_entry"):
        st.header(t("data_entry"))
        with st.form("form"):
            c1, c2 = st.columns(2)
            with c1:
                seller = st.selectbox(t("seller"), ["张伟","王芳","李强","刘洋","陈静","杨军","赵敏","周杰","吴磊","徐丽"])
                customer = st.text_input(t("customer"))
                car_model = st.text_input(t("car_model"))
            with c2:
                plate = st.text_input(t("plate"))
                cost = st.number_input(t("cost"), min_value=0, step=1000)
                price = st.number_input(t("price"), min_value=0, step=1000)
            profit = price - cost
            st.write(f"**{t('expected_profit')}:** ¥{profit:,}")
            if st.form_submit_button(t("save")):
                new = {
                    "日期": datetime.now().strftime("%Y-%m-%d"),
                    "销售员": seller,
                    "客户姓名": customer,
                    "车牌号": plate,
                    "车型": car_model,
                    "成本价": cost,
                    "售价": price,
                    "利润": profit,
                }
                df = pd.concat([df, pd.DataFrame([new])], ignore_index=True)
                save_data(df)
                st.success("✅ 录入成功！")
                st.rerun()

    elif menu == t("all_orders"):
        st.header(t("all_orders"))
        if not df.empty:
            st.dataframe(df, use_container_width=True)
            c1, c2, c3 = st.columns(3)
            c1.metric(t("total_sales"), len(df))
            c2.metric(t("total_profit"), f"¥{df['利润'].sum():,}")
            c3.metric(t("avg_price"), f"¥{df['售价'].mean():,.0f}")
        else:
            st.info(t("no_data"))

    elif menu == t("ranking"):
        st.header(t("ranking"))
        show_champions()
        st.subheader(t("stats_detail"))
        if not df.empty:
            stats = df.groupby("销售员").agg(销量=("车型","count"), 总利润=("利润","sum")).sort_values("销量", ascending=False)
            st.dataframe(stats, use_container_width=True)

# ---------------- 主程序 ----------------
def main():
    local_css()
    init_data()
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if not st.session_state["logged_in"]:
        login_screen()
    else:
        admin_dashboard()

if __name__ == "__main__":
    main()
