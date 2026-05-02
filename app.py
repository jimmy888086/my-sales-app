import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- 1. 页面配置 ---
st.set_page_config(page_title="汽车销售管理系统", page_icon="🚗", layout="wide")

# --- 2. 数据管理函数 ---
DATA_FILE = "sales_data.csv"

# 初始化数据文件（如果不存在则创建）
def init_data():
    if not os.path.exists(DATA_FILE):
        # 创建初始列
        df = pd.DataFrame(columns=["日期", "客户姓名", "车牌号", "车型", "成本价", "售价", "利润"])
        df.to_csv(DATA_FILE, index=False)

def load_data():
    init_data()
    return pd.read_csv(DATA_FILE)

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# --- 3. 登录验证 ---
def check_login():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if not st.session_state['logged_in']:
        st.title("🔒 管理员登录")
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            username = st.text_input("用户名")
            password = st.text_input("密码", type="password")
            if st.button("登录"):
                if username == "admin" and password == "123456":
                    st.session_state['logged_in'] = True
                    st.rerun()
                else:
                    st.error("用户名或密码错误！")
        st.stop() # 停止运行后续代码，直到登录

def logout():
    st.session_state['logged_in'] = False
    st.rerun()

# --- 4. 主程序 ---
def main():
    st.sidebar.title("🚗 AutoSales Pro")
    st.sidebar.write("欢迎使用汽车销售管理系统")
    st.sidebar.button("退出登录", on_click=logout)

    # 加载数据
    df = load_data()

    # 侧边栏导航
    menu = ["录入新订单 (后台)", "查看所有数据 (前台)"]
    choice = st.sidebar.radio("导航菜单", menu)

    # --- 页面 A: 录入新订单 ---
    if choice == "录入新订单 (后台)":
        st.header("📝 录入新销售数据")
        
        with st.form("entry_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("客户姓名")
                plate = st.text_input("车牌号")
                cost = st.number_input("成本价 (RM)", min_value=0.0, step=100.0)
            with col2:
                model = st.text_input("车型")
                price = st.number_input("售价 (RM)", min_value=0.0, step=100.0)
                date = st.date_input("日期", datetime.today())

            submitted = st.form_submit_button("💾 保存订单")
            if submitted:
                if name and plate and model:
                    # 计算利润
                    profit = price - cost
                    
                    # 创建新数据行
                    new_data = {
                        "日期": date,
                        "客户姓名": name,
                        "车牌号": plate,
                        "车型": model,
                        "成本价": cost,
                        "售价": price,
                        "利润": profit
                    }
                    
                    # 追加到现有数据
                    df_new = pd.DataFrame([new_data])
                    df_updated = pd.concat([df, df_new], ignore_index=True)
                    save_data(df_updated)
                    
                    st.success(f"成功录入！本单利润为: **{profit}**")
                else:
                    st.warning("请填写必填项（姓名、车牌、车型）")

    # --- 页面 B: 查看所有数据 ---
    elif choice == "查看所有数据 (前台)":
        st.header("📊 所有销售记录")
        
        if not df.empty:
            # 计算统计指标
            total_sales = len(df)
            total_revenue = df['售价'].sum()
            total_profit = df['利润'].sum()
            
            # 显示指标卡片
            m1, m2, m3 = st.columns(3)
            m1.metric("总销量", f"{total_sales} 台")
            m2.metric("总营收", f"RM {total_revenue:,.2f}")
            m3.metric("总利润", f"RM {total_profit:,.2f}")
            
            st.divider()
            
            # 显示数据表格
            st.dataframe(df, use_container_width=True)
            
            # 下载按钮
            @st.cache_data
            def convert_df(df):
                return df.to_csv(index=False).encode('utf-8')

            csv = convert_df(df)
            st.download_button(
                label="📥 下载数据为 CSV",
                data=csv,
                file_name='sales_data.csv',
                mime='text/csv',
            )
        else:
            st.info("暂无数据，请去后台录入。")

# --- 运行应用 ---
check_login()
main()
