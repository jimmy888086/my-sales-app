import streamlit as st
import pandas as pd
import os
import random
from datetime import datetime, timedelta

# --- 1. 页面配置 ---
st.set_page_config(page_title="2026 汽车销售系统", page_icon="🏆", layout="centered")

# --- 2. 数据管理函数 ---
DATA_FILE = "sales_data.csv"

def init_data():
    if not os.path.exists(DATA_FILE):
        # 创建空的DataFrame
        df = pd.DataFrame(columns=["日期", "销售员", "客户姓名", "车牌号", "车型", "成本价", "售价", "利润"])
        df.to_csv(DATA_FILE, index=False)

def load_data():
    init_data()
    return pd.read_csv(DATA_FILE)

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

def generate_dummy_data():
    """生成10条演示数据"""
    names = ["张伟", "王芳", "李强", "刘洋", "陈静", "杨军", "赵敏", "周杰", "吴磊", "徐丽"]
    cars = ["Tesla Model 3", "BMW i3", "Audi A4", "Mercedes C200", "Toyota Camry", "Honda Accord", "Ford Mustang", "Porsche 718", "Nio ET5", "Xpeng P7"]
    data = []
    
    # 随机生成10条数据，故意让 "张伟" 和 "王芳" 业绩高一点，方便看效果
    for i in range(15): # 生成15条，制造一些重复销售员
        seller = random.choice(names)
        # 让前两个人出现概率更高，模拟销冠
        if i < 5: seller = "张伟"
        elif i < 9: seller = "王芳"
        
        car = random.choice(cars)
        cost = random.randint(150000, 400000)
        profit = random.randint(5000, 30000)
        price = cost + profit
        
        record = {
            "日期": (datetime.now() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d"),
            "销售员": seller,
            "客户姓名": f"客户{i+1}",
            "车牌号": f"沪A·{random.randint(1000,9999)}",
            "车型": car,
            "成本价": cost,
            "售价": price,
            "利润": profit
        }
        data.append(record)
        
    df = pd.DataFrame(data)
    save_data(df)
    return df

# --- 3. 现代化 CSS 样式 ---
def local_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
        
        /* 全局设置 */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            background: #0f172a; /* 深色科技风背景 */
            color: white;
        }
        
        /* 隐藏默认菜单 */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* 登录卡片 */
        .login-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 20px 50px rgba(0,0,0,0.5);
            text-align: center;
        }
        
        /* 销冠榜单样式 */
        .podium-container {
            display: flex;
            justify-content: center;
            align-items: flex-end;
            margin-top: 30px;
            gap: 15px;
            padding-bottom: 20px;
        }
        
        .podium-item {
            background: linear-gradient(180deg, #333 0%, #111 100%);
            border-radius: 12px;
            padding: 15px;
            width: 100px;
            text-align: center;
            border: 1px solid #444;
            position: relative;
        }
        
        .podium-item.gold { border-bottom: 4px solid #FFD700; transform: scale(1.1); }
        .podium-item.silver { border-bottom: 4px solid #C0C0C0; }
        .podium-item.bronze { border-bottom: 4px solid #CD7F32; }
        
        .rank-num { font-size: 24px; font-weight: 800; display: block; margin-bottom: 5px; }
        .seller-name { font-size: 14px; font-weight: 600; color: #fff; display: block; }
        .sales-count { font-size: 12px; color: #888; margin-top: 5px; display: block; }
        
        /* 输入框美化 */
        .stTextInput > div > div > input {
            background-color: transparent;
            color: white;
            border: 1px solid #444;
            border-radius: 10px;
            padding: 10px;
        }
        .stButton > button {
            width: 100%;
            border-radius: 10px;
            height: 50px;
            font-weight: 600;
            background: linear-gradient(90deg, #3b82f6, #2563eb);
            border: none;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

# --- 4. 销冠排行榜组件 ---
def show_champions():
    df = load_data()
    
    if df.empty:
        st.info("暂无销售数据，请在后台录入或点击下方生成演示数据。")
        return

    # 计算销冠逻辑：按“销售员”分组，统计卖了多少辆车
    stats = df.groupby("销售员").agg(
        销量=("车型", "count"),
        总利润=("利润", "sum")
    ).reset_index().sort_values(by="销量", ascending=False)

    top_3 = stats.head(3)

    st.markdown("### 🏆 本月销冠荣耀榜")
    
    # 使用列布局制作奖杯台
    c1, c2, c3 = st.columns([1, 1.2, 1])
    
    # 第2名
    with c1:
        if len(top_3) > 1:
            name = top_3.iloc[1]['销售员']
            count = int(top_3.iloc[1]['销量'])
            st.markdown(f"""
            <div class="podium-item silver">
                <span class="rank-num" style="color:#C0C0C0">2</span>
                <span class="seller-name">{name}</span>
                <span class="sales-count">{count} 台</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.write("")

    # 第1名 (C位放大)
    with c2:
        if len(top_3) > 0:
            name = top_3.iloc[0]['销售员']
            count = int(top_3.iloc[0]['销量'])
            st.markdown(f"""
            <div class="podium-item gold">
                <span class="rank-num" style="color:#FFD700; font-size:32px">1</span>
                <span class="seller-name" style="color:#FFD700">{name}</span>
                <span class="sales-count" style="color:#FFF">👑 {count} 台</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.write("")

    # 第3名
    with c3:
        if len(top_3) > 2:
            name = top_3.iloc[2]['销售员']
            count = int(top_3.iloc[2]['销量'])
            st.markdown(f"""
            <div class="podium-item bronze">
                <span class="rank-num" style="color:#CD7F32">3</span>
                <span class="seller-name">{name}</span>
                <span class="sales-count">{count} 台</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.write("")

# --- 5. 登录界面 ---
def login_screen():
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="login-card" style="margin-top: 50px;">
            <h1 style="color:white; margin-bottom:10px;">🚗 汽车销售系统</h1>
            <p style="color:#aaa; font-size:14px;">请输入您的员工工号以进入管理后台</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 真正的输入框
        username = st.text_input("工号 / 用户名", placeholder="请输入 admin")
        password = st.text_input("密码", type="password", placeholder="请输入 123456")
        
        login_btn = st.button("立即登录")
        
        if login_btn:
            if username == "admin" and password == "123456":
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("账号或密码错误！")

    with col2:
        st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
        show_champions() # 在右侧显示销冠榜
        
        # 演示数据按钮
        st.markdown("---")
        if st.button("🔧 生成10条演示数据 (测试用)"):
            generate_dummy_data()
            st.success("已生成10条测试数据！请刷新页面查看销冠变化。")
            st.rerun()

# --- 6. 后台录入界面 ---
def admin_dashboard():
    st.sidebar.title("👤 管理菜单")
    menu = st.sidebar.radio("导航", ["数据录入", "所有订单", "销冠排行榜"])
    
    df = load_data()

    if menu == "数据录入":
        st.header("📝 新车销售录入")
        
        with st.form("sales_form"):
            c1, c2 = st.columns(2)
            with c1:
                seller = st.selectbox("销售员", ["张伟", "王芳", "李强", "刘洋", "陈静", "其他"])
                customer = st.text_input("客户姓名")
                car_model = st.text_input("车型 (如 Tesla Model 3)")
            with c2:
                plate = st.text_input("车牌号")
                cost = st.number_input("成本价", min_value=0, step=1000)
                price = st.number_input("售价", min_value=0, step=1000)
            
            profit = price - cost
            st.write(f"预计利润: **{profit}**")
            
            submitted = st.form_submit_button("保存订单")
            if submitted:
                new_data = {
                    "日期": datetime.now().strftime("%Y-%m-%d"),
                    "销售员": seller,
                    "客户姓名": customer,
                    "车牌号": plate,
                    "车型": car_model,
                    "成本价": cost,
                    "售价": price,
                    "利润": profit
                }
                df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
                save_data(df)
                st.success("录入成功！")
                st.rerun()

    elif menu == "所有订单":
        st.header("📊 销售数据总表")
        if not df.empty:
            # 简单的表格美化
            st.dataframe(df, use_container_width=True)
            
            # 统计指标
            m1, m2, m3 = st.columns(3)
            m1.metric("总销量", len(df))
            m2.metric("总利润", f"{df['利润'].sum():,}")
            m3.metric("平均售价", f"{df['售价'].mean():,.0f}")
        else:
            st.info("暂无数据")

    elif menu == "销冠排行榜":
        st.header("🏆 实时销冠排行榜")
        show_champions()
        st.write("---")
        st.subheader("详细数据排名")
        if not df.empty:
            stats = df.groupby("销售员").agg(
                销量=("车型", "count"),
                总利润=("利润", "sum")
            ).sort_values(by="销量", ascending=False)
            st.dataframe(stats)

# --- 7. 主程序逻辑 ---
def main():
    local_css()
    init_data()
    
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        
    if not st.session_state['logged_in']:
        login_screen()
    else:
        admin_dashboard()

if __name__ == "__main__":
    main()
