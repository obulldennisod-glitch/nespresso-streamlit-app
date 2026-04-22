import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# 1️⃣ Page config
# -----------------------------
st.set_page_config(page_title="Attendance Dashboard", layout="wide")

st.title("📊 Attendance Dashboard")

# -----------------------------
# 2️⃣ Load data
# -----------------------------
file_path = r"C:\Users\Dennis Obull\Desktop\news\MY MODULES\ML\251212_KENYA_CENTRAL_2024AC_Monthly_Attendance_Database_Nov25.xlsx"

df = pd.read_excel(file_path)

# -----------------------------
# 3️⃣ Month columns
# -----------------------------
months = ['jan24','feb24','mar24','apr24','may24','jun24','jul24','aug24','sep24','oct24','nov24',
          'jan25','feb25','mar25','apr25','may25','jun25','jul25','aug25','sep25','oct25','nov25']

# -----------------------------
# 4️⃣ Sidebar filters
# -----------------------------
st.sidebar.header("🔎 Filters")

factory_filter = st.sidebar.multiselect(
    "Select Factory",
    options=df['Factory'].unique(),
    default=df['Factory'].unique()
)

trainer_filter = st.sidebar.multiselect(
    "Select Farmer Trainer",
    options=df['Farmer Trainer Name'].unique(),
    default=df['Farmer Trainer Name'].unique()
)

# Apply filters
filtered_df = df[
    (df['Factory'].isin(factory_filter)) &
    (df['Farmer Trainer Name'].isin(trainer_filter))
]

# -----------------------------
# 5️⃣ Attendance by Month
# -----------------------------
attendance_by_month = filtered_df[months].sum().reset_index()
attendance_by_month.columns = ['Month', 'Total Attendance']

fig_month = px.bar(
    attendance_by_month,
    x='Month',
    y='Total Attendance',
    title='📅 Total Attendance by Month',
    text='Total Attendance'
)

# -----------------------------
# 6️⃣ Attendance by Trainer
# -----------------------------
attendance_by_trainer = (
    filtered_df.groupby('Farmer Trainer Name')[months]
    .sum()
    .sum(axis=1)
    .reset_index()
)
attendance_by_trainer.columns = ['Farmer Trainer', 'Total Attendance']

fig_trainer = px.bar(
    attendance_by_trainer,
    x='Farmer Trainer',
    y='Total Attendance',
    title='👨‍🏫 Attendance by Farmer Trainer',
    text='Total Attendance'
)

# -----------------------------
# 7️⃣ Attendance by Factory
# -----------------------------
attendance_by_factory = (
    filtered_df.groupby('Factory')[months]
    .sum()
    .sum(axis=1)
    .reset_index()
)
attendance_by_factory.columns = ['Factory', 'Total Attendance']

fig_factory = px.bar(
    attendance_by_factory,
    x='Factory',
    y='Total Attendance',
    title='🏭 Attendance by Factory',
    text='Total Attendance'
)

# -----------------------------
# 8️⃣ Display charts (same page)
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig_month, use_container_width=True)

with col2:
    st.plotly_chart(fig_factory, use_container_width=True)

st.plotly_chart(fig_trainer, use_container_width=True)

# -----------------------------
# 9️⃣ Show raw data (optional)
# -----------------------------
with st.expander("📄 View Raw Data"):
    st.dataframe(filtered_df)

# streamlit run Nespresso.py