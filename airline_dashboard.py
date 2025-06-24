airline_dashboard.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

# Simulate fake airline operations data
np.random.seed(42)
dates = pd.date_range(datetime.today() - timedelta(days=30), periods=31)
airlines = ['Saudia', 'Flynas', 'Flyadeal', 'Emirates', 'Qatar Airways']

data = {
    'Date': np.tile(dates, len(airlines)),
    'Airline': np.repeat(airlines, len(dates)),
    'Passengers': np.random.randint(800, 3000, len(dates) * len(airlines)),
    'Delays (%)': np.round(np.random.uniform(0, 0.25, len(dates) * len(airlines)), 2),
    'Cargo (tons)': np.random.randint(50, 500, len(dates) * len(airlines)),
    'Takeoffs': np.random.randint(5, 30, len(dates) * len(airlines))
}
df = pd.DataFrame(data)

# Streamlit App
st.set_page_config(layout="wide")
st.title("✈️ King Salman International Airport – Airline Operations Dashboard")

# Filters
selected_airline = st.selectbox("Select Airline", ['All'] + airlines)
filtered_df = df if selected_airline == 'All' else df[df['Airline'] == selected_airline]

# KPIs
st.subheader("📌 Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Avg. Daily Passengers", int(filtered_df.groupby('Date')['Passengers'].sum().mean()))
col2.metric("Avg. Delay Rate", f"{filtered_df['Delays (%)'].mean():.2%}")
col3.metric("Avg. Cargo Volume", f"{filtered_df['Cargo (tons)'].mean():.1f} tons")

# Charts
st.subheader("📈 Daily Passenger Volume")
fig1 = px.line(
    filtered_df.groupby('Date')['Passengers'].sum().reset_index(),
    x='Date', y='Passengers', title="Passenger Trend"
)
st.plotly_chart(fig1, use_container_width=True)

st.subheader("📉 Delay Rate Over Time")
fig2 = px.line(
    filtered_df.groupby('Date')['Delays (%)'].mean().reset_index(),
    x='Date', y='Delays (%)', title="Delay Rate"
)
st.plotly_chart(fig2, use_container_width=True)

st.subheader("📦 Cargo Volume per Day")
fig3 = px.bar(
    filtered_df.groupby('Date')['Cargo (tons)'].sum().reset_index(),
    x='Date', y='Cargo (tons)', title="Cargo Load"
)
st.plotly_chart(fig3, use_container_width=True)

st.subheader("🛫 Market Share by Airline (Latest Day)")
latest_data = df[df['Date'] == df['Date'].max()]
fig4 = px.pie(latest_data, names='Airline', values='Passengers')
st.plotly_chart(fig4, use_container_width=True)

