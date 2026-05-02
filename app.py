import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="AutoSales Pro",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def get_data():
    data = {
        "ID": range(1, 21),
        "Name": ["Ahmad", "Siti", "Razak", "Lee", "Wong", "Kumar", "Muthu", "Ali", "Abu", "Chong",
                 "Tan", "Lim", "Ng", "Ismail", "Hashim", "Yeoh", "Ooi", "Tan", "Liew", "Gan"],
        "Date": pd.date_range(start='2026-04-01', periods=20, freq='D'),
        "Plate": [f"W{i}A" for i in range(1, 21)],
        "Model": ["Honda Civic", "Toyota Harrier", "BMW 320i", "Mercedes C200", "VW Golf",
                  "Nissan GTR", "Ford Ranger", "Mazda 3", "Hyundai Tucson", "Kia Sportage",
                  "Honda CRV", "Toyota Alphard", "Lexus ES", "Porsche 718", "Mini Cooper",
                  "Volvo XC60", "Jeep Wrangler", "Subaru WRX", "Mitsubishi Triton", "Isuzu D-Max"],
        "Cost": np.random.randint(80000, 250000, 20),
        "Price": np.random.randint(95000, 300000, 20)
    }
    df = pd.DataFrame(data)
    df['Price'] = df.apply(lambda x: max(x['Cost'] + 5000, x['Price']), axis=1)
    df['Profit'] = df['Price'] - df['Cost']
    return df

df = get_data()

if 'lang' not in st.session_state:
    st.session_state.lang = 'en'

lang_dict = {
    'en': {
        'title': '🚀 AutoSales Dashboard Pro',
        'sidebar_title': '⚙️ Control Panel',
        'kpi_sales': 'Total Sales',
        'kpi_profit': 'Total Profit',
        'kpi_avg': 'Avg. Profit',
        'table_title': '📊 Sales Records',
        'toggle': 'Switch to Chinese',
        'chart': 'Profit Analysis'
    },
    'zh': {
        'title': '🚀 汽车销售专业仪表盘',
        'sidebar_title': '⚙️ 控制面板',
        'kpi_sales': '总销售额',
        'kpi_profit': '总利润',
        'kpi_avg': '平均利润',
        'table_title': '📊 销售记录表',
        'toggle': '切换英文',
        'chart': '利润分析图'
    }
}

def t(key):
    return lang_dict[st.session_state.lang][key]

with st.sidebar:
    st.header(t('sidebar_title'))
    if st.button(t('toggle')):
        st.session_state.lang = 'zh' if st.session_state.lang == 'en' else 'en'
        st.experimental_rerun()  # 关键修复：兼容所有Streamlit版本

st.title(t('title'))

c1, c2, c3 = st.columns(3)
total_sales = df['Price'].sum()
total_profit = df['Profit'].sum()
avg_profit = df['Profit'].mean()

c1.metric(label=t('kpi_sales'), value=f"RM {total_sales:,.0f}")
c2.metric(label=t('kpi_profit'), value=f"RM {total_profit:,.0f}", delta=f"{total_profit/total_sales*100:.1f}% margin")
c3.metric(label=t('kpi_avg'), value=f"RM {avg_profit:,.0f}")

st.divider()

col_chart, col_table = st.columns([1, 1])

with col_chart:
    st.subheader(t('chart'))
    st.bar_chart(df.set_index('Model')['Profit'], color="#FF4B4B")

with col_table:
    st.subheader(t('table_title'))
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Date": st.column_config.DateColumn("Date", format="YYYY-MM-DD"),
            "Cost": st.column_config.NumberColumn("Cost", format="RM %d"),
            "Price": st.column_config.NumberColumn("Price", format="RM %d"),
            "Profit": st.column_config.NumberColumn("Profit", format="RM %d", help="Price - Cost")
        },
        height=400
    )

st.caption("Powered by Streamlit | Designed for 2026")
