import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Set the window size to 10" x 10"
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

SHEET_ID = '1wV-DRmg31hWOK-o1UzhiKIlm2vwdH5y1'
SHEET_NAME = 'consumer_complaints'
url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'
df = pd.read_csv(url)

st.title("Consumer Financial Complaints Dashboard")

# Create a horizontal layout for KPIs and the State Filter in the same line
col1, col3, col4, col5, col6, col7, col8, col2 = st.columns(8)

# Add a dropdown filter to select the state
state_filter = col2.selectbox("Select State Filter", ["All States"] + df['state'].unique().tolist())

# Apply the state filter to your data
if state_filter == "All States":
    filtered_df = df  # Show data for all states
else:
    filtered_df = df[df['state'] == state_filter]

# KPI 1: Total Number of Complaints
total_complaints = filtered_df['Count of complaint_id'].sum()
col1.metric("Total Complaints", total_complaints)

# KPI 2: Total Number of Complaints with Closed Status
closed_complaints = filtered_df[filtered_df['company_response'].str.contains("Closed")]['Count of complaint_id'].sum()
col3.metric("Closed Complaints", closed_complaints)

# KPI 3: % of Timely Responded Complaints
timely_complaints = filtered_df[filtered_df['timely'] == 'Yes']['Count of complaint_id'].sum()
percentage_timely = (timely_complaints / total_complaints) * 100
col4.metric("% Timely Responded Complaints", percentage_timely)

# KPI 4: Total Number of Complaints with In Progress Status
in_progress_complaints = filtered_df[filtered_df['company_response'] == "In Progress"]['Count of complaint_id'].sum()
col5.metric("In Progress Complaints", in_progress_complaints)

# Create a horizontal layout for charts
col6, col7 = st.columns(2)

# Group the data by 'product' and sum the number of complaints
product_complaints = df.groupby('product')['Count of complaint_id'].sum().reset_index()

# Create a horizontal bar plot
fig1 = px.bar(product_complaints, x='Count of complaint_id', y='product', orientation='h', title='Number of Complaints by Product')
col6.plotly_chart(fig1)

# Convert the 'Month Year' column to a datetime format
df['Month Year'] = pd.to_datetime(df['Month Year'], format='%d/%m/%Y')

# Group the data by 'Month Year' and sum the number of complaints
time_complaints = df.groupby('Month Year')['Count of complaint_id'].sum().reset_index()

# Sort the data by 'Month Year' in ascending order
time_complaints = time_complaints.sort_values('Month Year')

# Create a line chart
fig2 = px.line(time_complaints, x='Month Year', y='Count of complaint_id', title='Number of Complaints Over Time (Month Year)', markers=True)
col7.plotly_chart(fig2)

# Create a horizontal layout for the pie chart
col8, col9 = st.columns(2)

# Group the data by 'submitted_via' and sum the number of complaints
submitted_via_complaints = df.groupby('submitted_via')['Count of complaint_id'].sum().reset_index()

# Create a pie chart
fig3 = px.pie(submitted_via_complaints, names='submitted_via', values='Count of complaint_id', title='Number of Complaints by Submitted Via Channel')
col8.plotly_chart(fig3)

# Group the data by 'issue' and 'sub_issue' and sum the number of complaints
issue_subissue_complaints = df.groupby(['issue', 'sub_issue'])['Count of complaint_id'].sum().reset_index()

# Create a treemap
fig4 = px.treemap(issue_subissue_complaints, path=['issue', 'sub_issue'], values='Count of complaint_id', title='Number of Complaints by Issue and Sub-Issue')
col9.plotly_chart(fig4)

# Add a footer
st.markdown("Designed by: Muhammad Zohaib Khan")
