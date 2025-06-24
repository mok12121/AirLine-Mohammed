# airport_qc_dashboard.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Config
st.set_page_config(layout="wide")
st.title("🛫 King Salman Airport – Real-Time Quality Control Dashboard")

# Time reference
now = datetime.now()
dates = pd.date_range(now - timedelta(days=30), periods=31)

# Simulated Airlines and Gates
airlines = ['Saudia', 'Flynas', 'Flyadeal', 'Emirates']
gates = [f"G{i}" for i in range(1, 11)]

# Helper: Generate Control Limits
def control_limits(series):
    mean = series.mean()
    std = series.std()
    return mean, mean + 3*std, mean - 3*std

# Section 1: Turnaround Time – Xbar-R Chart
st.header("🛬 Flight Turnaround Time – X̄ & R Chart")
tat = pd.Series(np.random.normal(40, 6, 50))
mean, ucl, lcl = control_limits(tat)
fig1 = px.line(y=tat, title="Turnaround Time (min)")
fig1.add_hline(y=mean, line_dash="dash", line_color="green")
fig1.add_hline(y=ucl, line_dash="dash", line_color="red")
fig1.add_hline(y=lcl, line_dash="dash", line_color="red")
st.plotly_chart(fig1, use_container_width=True)

# Section 2: Baggage SLA – CUSUM Chart
st.header("🎒 Baggage Delivery SLA – CUSUM")
slas = np.random.normal(18, 4, 100)
cusum = np.cumsum(slas - np.mean(slas))
fig2 = px.line(y=cusum, title="CUSUM of Baggage Delivery Time")
st.plotly_chart(fig2, use_container_width=True)

# Section 3: Security Queue – EWMA Chart
st.header("👮 Security Queue Wait Time – EWMA")
alpha = 0.3
waits = np.random.normal(8, 2, 100)
ewma = [waits[0]]
for i in range(1, len(waits)):
    ewma.append(alpha * waits[i] + (1 - alpha) * ewma[-1])
fig3 = px.line(y=ewma, title="EWMA – Security Wait Time (min)")
st.plotly_chart(fig3, use_container_width=True)

# Section 4: Gate Utilization – Bar Chart
st.header("✈️ Gate Utilization – Flights Per Gate")
gate_counts = pd.Series(np.random.randint(10, 40, len(gates)), index=gates)
fig4 = px.bar(gate_counts, title="Flights Handled Per Gate Today")
st.plotly_chart(fig4, use_container_width=True)

# Section 5: Baggage Scan Failures – P-Chart
st.header("🧳 Baggage Scan Failures – P-Chart")
total_bags = np.random.randint(950, 1050, 30)
fails = np.random.binomial(n=total_bags, p=0.01)
p_rates = fails / total_bags
fig5 = px.line(y=p_rates, title="Failure Rate Per 1000 Bags")
st.plotly_chart(fig5, use_container_width=True)

# Section 6: Passenger Flow – Real-Time Entries
st.header("🧍 Passenger Entry Flow – Moving Average")
pax = pd.Series(np.random.poisson(20, 60))
pax_ma = pax.rolling(window=5).mean()
fig6 = px.line(y=pax_ma, title="Passenger Entries Per Minute (5-min MA)")
st.plotly_chart(fig6, use_container_width=True)

# Section 7: Delay Types – Pareto Chart
st.header("📉 Delay Incident Analysis – Pareto Chart")
delay_causes = {
    'Technical': 24,
    'Crew': 17,
    'Weather': 8,
    'Security': 5,
    'Catering': 3
}
delay_df = pd.DataFrame(delay_causes.items(), columns=['Cause', 'Count'])
delay_df.sort_values(by='Count', ascending=False, inplace=True)
fig7 = px.bar(delay_df, x='Cause', y='Count', title="Top Delay Causes")
st.plotly_chart(fig7, use_container_width=True)

st.markdown("---")
st.success("✅ Dashboard running on simulated data. Hook into real sources via API to go live.")
