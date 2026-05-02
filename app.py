import streamlit as st
import pandas as pd
import os
import random
from datetime import datetime, timedelta

# ---------------- 页面配置 ----------------
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
        "demo_btn": "🔧 生成演示数据 (测试)",
        "demo_success": "✅ 已生成15条测试数据！请刷新页面查看销冠。",
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
        "username": "Employee ID / Username",
        "password": "Password",
        "login_btn": "🔐 Sign In",
        "placeholder_user": "Enter admin",
        "placeholder_pass": "Enter 123456",
        "error": "❌ Invalid credentials!",
        "champion_title": "🏆 Sales Champions of the Month",
        "gold": "🥇 Champion",
        "silver": "🥈 Runner-up",
        "bronze": "🥉 Third Place",
        "units": "units",
        "demo_btn": "🔧 Generate Demo Data",
        "demo_success": "✅ 15 demo records generated! Refresh to see champions.",
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
        "customer": "Customer Name",
        "car_model": "Car Model",
        "plate": "License Plate",
        "cost": "Cost Price",
        "price": "Selling Price",
        "expected_profit": "Expected Profit",
        "no_data": "No sales data yet",
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
        data.append(
            {
                "日期": (datetime.now() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d"),
                "销售员": seller,
                "客户姓名": f"客户{random.randint(1,99):02d}",
                "车牌号": f"京A{random.randint(10000,99999)}",
                "车型": car,
                "成本价": cost,
                "售价": price,
                "利润": price - cost,
            }
        )
    df = pd.DataFrame(data)
    df.to_csv(DATA_FILE, index=False)

# ---------------- UI 样式 (响应式) ----------------
def local_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* 主背景 */
        .stApp {
            background: linear-gradient(135deg, #0a0e27 0%, #1a1a3e 50%, #0d1117 100%);
        }

        /* 玻璃卡片（自适应） */
        .glass-card {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-radius: 24px;
            padding: clamp(20px, 5vw, 40px) clamp(15px, 4vw, 35px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.05);
            position: relative;
            z-index: 1;
            width: 100%;
            max-width: 500px;
            margin: 0 auto;
        }

        .main-title {
            font-size: clamp(24px, 5vw, 32px);
            font-weight: 800;
            background: linear-gradient(135deg, #6366f1, #8b5cf6, #3b82f6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 5px;
            letter-spacing: -0.5px;
        }

        .subtitle {
            font-size: clamp(12px, 2vw, 14px);
            color: rgba(255, 255, 255, 0.4);
            font-weight: 300;
            letter-spacing: 2px;
            text-transform: uppercase;
        }

        /* 领奖台容器 */
        .champion-section {
            background: rgba(255, 255, 255, 0.02);
            border-radius: 24px;
            padding: 25px 15px;
            border: 1px solid rgba(255, 255, 255, 0.06);
            width: 100%;
            max-width: 600px;
            margin: 0 auto;
        }

        .champion-title {
            font-size: clamp(16px, 3vw, 18px);
            font-weight: 700;
            text-align: center;
            color: rgba(255, 255, 255, 0.9);
            margin-bottom: 20px;
            letter-spacing: 1px;
        }

        /* 领奖台弹性布局 (移动端竖向) */
        .podium-wrapper {
            display: flex;
            justify-content: center;
            align-items: flex-end;
            gap: 12px;
            flex-wrap: wrap;
        }

        .podium-card {
            flex: 1 1 100px;
            max-width: 130px;
            border-radius: 16px;
            padding: clamp(15px, 3vw, 20px) clamp(8px, 2vw, 12px) 15px;
            text-align: center;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            backdrop-filter: blur(5px);
            -webkit-backdrop-filter: blur(5px);
        }

        .podium-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
        }

        .podium-gold {
            background: linear-gradient(180deg, rgba(255, 215, 0, 0.18) 0%, rgba(255, 180, 0, 0.08) 100%);
            border: 1.5px solid rgba(255, 215, 0, 0.4);
            box-shadow: 0 8px 32px rgba(255, 215, 0, 0.2);
            padding-top: clamp(25px, 4vw, 30px);
        }

        .podium-silver {
            background: linear-gradient(180deg, rgba(192, 192, 192, 0.12) 0%, rgba(150, 150, 150, 0.06) 100%);
            border: 1.5px solid rgba(192, 192, 192, 0.3);
        }

        .podium-bronze {
            background: linear-gradient(180deg, rgba(205, 127, 50, 0.12) 0%, rgba(180, 100, 30, 0.06) 100%);
            border: 1.5px solid rgba(205, 127, 50, 0.3);
        }

        .rank-badge {
            display: inline-block;
            width: 36px;
            height: 36px;
            border-radius: 50%;
            line-height: 36px;
            font-weight: 800;
            font-size: 16px;
            margin-bottom: 10px;
            color: white;
        }

        .podium-gold .rank-badge {
            background: linear-gradient(135deg, #fbbf24, #f59e0b);
            box-shadow: 0 4px 15px rgba(251, 191, 36, 0.6);
        }

        .podium-silver .rank-badge {
            background: linear-gradient(135deg, #c0c0c0, #a0a0a0);
            box-shadow: 0 4px 12px rgba(192, 192, 192, 0.4);
        }

        .podium-bronze .rank-badge {
            background: linear-gradient(135deg, #cd7f32, #b8702e);
            box-shadow: 0 4px 12px rgba(205, 127, 50, 0.4);
        }

        .seller-name {
            display: block;
            font-size: clamp(13px, 2.5vw, 15px);
            font-weight: 700;
            color: white;
            margin: 8px 0 5px;
        }

        .sales-count {
            display: block;
            font-size: clamp(20px, 4vw, 24px);
            font-weight: 800;
            color: rgba(255, 255, 255, 0.95);
        }

        .sales-label {
            display: block;
            font-size: 11px;
            color: rgba(255, 255, 255, 0.4);
            margin-top: 2px;
        }

        /* 输入框与按钮自适应 */
        .stTextInput > div > div > input {
            background: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px !important;
            color: white !important;
            padding: 12px 16px !important;
            font-size: 14px !important;
        }

        .stTextInput > div > div > input:focus {
            border-color: #6366f1 !important;
            box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.3) !important;
        }

        .stButton > button {
            width: 100% !important;
            border-radius: 12px !important;
            height: 50px !important;
            font-weight: 700 !important;
            font-size: 16px !important;
            background: linear-gradient(135deg, #6366f1, #3b82f6) !important;
            border: none !important;
            color: white !important;
            transition: all 0.3s ease !important;
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(59, 130, 246, 0.4);
        }

        /* 语言切换按钮 */
        .lang-switch {
            position: fixed;
            top: 15px;
            right: 20px;
            z-index: 9999;
            background: rgba(255,255,255,0.06);
            backdrop-filter: blur(10px);
            border-radius: 30px;
            padding: 6px 18px;
            border: 1px solid rgba(255,255,255,0.1);
            color: white;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
        }

        /* 移动端领奖台竖向排列 */
        @media (max-width: 600px) {
            .podium-wrapper {
                flex-direction: column;
                align-items: center;
                gap: 15px;
            }
            .podium-card {
                max-width: 200px;
                width: 80%;
            }
            .glass-card {
                padding: 25px 20px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# ---------------- 销冠排行榜组件 ----------------
def show_champions():
    df = load_data()
    if df.empty:
        st.info(t("no_data"))
        return

    stats = (
        df.groupby("销售员")
        .agg(销量=("车型", "count"), 总利润=("利润", "sum"))
        .reset_index()
        .sort_values(by="销量", ascending=False)
    )
    top3 = stats.head(3)

    st.markdown(f'<div class="champion-title">{t("champion_title")}</div>', unsafe_allow_html=True)
    st.markdown('<div class="podium-wrapper">', unsafe_allow_html=True)

    # 亚军 (第二)
    if len(top3) > 1:
        silver = top3.iloc[1]
        st.markdown(
            f"""
            <div class="podium-card podium-silver">
                <div class="rank-badge">2</div>
                <span class="seller-name">{silver['销售员']}</span>
                <span class="sales-count">{int(silver['销量'])}</span>
                <span class="sales-label">{t('units')}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown('<div class="podium-card podium-silver" style="visibility:hidden;"></div>', unsafe_allow_html=True)

    # 冠军 (第一)
    if len(top3) > 0:
        gold = top3.iloc[0]
        st.markdown(
            f"""
            <div class="podium-card podium-gold">
                <div class="rank-badge">👑</div>
                <span class="seller-name">{gold['销售员']}</span>
                <span class="sales-count">{int(gold['销量'])}</span>
                <span class="sales-label">{t('units')}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # 季军 (第三)
    if len(top3) > 2:
        bronze = top3.iloc[2]
        st.markdown(
            f"""
            <div class="podium-card podium-bronze">
                <div class="rank-badge">3</div>
                <span class="seller-name">{bronze['销售员']}</span>
                <span class="sales-count">{int(bronze['销量'])}</span>
                <span class="sales-label">{t('units')}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- 登录页 ----------------
def login_screen():
    # 语言切换按钮 (固定在右上角)
    lang_label = "EN" if st.session_state.language == "中文" else "中文"
    if st.button(lang_label, key="lang_toggle"):
        st.session_state.language = "English" if st.session_state.language == "中文" else "中文"
        st.rerun()

    col1, col2 = st.columns([1, 1], gap="medium")

    with col1:
        st.markdown(
            f"""
            <div class="glass-card">
                <div class="main-title">{t('title')}</div>
                <div class="subtitle">{t('subtitle')}</div>
                <br>
                <p style="color: rgba(255,255,255,0.7); font-size: 14px;">{t('login_title')}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        # 实际的输入框在卡片外面，保持流式布局
        username = st.text_input(t("username"), placeholder=t("placeholder_user"), key="user")
        password = st.text_input(t("password"), type="password", placeholder=t("placeholder_pass"), key="pass")
        login_btn = st.button(t("login_btn"), use_container_width=True)

        if login_btn:
            if username == "admin" and password == "123456":
                st.session_state["logged_in"] = True
                st.rerun()
            else:
                st.error(t("error"))

    with col2:
        st.markdown('<div class="champion-section">', unsafe_allow_html=True)
        show_champions()
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button(t("demo_btn"), use_container_width=True):
            generate_dummy_data()
            st.success(t("demo_success"))
            st.rerun()

# ---------------- 后台管理 ----------------
def admin_dashboard():
    st.sidebar.title("👤 " + t("welcome"))
    menu = st.sidebar.radio("", [t("data_entry"), t("all_orders"), t("ranking")])

    # 语言切换
    lang_label = "Switch to English" if st.session_state.language == "中文" else "切换到中文"
    if st.sidebar.button(lang_label):
        st.session_state.language = "English" if st.session_state.language == "中文" else "中文"
        st.rerun()

    df = load_data()

    if menu == t("data_entry"):
        st.header(t("data_entry"))
        with st.form("sales_form"):
            c1, c2 = st.columns(2)
            with c1:
                seller = st.selectbox(t("seller"), ["张伟", "王芳", "李强", "刘洋", "陈静", "杨军", "赵敏", "周杰", "吴磊", "徐丽"])
                customer = st.text_input(t("customer"))
                car_model = st.text_input(t("car_model"))
            with c2:
                plate = st.text_input(t("plate"))
                cost = st.number_input(t("cost"), min_value=0, step=1000)
                price = st.number_input(t("price"), min_value=0, step=1000)
            profit = price - cost
            st.write(f"**{t('expected_profit')}:** {profit:,}")
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
            m1, m2, m3 = st.columns(3)
            m1.metric(t("total_sales"), len(df))
            m2.metric(t("total_profit"), f"{df['利润'].sum():,}")
            m3.metric(t("avg_price"), f"{df['售价'].mean():,.0f}")
        else:
            st.info(t("no_data"))

    elif menu == t("ranking"):
        st.header(t("ranking"))
        show_champions()
        st.markdown("---")
        st.subheader(t("stats_detail"))
        if not df.empty:
            stats = (
                df.groupby("销售员")
                .agg(销量=("车型", "count"), 总利润=("利润", "sum"))
                .sort_values(by="销量", ascending=False)
            )
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
