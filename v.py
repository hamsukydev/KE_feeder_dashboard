# Metrics for Total Feeder Count by Band
st.subheader('Total Feeder Count by Band')

# Group by BAND and count the feeders
band_counts = df.groupby('BAND')['LOAD CENTER'].count().reset_index(name='Feeder Count')

# Display metrics using st.columns
with st.expander("Metrics"):
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
