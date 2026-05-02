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
    initial_sidebar_state="collapsed"
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

# ---------------- UI 样式 (已修复注释) ----------------
def local_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@400;500;600;700&display=swap');

        * {
            font-family: 'Inter', 'Space Grotesk', -apple-system, sans-serif;
        }

        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* 动态弥散光背景 */
        .stApp {
            background: #0a0a0f;
            position: relative;
            overflow: hidden;
        }

        .stApp::before {
            content: '';
            position: fixed;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background:
                radial-gradient(ellipse at 20% 50%, rgba(236, 72, 153, 0.12) 0%, transparent 50%),
                radial-gradient(ellipse at 80% 20%, rgba(99, 102, 241, 0.1) 0%, transparent 50%),
                radial-gradient(ellipse at 50% 80%, rgba(6, 182, 212, 0.08) 0%, transparent 50%);
            animation: bgShift 20s ease-in-out infinite;
            z-index: 0;
            pointer-events: none;
        }

        @keyframes bgShift {
            0%, 100% { transform: translate(0, 0) rotate(0deg); }
            33% { transform: translate(2%, -1%) rotate(1deg); }
            66% { transform: translate(-1%, 1%) rotate(-1deg); }
        }

        /* Bento Box 主容器 */
        .bento-container {
            position: relative;
            z-index: 1;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 20px;
            max-width: 1100px;
            margin: 0 auto;
            padding: 20px;
        }

        /* 液态玻璃卡片 */
        .glass-bento {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(40px) saturate(180%);
            -webkit-backdrop-filter: blur(40px) saturate(180%);
            border-radius: 28px;
            padding: 32px 28px;
            border: 1px solid rgba(255, 255, 255, 0.06);
            box-shadow:
                0 8px 32px rgba(0, 0, 0, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.04);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }

        .glass-bento::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 1px;
            background: linear-gradient(90deg,
                transparent,
                rgba(255, 255, 255, 0.1),
                transparent
            );
        }

        .glass-bento:hover {
            border-color: rgba(255, 255, 255, 0.12);
            box-shadow:
                0 12px 48px rgba(0, 0, 0, 0.4),
                inset 0 1px 0 rgba(255, 255, 255, 0.06);
            transform: translateY(-2px);
        }

        /* 电光粉渐变标题 */
        .hero-title {
            font-family: 'Space Grotesk', 'Inter', sans-serif;
            font-size: clamp(28px, 5vw, 40px);
            font-weight: 800;
            background: linear-gradient(135deg, #f472b6 0%, #ec4899 25%, #a855f7 50%, #6366f1 75%, #3b82f6 100%);
            background-size: 200% 200%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: gradientFlow 6s ease infinite;
            letter-spacing: -1px;
            line-height: 1.2;
        }

        @keyframes gradientFlow {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }

        .hero-subtitle {
            font-family: 'Space Grotesk', sans-serif;
            font-size: clamp(12px, 1.5vw, 14px);
            color: rgba(255, 255, 255, 0.3);
            font-weight: 500;
            letter-spacing: 4px;
            text-transform: uppercase;
            margin-top: 4px;
        }

        /* 领奖台 2026 */
        .podium-2026 {
            display: flex;
            justify-content: center;
            align-items: flex-end;
            gap: 16px;
            flex-wrap: wrap;
            padding: 10px 0;
        }

        .podium-card-2026 {
            flex: 1 1 110px;
            max-width: 140px;
            border-radius: 20px;
            padding: 24px 14px 18px;
            text-align: center;
            position: relative;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            cursor: default;
        }

        .podium-card-2026:hover {
            transform: translateY(-10px);
        }

        /* 冠军 - 电光金 */
        .podium-champion {
            background: linear-gradient(180deg,
                rgba(251, 191, 36, 0.15) 0%,
                rgba(245, 158, 11, 0.06) 100%);
            border: 1.5px solid rgba(251, 191, 36, 0.4);
            box-shadow:
                0 8px 40px rgba(251, 191, 36, 0.2),
                0 0 80px rgba(251, 191, 36, 0.05);
            padding-top: 32px;
            padding-bottom: 28px;
            z-index: 3;
        }

        .podium-champion .crown-glow {
            font-size: 36px;
            filter: drop-shadow(0 0 20px rgba(251, 191, 36, 0.8));
            animation: crownFloat 3s ease-in-out infinite;
        }

        @keyframes crownFloat {
            0%, 100% { transform: translateY(0) scale(1); }
            50% { transform: translateY(-10px) scale(1.1); }
        }

        /* 亚军 - 液态银 */
        .podium-runnerup {
            background: linear-gradient(180deg,
                rgba(192, 192, 192, 0.1) 0%,
                rgba(148, 163, 184, 0.05) 100%);
            border: 1.5px solid rgba(192, 192, 192, 0.25);
            box-shadow: 0 6px 30px rgba(192, 192, 192, 0.08);
            z-index: 2;
        }

        /* 季军 - 琥珀铜 */
        .podium-third {
            background: linear-gradient(180deg,
                rgba(205, 127, 50, 0.1) 0%,
                rgba(180, 83, 9, 0.05) 100%);
            border: 1.5px solid rgba(205, 127, 50, 0.25);
            box-shadow: 0 6px 30px rgba(205, 127, 50, 0.08);
            z-index: 1;
        }

        .rank-circle {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            font-weight: 800;
            font-size: 16px;
            color: white;
            margin-bottom: 12px;
        }

        .podium-champion .rank-circle {
            background: linear-gradient(135deg, #fbbf24, #f59e0b);
            box-shadow: 0 0 30px rgba(251, 191, 36, 0.6);
        }

        .podium-runnerup .rank-circle {
            background: linear-gradient(135deg, #cbd5e1, #94a3b8);
            box-shadow: 0 0 20px rgba(148, 163, 184, 0.3);
        }

        .podium-third .rank-circle {
            background: linear-gradient(135deg, #cd7f32, #a0522d);
            box-shadow: 0 0 20px rgba(205, 127, 50, 0.3);
        }

        .podium-name {
            display: block;
            font-size: clamp(13px, 2vw, 16px);
            font-weight: 700;
            color: white;
            margin: 8px 0 6px;
            letter-spacing: 0.5px;
        }

        .podium-number {
            display: block;
            font-size: clamp(22px, 3.5vw, 30px);
            font-weight: 900;
            color: rgba(255, 255, 255, 0.95);
            font-family: 'Space Grotesk', sans-serif;
        }

        .podium-label {
            display: block;
            font-size: 11px;
            color: rgba(255, 255, 255, 0.35);
            font-weight: 500;
            margin-top: 4px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        /* 输入框液态风格 */
        .stTextInput > div > div > input {
            background: rgba(255, 255, 255, 0.04) !important;
            border: 1.5px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 14px !important;
            color: white !important;
            padding: 14px 18px !important;
            font-size: 15px !important;
            transition: all 0.3s ease !important;
            backdrop-filter: blur(10px) !important;
        }

        .stTextInput > div > div > input:focus {
            border-color: #ec4899 !important;
            box-shadow: 0 0 0 3px rgba(236, 72, 153, 0.15), 0 0 30px rgba(236, 72, 153, 0.08) !important;
            background: rgba(255, 255, 255, 0.06) !important;
        }

        .stTextInput > div > div > input::placeholder {
            color: rgba(255, 255, 255, 0.2) !important;
        }

        /* Streamlit 按钮覆盖 */
        .stButton > button {
            width: 100% !important;
            border-radius: 16px !important;
            height: 52px !important;
            font-weight: 700 !important;
            font-size: 16px !important;
            letter-spacing: 0.5px !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }

        /* 响应式 */
        @media (max-width: 768px) {
            .bento-container {
                grid-template-columns: 1fr;
                padding: 12px;
                gap: 14px;
            }
            .glass-bento {
                padding: 24px 18px;
                border-radius: 22px;
            }
            .podium-2026 {
                flex-direction: column;
                align-items: center;
                gap: 12px;
            }
            .podium-card-2026 {
                max-width: 220px;
                width: 85%;
            }
        }

        @media (max-width: 480px) {
            .hero-title {
                font-size: 24px;
            }
            .glass-bento {
                padding: 20px 14px;
                border-radius: 18px;
            }
        }
    </style>
    """, unsafe_allow_html=True)

# ---------------- 销冠排行榜 ----------------
def show_champions():
    df = load_data()
    if df.empty:
        st.info(f"💡 {t('no_data')}")
        return

    stats = (
        df.groupby("销售员")
        .agg(销量=("车型", "count"), 总利润=("利润", "sum"))
        .reset_index()
        .sort_values(by="销量", ascending=False)
    )
    top3 = stats.head(3)

    st.markdown(f"""
        <div style="text-align:center; margin-bottom:20px;">
            <span style="font-size: clamp(16px, 2.5vw, 20px); font-weight: 700; color: rgba(255,255,255,0.85); letter-spacing: 1px;">
                {t('champion_title')}
            </span>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="podium-2026">', unsafe_allow_html=True)

    # 亚军
    if len(top3) > 1:
        s = top3.iloc[1]
        st.markdown(f"""
        <div class="podium-card-2026 podium-runnerup">
            <div class="rank-circle">2</div>
            <span class="podium-name">{s['销售员']}</span>
            <span class="podium-number">{int(s['销量'])}</span>
            <span class="podium-label">{t('units')}</span>
        </div>
        """, unsafe_allow_html=True)

    # 冠军
    if len(top3) > 0:
        g = top3.iloc[0]
        st.markdown(f"""
        <div class="podium-card-2026 podium-champion">
            <div class="crown-glow">👑</div>
            <span class="podium-name">{g['销售员']}</span>
            <span class="podium-number">{int(g['销量'])}</span>
            <span class="podium-label">{t('units')}</span>
        </div>
        """, unsafe_allow_html=True)

    # 季军
    if len(top3) > 2:
        b = top3.iloc[2]
        st.markdown(f"""
        <div class="podium-card-2026 podium-third">
            <div class="rank-circle">3</div>
            <span class="podium-name">{b['销售员']}</span>
            <span class="podium-number">{int(b['销量'])}</span>
            <span class="podium-label">{t('units')}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- 登录页 ----------------
def login_screen():
    # 语言切换按钮（置顶）
    lang_label = "EN" if st.session_state.language == "中文" else "中文"
    st.markdown('<div style="position:fixed; top:16px; right:20px; z-index:9999;">', unsafe_allow_html=True)
    if st.button(lang_label, key="lang_toggle"):
        st.session_state.language = "English" if st.session_state.language == "中文" else "中文"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="bento-container">', unsafe_allow_html=True)

    # 左侧登录卡片
    st.markdown(f"""
    <div class="glass-bento">
        <div class="hero-title">{t('title')}</div>
        <div class="hero-subtitle">{t('subtitle')}</div>
        <div style="margin-top: 28px;">
            <p style="color: rgba(255,255,255,0.5); font-size: 13px; font-weight: 500; letter-spacing: 1px; margin-bottom: 20px;">
                {t('login_title').upper()}
            </p>
    """, unsafe_allow_html=True)

    username = st.text_input(t("username"), placeholder=t("placeholder_user"), key="user", label_visibility="collapsed")
    password = st.text_input(t("password"), type="password", placeholder=t("placeholder_pass"), key="pass", label_visibility="collapsed")

    st.markdown("</div>", unsafe_allow_html=True)

    # 登录按钮行
    col1, col2 = st.columns([4, 1])
    with col1:
        if st.button(t("login_btn"), key="login_btn_main", use_container_width=True):
            if username == "admin" and password == "123456":
                st.session_state["logged_in"] = True
                st.rerun()
            else:
                st.error(t("error"))
    with col2:
        if st.button("⚡", key="demo_btn_quick", help=t("demo_btn"), use_container_width=True):
            generate_dummy_data()
            st.success(t("demo_success"))
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # 右侧销冠榜
    st.markdown('<div class="glass-bento">', unsafe_allow_html=True)
    show_champions()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- 后台管理 ----------------
def admin_dashboard():
    st.sidebar.markdown(f"""
        <div style="padding: 10px 0;">
            <span style="font-family: 'Space Grotesk', sans-serif; font-size: 22px; font-weight: 800;
                         background: linear-gradient(135deg, #f472b6, #a855f7);
                         -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                {t('dashboard')}
            </span>
        </div>
    """, unsafe_allow_html=True)

    menu = st.sidebar.radio("", [t("data_entry"), t("all_orders"), t("ranking")], label_visibility="collapsed")

    lang_label = "Switch to English" if st.session_state.language == "中文" else "切换到中文"
    if st.sidebar.button(lang_label, use_container_width=True):
        st.session_state.language = "English" if st.session_state.language == "中文" else "中文"
        st.rerun()

    st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
    if st.sidebar.button("🚪 退出登录", use_container_width=True):
        st.session_state["logged_in"] = False
        st.rerun()

    df = load_data()

    if menu == t("data_entry"):
        st.markdown(f'<span style="font-size:24px; font-weight:700;">{t("data_entry")}</span>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        with st.form("sales_form"):
            c1, c2 = st.columns(2)
            with c1:
                seller = st.selectbox(t("seller"),
                    ["张伟", "王芳", "李强", "刘洋", "陈静", "杨军", "赵敏", "周杰", "吴磊", "徐丽"])
                customer = st.text_input(t("customer"))
                car_model = st.text_input(t("car_model"))
            with c2:
                plate = st.text_input(t("plate"))
                cost = st.number_input(t("cost"), min_value=0, step=1000)
                price = st.number_input(t("price"), min_value=0, step=1000)

            profit = price - cost
            st.markdown(f"""
                <div style="background: rgba(236, 72, 153, 0.08); border-radius: 14px; padding: 14px 18px;
                            border: 1px solid rgba(236, 72, 153, 0.2); margin: 16px 0;">
                    <span style="color: rgba(255,255,255,0.6); font-size: 13px;">{t('expected_profit')}</span>
                    <span style="font-size: 22px; font-weight: 800; color: #f472b6; float: right;">¥{profit:,}</span>
                </div>
            """, unsafe_allow_html=True)

            if st.form_submit_button(t("save"), use_container_width=True):
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
        st.markdown(f'<span style="font-size:24px; font-weight:700;">{t("all_orders")}</span>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        if not df.empty:
            st.dataframe(df, use_container_width=True)
            st.markdown("<br>", unsafe_allow_html=True)
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric(t("total_sales"), len(df))
            with m2:
                st.metric(t("total_profit"), f"¥{df['利润'].sum():,}")
            with m3:
                st.metric(t("avg_price"), f"¥{df['售价'].mean():,.0f}")
        else:
            st.info(t("no_data"))

    elif menu == t("ranking"):
        st.markdown(f'<span style="font-size:24px; font-weight:700;">{t("ranking")}</span>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

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
