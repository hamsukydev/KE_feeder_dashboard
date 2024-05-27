import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import plotly.express as px
from time import sleep

# Set page configuration
st.set_page_config(page_title="Real Time Feeder Dashboard", page_icon="💡", layout="wide")

# Add an image to the sidebar
st.sidebar.image('assets/kaduna-removebg-preview.png', use_column_width=True)

# Set up the connection to Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('feederapi-424406-754ae91736c5.json', scope)
client = gspread.authorize(creds)

# Open the Google Sheet
sheet_url = 'https://docs.google.com/spreadsheets/d/14S8FXJGAp7PkCvtK3Y-PdSzrUkc4QOus2oGRQyBXqjk/edit#gid=541324402'
sheet = client.open_by_url(sheet_url)

# List all sheet names
worksheet_list = sheet.worksheets()
sheet_names = [worksheet.title for worksheet in worksheet_list]

# Dropdown to select sheet
selected_sheet = st.sidebar.selectbox('Select a sheet to view', sheet_names)

# Get all records from the selected sheet
worksheet = sheet.worksheet(selected_sheet)
data = worksheet.get_all_records()

# Convert the data to a DataFrame
df = pd.DataFrame(data)

# Define the hourly columns
hourly_columns = [
    '0:00', '0:30', '1:00', '1:30', '2:00', '2:30', '3:00', '3:30', '4:00', '4:30',
    '5:00', '5:30', '6:00', '6:30', '7:00', '7:30', '8:00', '8:30', '9:00', '9:30',
    '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30', '14:00', '14:30',
    '15:00', '15:30', '16:00', '16:30', '17:00', '17:30', '18:00', '18:30', '19:00', '19:30',
    '20:00', '20:30', '21:00', '21:30', '22:00', '22:30', '23:00', '23:30'
]

# Check for missing hourly columns and handle them
missing_columns = [col for col in hourly_columns if col not in df.columns]
if missing_columns:
    for col in missing_columns:
        df[col] = 0

# Convert all hourly columns to numeric, setting errors='coerce' to convert non-numeric values to NaN, then fill NaN with 0
df[hourly_columns] = df[hourly_columns].apply(pd.to_numeric, errors='coerce').fillna(0)

# Calculate SUPPLY_Hrs, TOTAL_LOAD, and AVRG_LOAD
df['SUPPLY_Hrs'] = df[hourly_columns].apply(lambda row: (row > 0).sum(), axis=1)
df['TOTAL_LOAD'] = df[hourly_columns].apply(lambda row: row.sum(), axis=1)
df['AVRG_LOAD'] = df[hourly_columns].apply(lambda row: row[row > 0].mean() if (row > 0).any() else 0, axis=1)

# Add feeder type (33kV or 11kV) to the load center name
df['FEEDER'] = df['33/11KV FEEDER'] + ' (' + df['LOAD CENTER'] + ')'

# Calculate total load metric
total_load_metric = df['TOTAL_LOAD'].sum()

# Calculate total load metric for each band
band_load_metrics = {}
for band in ['A', 'B', 'C', 'D', 'E']:
    total_load = df[df['BAND'] == band]['TOTAL_LOAD'].sum()
    band_load_metrics[f"Band {band}"] = total_load

# Explanation
st.markdown("""
    <h1 style="color: #4CAF50;">Feeder Dashboard</h1>
    <p style="color: #555;">## Welcome to the Feeder Dashboard</p>
    <p>This dashboard provides a comprehensive overview of the electrical feeder data collected from various area offices. 
    You can navigate through different sections using the sidebar. Here’s what you can do:</p>
    <ul>
        <li>Data Preview: View the raw data from Google Sheets.</li>
        <li>Metrics: See key performance indicators such as total load and supply hours for each band.</li>
        <li>Visualizations: Explore various charts that visualize the feeder performance metrics.</li>
    </ul>
    <p>Use this dashboard to monitor, analyze, and gain insights into the feeder data to ensure efficient energy distribution.</p>
""", unsafe_allow_html=True)

# Layout using st.columns for metrics
st.markdown("<h2 style='color: #007BFF;'>Total Load Of Each Band</h2>", unsafe_allow_html=True)

st.metric(label="Total Load of All Feeders", value=total_load_metric)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(label="Band A Load", value=band_load_metrics.get("Band A", 0))

with col2:
    st.metric(label="Band B Load", value=band_load_metrics.get("Band B", 0))

with col3:
    st.metric(label="Band C Load", value=band_load_metrics.get("Band C", 0))

with col4:
    st.metric(label="Band D Load", value=band_load_metrics.get("Band D", 0))
with col5:
    st.metric(label="Band E Load", value=band_load_metrics.get("Band E", 0))

# Metrics for Total Feeder Count by Band
st.markdown("<h2 style='color: #007BFF;'>Total Feeder Count by Band</h2>", unsafe_allow_html=True)

# Group by BAND and count the feeders
band_counts = df.groupby('BAND')['LOAD CENTER'].count().reset_index(name='Feeder Count')

# Display metrics using st.columns
cols = st.columns(5)

# Display for Band A
if 'A' in band_counts['BAND'].values:
    cols[0].metric(label="Band A Feeders 🏠", value=int(band_counts[band_counts['BAND'] == 'A']['Feeder Count']), delta=0)
else:
    cols[0].metric(label="Band A Feeders 🏠", value=0, delta=0)

# Display for Band B
if 'B' in band_counts['BAND'].values:
    cols[1].metric(label="Band B Feeders 🏠", value=int(band_counts[band_counts['BAND'] == 'B']['Feeder Count']), delta=0)
else:
    cols[1].metric(label="Band B Feeders 🏠", value=0, delta=0)

# Display for Band C
if 'C' in band_counts['BAND'].values:
    cols[2].metric(label="Band C Feeders 🏠", value=int(band_counts[band_counts['BAND'] == 'C']['Feeder Count']), delta=0)
else:
    cols[2].metric(label="Band C Feeders 🏠", value=0, delta=0)

# Display for Band D
if 'D' in band_counts['BAND'].values:
    cols[3].metric(label="Band D Feeders 🏠", value=int(band_counts[band_counts['BAND'] == 'D']['Feeder Count']), delta=0)
else:
    cols[3].metric(label="Band D Feeders 🏠", value=0, delta=0)

# Display for Band E
if 'E' in band_counts['BAND'].values:
    cols[4].metric(label="Band E Feeders 🏠", value=int(band_counts[band_counts['BAND'] == 'E']['Feeder Count']), delta=0)
else:
    cols[4].metric(label="Band E Feeders 🏠", value=0, delta=0)

# Bar chart for total load by load center
st.markdown("<h2 style='color: #007BFF;'>Total Energy by Load Center</h2>", unsafe_allow_html=True)
fig_total_load = px.bar(df, x='FEEDER', y='TOTAL_LOAD', title='Total Energy by Load Center', labels={'FEEDER': 'Feeder (Load Center)', 'TOTAL_LOAD': 'Total Energy (MWH)'})
st.plotly_chart(fig_total_load)

# Bar chart for average load by load center
st.markdown("<h2 style='color: #007BFF;'>Average Energy by Load Center</h2>", unsafe_allow_html=True)
fig_avg_load = px.bar(df, x='FEEDER', y='AVRG_LOAD', title='Average Load by Load Center', labels={'FEEDER': 'Feeder (Load Center)', 'AVRG_LOAD': 'Average Energy (MWH)'})
st.plotly_chart(fig_avg_load)

# Bar chart for feeders with LS
st.markdown("<h2 style='color: #007BFF;'>Total LS Hours by Feeder</h2>", unsafe_allow_html=True)
ls_feeders = df[df.apply(lambda row: 'LS' in row.values, axis=1)]

if not ls_feeders.empty:
    ls_hours = ls_feeders[hourly_columns].applymap(lambda x: 1 if x == 'LS' else 0).sum(axis=1)
    ls_feeders['LS_Hours'] = ls_hours

    fig_ls_load = px.bar(ls_feeders, x='FEEDER', y='LS_Hours', title='Total LS Hours by Feeder', labels={'FEEDER': 'Feeder', 'LS_Hours': 'LS Hours'})
    st.plotly_chart(fig_ls_load)
else:
    st.write("No feeders with LS found.")

# Bar chart for top N feeders by total load
st.markdown("<h2 style='color: #007BFF;'>Top Feeders by Total Energy</h2>", unsafe_allow_html=True)
top_n = 10  # You can change this value to get more or fewer top feeders
top_feeders = df.nlargest(top_n, 'TOTAL_LOAD')
fig_top_feeders = px.bar(top_feeders, x='FEEDER', y='TOTAL_LOAD', title=f'Top {top_n} Feeders by Total Energy', text='TOTAL_LOAD', labels={'FEEDER': 'Feeder (Load Center)', 'TOTAL_LOAD': 'Total Energy (MWH)'})
fig_top_feeders.update_traces(texttemplate='%{text:.2s}', textposition='outside')
st.plotly_chart(fig_top_feeders)

# Add section for Total Previous Load of Each Sheet
st.markdown("<h2 style='color: #007BFF;'>Total Previous Energy of Each Sheet</h2>", unsafe_allow_html=True)

# Calculate total load for each sheet
total_loads = []
for worksheet in worksheet_list:
    data = worksheet.get_all_records()
    df_sheet = pd.DataFrame(data)
    # Ensure all hourly columns exist in the DataFrame
    missing_columns = [col for col in hourly_columns if col not in df_sheet.columns]
    if missing_columns:
        for col in missing_columns:
            df_sheet[col] = 0
    df_sheet[hourly_columns] = df_sheet[hourly_columns].apply(pd.to_numeric, errors='coerce').fillna(0)
    total_load = df_sheet[hourly_columns].sum().sum()
    total_loads.append((worksheet.title, total_load))
    # To prevent hitting API limits, add a small delay between requests
    sleep(1)

# Convert to DataFrame
df_total_loads = pd.DataFrame(total_loads, columns=['Sheet Name', 'Total Load'])

# Bar chart for total load of each sheet
fig_total_loads = px.bar(df_total_loads, x='Sheet Name', y='Total Load', title='Total Previous Energy of Each Sheet', labels={'Sheet Name': 'Sheet Name', 'Total Load': 'Total Load (MWH)'})
st.plotly_chart(fig_total_loads)

# Calculate and display the sum of all total loads
total_sum_loads = df_total_loads['Total Load'].sum()
st.markdown(f"<h2 style='color: #007BFF;'>Sum of All Total Loads: {total_sum_loads:.2f} MW</h2>", unsafe_allow_html=True)