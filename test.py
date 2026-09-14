import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

import altair as alt




# 1. Create dummy data with 10 categories
data = pd.DataFrame({
    'Item': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
    'Value': [95, 85, 75, 65, 55, 45, 35, 25, 15, 5],
    'Begin': [0,0,0,0,0,0,0,0,0,0],
    'Range': pd.date_range(start="2026-09-04", periods=10, freq="D"),
    'Color':[
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

data = data.reset_index()



# y_axis = alt.Y('index:O', sort = '-x', title = "", axis=alt.Axis(labelLimit=200))
# chart = alt.Chart(data).mark_bar().encode(
#     x='Value:Q',
#     y=y_axis
# ).properties(height=700)


# items_to_display = data_full[0:min(len(data_full), num_to_display)]['Item'].to_list() # Get top 5 or less, all of them 

# Create bar chart 
# y_axis = alt.Y('Item:N', sort = '-x', title = "", axis=alt.Axis(labelLimit=200),
#             scale=alt.Scale(domain = items_to_display))
y_axis_name = 'Range:O'
# y_axis = alt.Y(y_axis_name, sort = '-x', title = "", axis=alt.Axis(labelLimit=200),)

max_date = pd.Timestamp.today()
min_date = max_date + pd.Timedelta(days=5)
y_axis = alt.Y('Range:T', sort = "-y",axis = None,  scale=alt.Scale(domain = [min_date, max_date], reverse=True))
            # scale=alt.Scale(domain = items_to_display))

chart = alt.Chart(data).mark_bar(size = 30).encode(
    x=alt.X(f'Value:Q'), 
    # y=alt.Y("Item:N", sort="-x", title = "", axis= alt.Axis(labelLimit=200)),
    y = y_axis,
    color=alt.Color(
        "Color:N",
        scale=None,
        legend=None
    ),
    tooltip=[alt.Tooltip('Item:N'), alt.Tooltip('Value:Q', format=".2f")]
).interactive(bind_x = False)
# Add labels 
# labels = alt.Chart(data).mark_text(
#     align="left",
#     baseline="middle",
#     dx=5,
#     color="white"
# ).encode(
#     x=alt.X("Value:Q"),
#     y=alt.Y("Range:T", sort="-x"),
#     text=alt.Text("Value:Q", format=",.2f")
# )

# Add labels 
labels_2 = alt.Chart(data).mark_text(
    align="right",
    baseline="middle",
    dx=-5,
    color="white"
).encode(
    x=alt.X("Begin:Q"),
    y=alt.Y("Range:T", sort="-x"),
    text=alt.Text("Item:N")
)

st.altair_chart(chart + labels_2)