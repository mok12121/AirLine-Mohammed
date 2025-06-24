# airport_qc_dashboard.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

# Config
st.set_page_config(layout="wide")
st.title("🛫 King Salman Airport – Real-Time Quality Control Dashboard")

# Simulate a full year date range
np.random.seed(42)
dates = pd.date_range(start="2025-01-01", end="2025-12-31", freq="D")
airlines = ['Saudia', 'Flynas', 'Flyadeal', 'Emirates']
gates = [f"G{i}" for i in range(1, 11)]

# Simulate full operational dataset
data = []
for date in dates:
    for airline in airlines:
        record = {
            'Date': date,
            'Airline': airline,
            'Gate': np.random.choice(gates),
            'TurnaroundTime': np.random.normal(40, 5),
            'BagSLA': np.random.normal(18, 3),
            'QueueTime': np.random.normal(8, 2),
            'ScanFailures': np.random.binomial(1000, 0.01),
            'TotalBags': 1000,
            'PaxFlow': np.random.poisson(20),
            'DelayCause': np.random.choice(['Technical', 'Crew', 'Weather', 'Security', 'Catering'], p=[0.4,0.2,0.15,0.15,0.1])
        }
        data.append(record)
df = pd.DataFrame(data)

# Sidebar filters
st.sidebar.header("🔍 Filters")
selected_airline = st.sidebar.selectbox("Airline", ['All'] + airlines)
selected_gates = st.sidebar.multiselect("Gates", options=gates, default=gates)
date_range = st.sidebar.date_input("Select Date Range", [datetime(2025,1,1), datetime(2025,12,31)])

# Apply filters
filtered_df = df.copy()
if selected_airline != 'All':
    filtered_df = filtered_df[filtered_df['Airline'] == selected_airline]
filtered_df = filtered_df[filtered_df['Gate'].isin(selected_gates)]
if isinstance(date_range, list) and len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = filtered_df[(filtered_df['Date'] >= pd.to_datetime(start_date)) & (filtered_df['Date'] <= pd.to_datetime(end_date))]

st.markdown(f"### 📆 Showing data from {start_date.strftime('%d/%m/%Y')} to {end_date.strftime('%d/%m/%Y')}")

# Turnaround Time Chart
st.header("🛬 Turnaround Time – X̄ & R Chart")
fig1 = px.line(filtered_df, x='Date', y='TurnaroundTime', color='Airline', markers=True, title="Avg Turnaround Time")
st.plotly_chart(fig1, use_container_width=True)

# Baggage SLA – CUSUM
st.header("🎒 Baggage Delivery SLA – CUSUM")
sla_series = filtered_df.groupby('Date')['BagSLA'].mean()
cusum = np.cumsum(sla_series - sla_series.mean())
fig2 = px.line(x=sla_series.index, y=cusum, title="CUSUM – Baggage SLA")
st.plotly_chart(fig2, use_container_width=True)

# Security Queue – EWMA
st.header("👮 Security Queue Time – EWMA")
alpha = 0.3
queue_series = filtered_df.groupby('Date')['QueueTime'].mean()
ewma = [queue_series.iloc[0]]
for i in range(1, len(queue_series)):
    ewma.append(alpha * queue_series.iloc[i] + (1 - alpha) * ewma[-1])
fig3 = px.line(x=queue_series.index, y=ewma, title="EWMA – Queue Time")
st.plotly_chart(fig3, use_container_width=True)

# Gate Utilization
st.header("✈️ Gate Utilization")
gate_util = filtered_df['Gate'].value_counts().sort_index()
fig4 = px.bar(x=gate_util.index, y=gate_util.values, title="Flights per Gate")
st.plotly_chart(fig4, use_container_width=True)

# Baggage Scan Failures – P-chart
st.header("🧳 Scan Failures – P-Chart")
daily = filtered_df.groupby('Date')[['ScanFailures', 'TotalBags']].sum()
p_rate = daily['ScanFailures'] / daily['TotalBags']
fig5 = px.line(x=daily.index, y=p_rate, title="Scan Failure Rate per Day")
st.plotly_chart(fig5, use_container_width=True)

# Passenger Flow
st.header("🧍 Passenger Flow – Moving Average")
pax_series = filtered_df.groupby('Date')['PaxFlow'].sum().rolling(window=3).mean()
fig6 = px.line(x=pax_series.index, y=pax_series.values, title="Passenger Flow (3-day MA)")
st.plotly_chart(fig6, use_container_width=True)

# Delay Types – Pareto Chart
st.header("📉 Delay Causes – Pareto Chart")
delay_counts = filtered_df['DelayCause'].value_counts()
fig7 = px.bar(x=delay_counts.index, y=delay_counts.values, title="Top Delay Causes")
st.plotly_chart(fig7, use_container_width=True)

st.success("✅ Dashboard running on date-filtered, categorized simulated operational data.")
