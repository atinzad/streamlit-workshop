import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Demo Streamlit App")

df = pd.read_csv("state_data.csv")

# --- Filters above tabs ---
col1, col2, col3 = st.columns(3)

with col1:
    state = st.selectbox("Select a State:", df["State"].unique())

with col2:
    demographic = st.selectbox(
        "Select a Demographic:", ["Total Population", "Median Household Income"]
    )

with col3:
    year = st.selectbox("Select a Year:", df["Year"].unique())

# --- Tabs for graphs ---
tab1, tab2, tab3 = st.tabs(["State Line Graph", "Choropleth Map", "Bar Chart + Data"])

with tab1:
    # State line graph
    mask = df["State"] == state
    df_state = df[mask]
    fig_line = px.line(
        df_state,
        x="Year",
        y=demographic,
        title=f"{demographic} for {state}"
    )
    st.plotly_chart(fig_line, use_container_width=True)

with tab2:
    # Dynamic choropleth across all years
    fig_map = px.choropleth(
        df,
        locations="State Abbrev",
        locationmode="USA-states",
        color=demographic,
        animation_frame="Year",
        scope="usa",
        title=f"{demographic} across US states over time",
        color_continuous_scale="viridis",
    )
    st.plotly_chart(fig_map, use_container_width=True)

with tab3:
    # Multiselect for states
    selected_states = st.multiselect("Select States:", df["State"].unique())

    # Filter dataframe for selected states across all years
    if selected_states:
        df_states = df[df["State"].isin(selected_states)]
    else:
        df_states = df  # show everything if none selected

    # Filter for bar chart (specific year + selected states)
    df_year = df[df["Year"] == year]
    if selected_states:
        df_year = df_year[df_year["State"].isin(selected_states)]

    # Bar chart
    fig_bar = px.bar(
        df_year,
        x="State",
        y=demographic,
        title=f"{demographic} across selected states in {year}",
        color=demographic,
        color_continuous_scale="viridis"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # Dataframe for selected states across all years
    st.write("Data for selected states across all years:")
    st.dataframe(df_states)
