import streamlit as st
import pandas as pd
import os
import random
from datetime import datetime, timedelta

# ---------------- 页面配置 ----------------
st.set_page_config(
    page_title="Auto Commission | 汽车佣金系统",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------- 双语系统 ----------------
if "language" not in st.session_state:
    st.session_state.language = "中文"

texts = {
    "中文": {
        "app_title": "Auto Commission",
        "subtitle": "EMPLOYEE CAR COMMISSION CALCULATOR",
        "top_sales": "TOP SALES · Top 3 monthly income",
        "first": "1st",
        "second": "2nd",
        "third": "3rd",
        "vehicles": "Vehicles",
        "front_desk": "Front Desk · Employee Login",
        "back_office": "Back Office · Manager Login",
        "read_only": "READ ONLY",
        "full_access": "FULL ACCESS",
        "desc": "Employees can only see their own data, while managers can control everything.",
        "independent_access": "INDEPENDENT ACCESS",
        "login": "登录",
        "username": "工号",
        "password": "密码",
        "login_btn": "进入系统",
        "error": "账号或密码错误",
        "demo_btn": "生成演示数据",
        "demo_success": "演示数据已生成！",
        "welcome": "管理后台",
        "data_entry": "数据录入",
        "all_orders": "全部订单",
        "ranking": "排行榜",
        "save": "保存订单",
        "seller": "销售员",
        "customer": "客户姓名",
        "car_model": "车型",
        "cost": "成本价",
        "price": "售价",
        "profit": "利润",
        "total_sales": "总销量",
        "total_profit": "总利润",
        "avg_price": "平均售价",
    },
    "English": {
        "app_title": "Auto Commission",
        "subtitle": "EMPLOYEE CAR COMMISSION CALCULATOR",
        "top_sales": "TOP SALES · Top 3 monthly income",
        "first": "1st",
        "second": "2nd",
        "third": "3rd",
        "vehicles": "Vehicles",
        "front_desk": "Front Desk · Employee Login",
        "back_office": "Back Office · Manager Login",
        "read_only": "READ ONLY",
        "full_access": "FULL ACCESS",
        "desc": "Employees can only see their own data, while managers can control everything.",
        "independent_access": "INDEPENDENT ACCESS",
        "login": "Login",
        "username": "Employee ID",
        "password": "Password",
        "login_btn": "Enter",
        "error": "Invalid credentials",
        "demo_btn": "Generate Demo Data",
        "demo_success": "Demo data generated!",
        "welcome": "Dashboard",
        "data_entry": "Data Entry",
        "all_orders": "All Orders",
        "ranking": "Leaderboard",
        "save": "Save",
        "seller": "Salesperson",
        "customer": "Customer",
        "car_model": "Model",
        "cost": "Cost",
        "price": "Price",
        "profit": "Profit",
        "total_sales": "Total Sales",
        "total_profit": "Total Profit",
        "avg_price": "Avg Price",
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
    """生成与参考图匹配的演示数据：周敏4辆RM63100，林晓3辆RM43700，陈洁2辆RM33600"""
    base = [
        ("周敏", 4, 63100),
        ("林晓", 3, 43700),
        ("陈洁", 2, 33600),
    ]
    data = []
    for name, count, profit in base:
        for i in range(count):
            cost = random.randint(100000, 200000)
            price = cost + profit // count + random.randint(-2000, 2000)
            data.append({
                "日期": (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d"),
                "销售员": name,
                "客户姓名": f"客户{random.randint(1,99):02d}",
                "车牌号": f"京A{random.randint(10000,99999)}",
                "车型": random.choice(["Tesla Model 3", "BMW i3", "Mercedes C200"]),
                "成本价": cost,
                "售价": price,
                "利润": price - cost,
            })
    # 补充随机的其他销售员数据
    others = ["张伟", "王芳", "李强", "刘洋"]
    for _ in range(6):
        seller = random.choice(others)
        cost = random.randint(150000, 500000)
        price = cost + random.randint(10000, 40000)
        data.append({
            "日期": (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d"),
            "销售员": seller,
            "客户姓名": f"客户{random.randint(1,99):02d}",
            "车牌号": f"京A{random.randint(10000,99999)}",
            "车型": random.choice(["Toyota Camry", "Honda Accord", "Ford Mustang"]),
            "成本价": cost,
            "售价": price,
            "利润": price - cost,
        })
    df = pd.DataFrame(data)
    df.to_csv(DATA_FILE, index=False)

# ---------------- UI 样式（复刻参考图）----------------
def local_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
        * { font-family: 'Inter', sans-serif; }
        #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}

        .stApp {
            background: linear-gradient(135deg, #0d1117 0%, #161b22 100%);
        }

        /* 整体容器 */
        .main-container {
            max-width: 1000px;
            margin: 0 auto;
            padding: 2rem 1rem;
        }

        /* 标题区 */
        .app-title {
            font-size: 3.5rem;
            font-weight: 800;
            text-align: center;
            letter-spacing: 2px;
            background: linear-gradient(180deg, #f0c040 0%, #c88800 80%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0;
        }
        .app-subtitle {
            text-align: center;
            color: #b0a080;
            font-size: 0.9rem;
            letter-spacing: 4px;
            font-weight: 500;
            margin-top: 0.2rem;
        }

        /* TOP SALES 区域 */
        .top-sales-title {
            text-align: center;
            font-size: 1.3rem;
            font-weight: 700;
            color: #d4af37;
            margin: 2rem 0 1rem;
            letter-spacing: 2px;
        }

        .podium-container {
            display: flex;
            justify-content: center;
            gap: 1.2rem;
            flex-wrap: wrap;
            margin-bottom: 2rem;
        }

        .podium-card {
            background: linear-gradient(145deg, #1a1f2b, #0e1218);
            border: 1px solid #2a2f3a;
            border-radius: 16px;
            padding: 1.5rem 1.2rem 1rem;
            text-align: center;
            width: 180px;
            position: relative;
            transition: all 0.3s;
        }
        .podium-card:hover {
            transform: translateY(-5px);
            border-color: #d4af37;
            box-shadow: 0 10px 25px rgba(212, 175, 55, 0.15);
        }

        .rank-badge {
            font-size: 2rem;
            font-weight: 800;
            color: #d4af37;
            margin-bottom: 0.2rem;
        }
        .name {
            font-size: 1.2rem;
            font-weight: 700;
            color: #ffffff;
            margin: 0.3rem 0;
        }
        .stats {
            font-size: 0.9rem;
            color: #9099a8;
        }
        .income {
            font-size: 1.4rem;
            font-weight: 800;
            color: #d4af37;
            margin-top: 0.4rem;
        }

        /* 登录入口卡片 */
        .login-cards {
            display: flex;
            justify-content: center;
            gap: 2rem;
            flex-wrap: wrap;
            margin: 2rem 0;
        }

        .login-card {
            background: linear-gradient(145deg, #1a1f2b, #0e1218);
            border: 1px solid #2a2f3a;
            border-radius: 16px;
            padding: 1.5rem;
            width: 280px;
            cursor: pointer;
            transition: all 0.3s;
            text-align: center;
        }
        .login-card:hover {
            border-color: #d4af37;
            box-shadow: 0 8px 20px rgba(212, 175, 55, 0.2);
        }
        .login-card-title {
            font-size: 1.2rem;
            font-weight: 700;
            color: #ffffff;
        }
        .login-card-role {
            font-size: 0.75rem;
            color: #d4af37;
            letter-spacing: 2px;
            font-weight: 600;
            margin: 0.3rem 0;
        }
        .login-card-desc {
            font-size: 0.8rem;
            color: #9099a8;
            margin-top: 0.5rem;
        }

        /* 描述文字 */
        .desc-text {
            text-align: center;
            color: #707580;
            font-size: 0.8rem;
            max-width: 500px;
            margin: 1rem auto;
        }

        /* 语言切换按钮 */
        .lang-switch {
            text-align: right;
            margin-bottom: 1rem;
        }
        .lang-switch button {
            background: rgba(255,255,255,0.05);
            border: 1px solid #333;
            color: #ccc;
            padding: 0.3rem 1rem;
            border-radius: 20px;
            font-weight: 600;
            cursor: pointer;
        }

        /* 表单元素样式 */
        .stTextInput > div > div > input {
            background-color: rgba(255,255,255,0.05) !important;
            border: 1px solid #333 !important;
            border-radius: 10px !important;
            color: white !important;
        }
        .stButton > button {
            background: linear-gradient(135deg, #d4af37, #b8920a) !important;
            color: #0d1117 !important;
            border: none !important;
            font-weight: 700 !important;
            border-radius: 10px !important;
            transition: all 0.3s !important;
        }
        .stButton > button:hover {
            transform: scale(1.02);
            box-shadow: 0 5px 15px rgba(212, 175, 55, 0.3);
        }

        @media (max-width: 600px) {
            .app-title { font-size: 2.5rem; }
            .podium-container { flex-direction: column; align-items: center; }
        }
    </style>
    """, unsafe_allow_html=True)

# ---------------- 显示 TOP3 销售榜 ----------------
def show_top_sales():
    df = load_data()
    if df.empty:
        return None  # 无数据
    stats = df.groupby("销售员").agg(
        销量=("车型", "count"),
        总利润=("利润", "sum")
    ).reset_index().sort_values(by="总利润", ascending=False)
    return stats.head(3)

def render_top_sales():
    top3 = show_top_sales()
    if top3 is None or len(top3) == 0:
        st.info("暂无销售数据")
        return

    st.markdown(f"<div class='top-sales-title'>{t('top_sales')}</div>", unsafe_allow_html=True)
    st.markdown("<div class='podium-container'>", unsafe_allow_html=True)

    medals = ["1st", "2nd", "3rd"]
    for i in range(3):
        if i < len(top3):
            row = top3.iloc[i]
            name = row["销售员"]
            vehicles = int(row["销量"])
            income = row["总利润"]
            # 格式化收入为 RM xxx,xxx.00
            income_str = f"RM{income:,.2f}"
            st.markdown(f"""
            <div class="podium-card">
                <div class="rank-badge">{medals[i]} · {vehicles} {t('vehicles')}</div>
                <div class="name">{name}</div>
                <div class="income">{income_str}</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- 登录页（复刻参考图）----------------
def login_screen():
    # 语言切换
    col_lang, _ = st.columns([1, 4])
    with col_lang:
        lang_label = "EN" if st.session_state.language == "中文" else "中文"
        if st.button(lang_label, key="lang_toggle"):
            st.session_state.language = "English" if st.session_state.language == "中文" else "中文"
            st.rerun()

    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    # 标题
    st.markdown(f'<div class="app-title">{t("app_title")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="app-subtitle">{t("subtitle")}</div>', unsafe_allow_html=True)

    # 演示数据生成按钮
    col_demo, _ = st.columns([1, 4])
    with col_demo:
        if st.button(t("demo_btn")):
            generate_dummy_data()
            st.success(t("demo_success"))
            st.rerun()

    # TOP SALES 区域
    render_top_sales()

    # 说明文字
    st.markdown(f'<div class="desc-text">{t("desc")}</div>', unsafe_allow_html=True)

    # 两个登录入口卡片
    st.markdown('<div class="login-cards">', unsafe_allow_html=True)

    # 员工登录卡片
    if "login_role" not in st.session_state:
        st.session_state.login_role = None

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="login-card" id="employee-card">
            <div class="login-card-title">{t("front_desk")}</div>
            <div class="login-card-role">{t("read_only")}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(t("front_desk"), key="btn_employee"):
            st.session_state.login_role = "employee"

    with col2:
        st.markdown(f"""
        <div class="login-card" id="manager-card">
            <div class="login-card-title">{t("back_office")}</div>
            <div class="login-card-role">{t("full_access")}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(t("back_office"), key="btn_manager"):
            st.session_state.login_role = "manager"

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 如果点击了某个卡片，显示对应的登录表单
    if st.session_state.login_role:
        st.markdown("---")
        with st.container():
            role = st.session_state.login_role
            st.subheader(f"{'🔒' if role == 'employee' else '🔑'} {t(role)} {t('login')}")
            username = st.text_input(t("username"), key=f"user_{role}")
            password = st.text_input(t("password"), type="password", key=f"pass_{role}")
            if st.button(t("login_btn"), key=f"login_{role}"):
                # 暂时简单判断：管理员账号 admin/123456，员工账号 employee/123456
                if role == "manager" and username == "admin" and password == "123456":
                    st.session_state["logged_in"] = True
                    st.session_state["is_manager"] = True
                    st.rerun()
                elif role == "employee" and username == "employee" and password == "123456":
                    st.session_state["logged_in"] = True
                    st.session_state["is_manager"] = False
                    st.rerun()
                else:
                    st.error(t("error"))

        # 取消选择
        if st.button("↩️ 返回"):
            st.session_state.login_role = None
            st.rerun()

# ---------------- 后台管理 ----------------
def admin_dashboard():
    is_manager = st.session_state.get("is_manager", False)
    st.sidebar.title("💰 " + t("welcome"))

    menu = st.sidebar.radio("", [t("data_entry"), t("all_orders"), t("ranking")])

    if st.sidebar.button("🌐  EN" if st.session_state.language == "中文" else "🌐  中文"):
        st.session_state.language = "English" if st.session_state.language == "中文" else "中文"
        st.rerun()
    if st.sidebar.button("🚪 退出"):
        st.session_state["logged_in"] = False
        st.session_state.login_role = None
        st.rerun()

    if not is_manager:
        st.warning("您当前是员工权限，仅可查看自己的数据（演示模式）。")

    df = load_data()
    # 如果员工，过滤数据只显示 employee（这里演示为“员工”通用账号，暂时不作过滤）
    if menu == t("data_entry"):
        if not is_manager:
            st.error("只读权限，无权录入数据")
        else:
            st.header(t("data_entry"))
            with st.form("form"):
                c1, c2 = st.columns(2)
                with c1:
                    seller = st.selectbox(t("seller"), ["周敏","林晓","陈洁","张伟","王芳","李强","刘洋"])
                    customer = st.text_input(t("customer"))
                    car_model = st.text_input(t("car_model"))
                with c2:
                    cost = st.number_input(t("cost"), min_value=0, step=1000)
                    price = st.number_input(t("price"), min_value=0, step=1000)
                profit = price - cost
                st.write(f"**{t('profit')}:** RM{profit:,.2f}")
                if st.form_submit_button(t("save")):
                    new = {
                        "日期": datetime.now().strftime("%Y-%m-%d"),
                        "销售员": seller,
                        "客户姓名": customer or "未知",
                        "车牌号": "N/A",
                        "车型": car_model or "未知",
                        "成本价": cost,
                        "售价": price,
                        "利润": profit,
                    }
                    df = pd.concat([df, pd.DataFrame([new])], ignore_index=True)
                    save_data(df)
                    st.success("✅ 保存成功")
                    st.rerun()

    elif menu == t("all_orders"):
        st.header(t("all_orders"))
        if not df.empty:
            st.dataframe(df, use_container_width=True)
            c1, c2, c3 = st.columns(3)
            c1.metric(t("total_sales"), len(df))
            c2.metric(t("total_profit"), f"RM{df['利润'].sum():,.2f}")
            c3.metric(t("avg_price"), f"RM{df['售价'].mean():,.0f}")
        else:
            st.info("暂无数据")

    elif menu == t("ranking"):
        st.header(t("ranking"))
        render_top_sales()
        if not df.empty:
            stats = df.groupby("销售员").agg(
                销量=("车型","count"),
                总利润=("利润","sum")
            ).sort_values("总利润", ascending=False)
            st.dataframe(stats, use_container_width=True)

# ---------------- 主程序 ----------------
def main():
    local_css()
    init_data()
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "is_manager" not in st.session_state:
        st.session_state["is_manager"] = True  # 默认管理员

    if not st.session_state["logged_in"]:
        login_screen()
    else:
        admin_dashboard()

if __name__ == "__main__":
    main()
