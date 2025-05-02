import streamlit as st
from mydb import mydb
import plotly.graph_objects as go
import base64
import pandas as pd

# pip install streamlit

# python -m streamlit run app.py

# set background image
def set_background(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: auto;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

set_background("background.jpg")

# heading
st.title("_WELCOME TO FLIGHT_")
st.write("---Have a Safe Journey---")

# sidebar
st.sidebar.title("Flights Details" )
st.sidebar.image("download.jpeg", use_container_width=True)

# sidebar dropdown
choice = st.sidebar.selectbox("Menu", ["Select One", "Check Flight", "Analysis", "Map"])

db = mydb()

# choice 1
if choice == "Check Flight":
    st.title("Check Flights")

    col1,col2 = st.columns(2)

    with col1:
        source = st.selectbox("Source", db.get_cities())

    with col2:
        destination = st.selectbox("Destination", db.get_destination_cities())

    if st.button("Check Flights"):

        all_flights = db.get_flights_data(source, destination)
        
        st.dataframe(all_flights)

# choice 2
elif choice == "Analysis":
    st.title("Flight Analysis")

# pip install plotly

    air_name, flt_cnt = db.airlines_flights()

    # Pie chart
    fig = go.Figure(go.Pie(labels=air_name, values=flt_cnt))
    
    st.header("Airline Count")
    st.plotly_chart(fig)

    airport, cty = db.buziest_airports()

    # bar chart
    new_fig = go.Figure(go.Bar(x=airport, y=cty))

    st.header("Buziest Airports")
    st.plotly_chart(new_fig)

# choice 3
elif choice == "Map":
    st.title("Flight Source Map")

    # cities latitude and longitude
    city_coords = {
    'Delhi': [28.6139, 77.2090],
    'Kolkata': [22.5726, 88.3639],
    'Mumbai': [19.0760, 72.8777],
    'Chennai': [13.0827, 80.2707],
    'Bangalore': [12.9716, 77.5946],
    'Hyderabad': [17.3850, 78.4867],
    'Cochin': [9.9312, 76.2673],
    'New Delhi': [28.6139, 77.2088],
     }
    # upload daataset
    all_flights = pd.read_csv("flights.csv")

    # Add latitude and longitude based on Source city
    all_flights['lat'] = all_flights['Source'].map(lambda x: city_coords.get(x, [None, None])[0])
    all_flights['lon'] = all_flights['Source'].map(lambda x: city_coords.get(x, [None, None])[1])

    # Drop rows where coordinates are missing
    map_df = all_flights.dropna(subset=['lat', 'lon'])

    # Show the map
    if not map_df.empty:
        # st.subheader("Flight Source Map")
        st.map(map_df[['lat', 'lon']])
    else:
        st.warning("No valid coordinates found to plot.")

else:
    pass

