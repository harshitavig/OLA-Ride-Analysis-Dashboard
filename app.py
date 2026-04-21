import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(layout="wide")

# ------------------ LOAD DATA ------------------
df = pd.read_csv("ola_cleaned.csv")
df['Date'] = pd.to_datetime(df['Date'])

# ------------------ THEME ------------------
st.markdown("""
<style>
body {background-color: #000000;}
[data-testid="stAppViewContainer"] {
    background-color: #000000;
    color: white;
}
.metric-box {
    background-color: #000000;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
    border: 2px solid #f2c94c;
}
</style>
""", unsafe_allow_html=True)

# ------------------ SIDEBAR ------------------
st.sidebar.header("Filters")

vehicle = st.sidebar.multiselect("Vehicle Type", df["Vehicle_Type"].unique(), default=df["Vehicle_Type"].unique())
payment = st.sidebar.multiselect("Payment Method", df["Payment_Method"].unique(), default=df["Payment_Method"].unique())
status = st.sidebar.multiselect("Booking Status", df["Booking_Status"].unique(), default=df["Booking_Status"].unique())
start_date = st.sidebar.date_input("Start Date", df['Date'].min())
end_date = st.sidebar.date_input("End Date", df['Date'].max())


filtered_df = df[
    (df["Vehicle_Type"].isin(vehicle)) &
    (df["Payment_Method"].isin(payment)) &
    (df["Booking_Status"].isin(status))&
    (df["Date"] >= pd.to_datetime(start_date)) &
    (df["Date"] <= pd.to_datetime(end_date))
]

# ------------------ TITLE ------------------
st.markdown("<h1 style='color:#f2c94c;'> OLA Ride Analytics Dashboard</h1>", unsafe_allow_html=True)

# ------------------ KPI ------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"{int(filtered_df['Booking_Value'].sum()/1000000)}M")
col2.metric("Total Bookings", len(filtered_df))
col3.metric("Avg. Ride Distance", f"{filtered_df['Ride_Distance'].mean():.2f} km")
col4.metric("Cancellation Rate", f"{(filtered_df['Booking_Status'] == 'Cancelled').mean() * 100:.2f}%")

# ------------------ CHARTS ROW 1 ------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Ride Volume Trend")
    trend = filtered_df.groupby(filtered_df['Date'].dt.day).size()
    st.line_chart(trend)

with col2:
    st.subheader("Ride Distance by Vehicle")
    dist = filtered_df.groupby("Vehicle_Type")["Ride_Distance"].sum()
    st.bar_chart(dist)

# ------------------ CHARTS ROW 2 ------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Top Customers")
    top_cust = filtered_df.groupby("Customer_ID")["Booking_Value"].sum().nlargest(5)
    st.bar_chart(top_cust)

with col2:
    st.subheader("Booking Status Distribution")

    status_counts = filtered_df["Booking_Status"].value_counts().reset_index()
    status_counts.columns = ["Booking_Status", "Count"]

    fig = px.pie(
        status_counts,
        names="Booking_Status",
        values="Count",
        hole=0.2  # <-- ye donut banata hai
    )

    st.plotly_chart(fig)

# ------------------ CHARTS ROW 3 ------------------
col1, col2 = st.columns(2)

import plotly.express as px

#  Column 1
with col1:
    st.subheader("Payment Method")

    payment_counts = filtered_df["Payment_Method"].value_counts().reset_index()
    payment_counts.columns = ["Payment_Method", "Count"]

    fig = px.pie(
        payment_counts,
        names="Payment_Method",
        values="Count",
        hole=0.4
    )

    st.plotly_chart(fig, use_container_width=True)


#  Column 2
with col2:
    st.subheader("Ride Distance Trend")

    dist_trend = filtered_df.groupby(filtered_df['Date'].dt.day)["Ride_Distance"].sum()
    st.line_chart(dist_trend)


# ------------------ BUSINESS RECOMMENDATIONS ------------------
st.markdown("##  Business Insights & Recommendations")

st.markdown("""
###  Cancellation Issue
Insight:
High cancellation rate observed.

Recommendation:
• Add driver incentives in peak hours
• Improve ETA accuracy
• Apply cancellation penalties

###  Driver Performance
Insight:
Driver ratings vary significantly

Recommendation:
• Reward top drivers
• Train low performers
• Introduce incentives  

###  Revenue Optimization
Insight:
Revenue varies across vehicle types

Recommendation:
• Promote high revenue vehicles
• Apply dynamic pricing
• Optimize pricing strategy

###  Peak Hour Demand
Insight:
Bookings spike during certain hours

Recommendations:
• Apply surge pricing
• Offer driver bonuses
• Run off-peak discounts   

###  Payment Insights
 Insight:
Payment usage differs by users

Recommendations:
• Promote digital payments
• Offer cashback
• Simplify checkout

###  Customer Behavior
Insight:
Repeat customers drive revenue

Recommendations:
• Launch loyalty programs
• Give personalized offers
• Improve user experience

###  DISTANCE vs REVENUE
 Insight:
There is a relation between Ride distance and revenue 

Recommendations:
Optimize price for Long rides 
Improve price for Short rides 

###  Location Demand
Insight:
Certain locations show high demand

Recommendations:
• Pre-position drivers
• Increase supply in hotspots
• Promote low-demand areas

### Incomplete Rides
Insight:
Rides fail due to multiple issues

Recommendation:
• Fix top failure reasons
• Improve app performance
• Optimize driver coordination                                                

""")
