
import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from datetime import date, timedelta

st.set_page_config(
    page_title="AGROVISION 360",
    page_icon="🌾",
    layout="wide"
)

st.markdown("""
<style>
.block-container {
    padding: 1rem;
    max-width: 1200px;
}
h1 {color:#168044;}
.stButton button {
    width:100%;
    min-height:45px;
    border-radius:10px;
}
</style>
""", unsafe_allow_html=True)

st.title("🌍 AGROVISION 360")
st.subheader("AI Powered Smart Agriculture Monitoring")
st.caption("SATELLITE • AI • WEATHER • DISASTER INTELLIGENCE")

st.sidebar.title("🌱 Control Panel")

locations = {
    "Bhubaneswar": (20.2961,85.8245),
    "Puri": (19.8135,85.8312),
    "Cuttack": (20.4625,85.8830),
    "Bargarh": (21.3335,83.6190)
}

place = st.sidebar.selectbox(
    "Select your area",
    list(locations.keys())
)

lat, lon = locations[place]

st.sidebar.write("Latitude:", lat)
st.sidebar.write("Longitude:", lon)

radius = st.sidebar.slider(
    "Analysis radius (km)",1,10,3
)

start = st.sidebar.date_input(
    "Start date",
    date.today()-timedelta(days=90)
)

end = st.sidebar.date_input(
    "End date",
    date.today()-timedelta(days=10)
)

page = st.selectbox(
    "Navigation",
    [
        "Home",
        "Satellite Analysis",
        "AI Agriculture",
        "Weather Intelligence",
        "Disaster Monitoring",
        "Final Report"
    ]
)

@st.cache_data(ttl=1800)
def get_weather(lat,lon):

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude":lat,
        "longitude":lon,
        "daily":[
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "precipitation_probability_max"
        ],
        "timezone":"auto",
        "forecast_days":7
    }

    response=requests.get(
        url,params=params,timeout=25
    )

    response.raise_for_status()

    return pd.DataFrame(
        response.json()["daily"]
    )

def calculate_ai(ndvi, rainfall):

    if ndvi >= 0.6:
        status="Dense vegetation"
    elif ndvi >= 0.4:
        status="Good vegetation"
    elif ndvi >= 0.2:
        status="Moderate vegetation"
    else:
        status="Low vegetation"

    if ndvi < 0.35 and rainfall < 10:
        recommendation=(
            "Inspect soil moisture and irrigation requirements."
        )
    else:
        recommendation=(
            "Continue crop monitoring and field inspection."
        )

    return status,recommendation

if page == "Home":

    st.header("🌾 Welcome to AGROVISION 360")

    st.write(
        "Monitor agriculture using satellite imagery, "
        "weather intelligence and AI."
    )

    st.info(
        f"Selected demonstration area: {place}"
    )

    c1,c2,c3=st.columns(3)

    c1.metric("Technology","Satellite")
    c2.metric("Intelligence","AI")
    c3.metric("Monitoring","Weather")

    st.subheader("Project objectives")

    st.markdown("""
    - 🛰️ Satellite image analysis
    - 🌱 Crop vegetation monitoring
    - 🌦️ Weather forecasting
    - 🌊 Flood screening
    - ☀️ Drought screening
    - 📊 Agricultural reports
    """)

    st.map(pd.DataFrame({
        "lat":[lat],
        "lon":[lon]
    }))

elif page == "Weather Intelligence":

    st.header("🌦️ Weather Intelligence")

    try:

        weather=get_weather(lat,lon)

        st.dataframe(
            weather,
            use_container_width=True
        )

        fig=px.bar(
            weather,
            x="time",
            y="precipitation_sum",
            title="7-Day Rainfall Forecast"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        fig2=px.line(
            weather,
            x="time",
            y=[
                "temperature_2m_max",
                "temperature_2m_min"
            ],
            markers=True,
            title="Temperature Forecast"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    except Exception as e:
        st.error(f"Weather error: {e}")

elif page == "Satellite Analysis":

    st.header("🛰️ Satellite Analysis")

    st.info(
        "Satellite processing will be enabled after "
        "Google Earth Engine authentication."
    )

    st.write("Selected location:",place)

    st.write("Analysis radius:",radius,"km")

    st.write("Observation period:",start,"to",end)

    st.map(pd.DataFrame({
        "lat":[lat],
        "lon":[lon]
    }))

    st.warning(
        "No satellite measurements are displayed until "
        "real satellite processing is configured."
    )

elif page == "AI Agriculture":

    st.header("🤖 AI Agriculture Intelligence")

    st.write(
        "This demonstration uses an example NDVI value. "
        "It is not a real satellite measurement."
    )

    ndvi=st.slider(
        "Example NDVI value",
        0.0,1.0,0.52
    )

    rainfall=st.slider(
        "Example forecast rainfall (mm)",
        0,200,8
    )

    status,recommendation=calculate_ai(
        ndvi,rainfall
    )

    st.metric("Example vegetation status",status)

    st.success(recommendation)

    st.caption(
        "Demonstration decision rules only. "
        "Not a trained AI model."
    )

elif page == "Disaster Monitoring":

    st.header("⚠️ Disaster Monitoring")

    st.info(
        "Flood and drought screening will be enabled "
        "after satellite and historical weather integration."
    )

    st.write(
        "Location:",place
    )

    st.write(
        "Selected coordinates:",lat,lon
    )

    st.warning(
        "This version does not generate official "
        "disaster warnings or verified risk predictions."
    )

elif page == "Final Report":

    st.header("📄 Agricultural Report")

    report=f"""
AGROVISION 360
Agricultural Monitoring Report

Location: {place}
Latitude: {lat}
Longitude: {lon}
Analysis radius: {radius} km

Observation period:
{start} to {end}

This is an initial project report.
Satellite analysis must be configured
before reporting real vegetation measurements.
"""

    st.text_area(
        "Report preview",
        report,
        height=250
    )

    st.download_button(
        "Download Report",
        report,
        file_name="AGROVISION360_Report.txt"
    )

st.divider()

st.markdown(
    "<center>🌾 AGROVISION 360 | "
    "Monitor from Space. Understand with AI. "
    "Improve Farming on Earth.</center>",
    unsafe_allow_html=True
)
