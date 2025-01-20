import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

# Set the layout to wide
st.set_page_config(layout='wide')

# Load the data
df = pd.read_csv('india.csv')

list_of_states = list(df['State'].unique())
list_of_states.insert(0,'Overall India')

# Add title and description
st.title("India Data Visualization Tool")
st.markdown("""
An interactive tool for exploring India's state and district-level data. Select parameters from the sidebar to visualize trends and distributions on the map.
""")

st.sidebar.title('India Ka Data Viz')
list_of_states = list(df['State'].unique())
list_of_states.insert(0, 'Overall India')

selected_state = st.sidebar.selectbox('Select a state',list_of_states)
primary = st.sidebar.selectbox('Select Primary Parameter',sorted(df.columns[5:]))
secondary = st.sidebar.selectbox('Select Secondary Parameter',sorted(df.columns[5:]))

plot = st.sidebar.button('Plot Graph')

if plot:

    st.text('Size represent primary parameter')
    st.text('Color represents secondary parameter')
    if selected_state == 'Overall India':
        # plot for all india
        fig = px.scatter_mapbox(df, lat="Latitude", lon="Longitude", size=primary, color=secondary, zoom=4,size_max=35,
                                mapbox_style="carto-positron",width=1200,height=700,hover_name='District')

        st.plotly_chart(fig,use_container_width=True)
    else:
        # plot for selected state
        state_df = df[df['State'] == selected_state]

        fig = px.scatter_mapbox(state_df, lat="Latitude", lon="Longitude", size=primary, color=secondary, zoom=6, size_max=35,
                                mapbox_style="carto-positron", width=1200, height=700,hover_name='District')

        st.plotly_chart(fig, use_container_width=True)

# Allow users to download filtered data
st.sidebar.markdown("### Download Filtered Data")

def convert_df_to_csv(data):
    """Convert a DataFrame to CSV for downloading."""
    return data.to_csv(index=False).encode('utf-8')

if selected_state != 'Overall India':
    filtered_data = df[df['State'] == selected_state]
else:
    filtered_data = df

csv_data = convert_df_to_csv(filtered_data)
st.sidebar.download_button(
    label="Download CSV",
    data=csv_data,
    file_name='filtered_data.csv',
    mime='text/csv',
)



