import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

import altair as alt

# 1. Create dummy data with 10 categories
data = pd.DataFrame({
    'category': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
    'value': [95, 85, 75, 65, 55, 45, 35, 25, 15, 5],
    'color':[
    "#4A90E2",
    "#50E3C2",
    "#B8E986",
    "#F5A623",
    "#E2847A",
    "#9B51E0",
    "#34495E",
    "#E74C3C",
    "#2ECC71",
    "#1ABC9C"
]

})

# 2. Define the top 5 categories you want to show initially
top_5_categories = ['A', 'B', 'C', 'D', 'E']

# 3. Create a pan/zoom selection bound only to the X-axis
bind_pan_zoom = alt.selection_interval(
    bind='scales', 
    encodings=['x']
)

# 4. Build the chart
chart = alt.Chart(data).mark_bar().encode(
    x=alt.X(
        'category:N', 
        sort='-y',
        # Force the initial view to show only the top 5 categories
        scale=alt.Scale(domain=top_5_categories) 
    ),
    y=alt.Y('value:Q'),
    color = alt.Color(
        "color",
        scale=None,
        legend=None
    )
).add_params(
    bind_pan_zoom
).properties(
    title="Top 5 Categories (Drag/Pan to see more)",
    width=500,
    height=300
).interactive(bind_y= False)
with st.container(): 
    st.altair_chart(chart)