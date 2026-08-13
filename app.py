import streamlit as st
import altair as alt
import pandas as pd 
from data import load_data, calculate_summary_stats, top_producers, item_to_color
from PIL import Image, ImageOps

df = load_data()

st.set_page_config(
    # Title and icon for the browser's tab bar:
    page_title="Cyano Farms",
    page_icon="🚜",
    # Make the content take up the width of the page:
    layout="wide",
    
)

"""
# Cyano Farms

Cyano Farms is an organic smallholder farm entirely operated by Brian. We’ve supplied over 20 families from a variety of fresh fruits, vegetables, mushrooms, and seedlings. During the 2026 season, we've grown over 300 plants from seed including leafy greens, tomatoes, zucchini, and herbs. 

At the core of everything we do is a commitment to organic and sustainable agricultural practices. We used only upcycled materials, diverting hundreds of pounds of waste from the landfill to construct our raised beds, trellises, and plant covers. In addition, we collect gray or rain water to water out plants and use only organic pesticides and fertilizers. 

"""

""  # Add a little vertical space. Same as st.write("").
""
images = [ 'tomatoes.jpg', 'squash_kale.jpg', 'chard.jpg', 'butternut.jpg', 'mushroom.jpg']
paths = ['images/'+ path for path in images]
img = [ImageOps.exif_transpose(Image.open(path)) for path in paths]


st.image(img, width= 300)

# Filter by plant
plant_selection = st.multiselect(
    "Select food",
    df['Item'].unique(),
    default = df['Item'].unique(),
    accept_new_options=False
)


df_filter_plant = df[df['Item'].isin(plant_selection)]
df_filter_plant['Color'] = df_filter_plant['Item'].apply(item_to_color)
# # Filter by date range 
# start_date, end_date = st.select_slider(
#     "Select a date range",
#     options= df['Date'].unique(),
#     value=(df['Date'].min(), df['Date'].max()),
# )
# df_filter_plant_date = df_filter_plant[df_filter_plant['Date'].between(start_date, end_date)]

tab1, tab2 = st.tabs(["Week", "Day"])
with tab1:
    st.header("Harvest by Week")
    # st.bar_chart(df_filter_plant, x="Week", y="Weight (lb)", color='Item', stack=True)
    chart = (
        alt.Chart(df_filter_plant)
        .mark_bar()
        .encode(
            x=alt.X("Week:N", title="Week", axis=alt.Axis(labelAngle=0)),
            y=alt.Y("Weight (lb):Q", title="Weight (lb)"),
            color = alt.Color(
                    "Color:N",
                    scale=None,
                    legend=None
                ),
            tooltip=[
                alt.Tooltip("Week:N"),
                alt.Tooltip("Item:N"),
                alt.Tooltip("Weight (lb):Q", format=".2f"),
            ],
        )
    )

    st.altair_chart(chart)
with tab2:
    st.header("Harvest by Day")
    st.bar_chart(df_filter_plant, x="Date", y="Weight (lb)", color='Item', stack=True)

sum_stats = calculate_summary_stats(df_filter_plant)
top_producer_stats = top_producers(df_filter_plant)
"""
## 2026 Season
"""
with st.container(horizontal=True, gap="medium"):
    cols = st.columns([0.15, 0.35, 0.15, 0.35], gap="medium")

    # Column 0 for totals
    with cols[0]:
        st.metric(
            'Weight',
            f"{sum_stats['Total Weight']:.2f} lb",
            width="content",
            delta = f"{sum_stats['Current Week Weight']:.2f} lb",
            format = None,
            
            delta_description= "Since " +  pd.offsets.Week(weekday=6).rollback(pd.Timestamp.today().normalize()).strftime('%m/%d/%Y')
            )

    with cols[1]:
        st.write("Top Producers by Weight")
        if top_producer_stats is not None:
            chart_data = top_producer_stats[1][0:min(len(top_producer_stats[1]), 5)]
            chart_data["Color"] = chart_data['Item'].apply(item_to_color)
            chart = alt.Chart(chart_data).mark_bar().encode(
                x=alt.X("Weight (lb):Q"),
                y=alt.Y("Item:N", sort="-x"),
                color=alt.Color(
                    "Color:N",
                    scale=None,
                    legend=None
                ),
                tooltip=["Item", "Weight (lb)"]
            )

            st.altair_chart(chart)

    with cols[2]:
        st.metric(
            'Value',
            f"{sum_stats['Total Value']:.2f}",
            width="content",
            delta = f"{sum_stats['Current Week Value']:.2f}",
            format = "dollar",
            delta_description= "Since " +  pd.offsets.Week(weekday=6).rollback(pd.Timestamp.today().normalize()).strftime('%m/%d/%Y')
            )

    with cols[3]:
        st.write("Top Producers by Value")
        if top_producer_stats is not None: 
            chart_data = top_producer_stats[0][0:min(len(top_producer_stats[1]), 5)]
            chart_data["Color"] = chart_data['Item'].apply(item_to_color)
            chart = alt.Chart(chart_data).mark_bar().encode(
                x=alt.X("Value ($):Q"),
                y=alt.Y("Item:N", sort="-x"),
                color=alt.Color(
                    "Color:N",
                    scale=None,
                    legend=None
                ),
                tooltip=["Item", "Value ($)"]
            )

            st.altair_chart(chart)

"""
## Last 7 Days

"""
week_df = df_filter_plant[df_filter_plant['Date'] > pd.Timestamp.today().normalize() - pd.Timedelta(days=7)]
week_sum_stats = calculate_summary_stats(week_df)
week_top_producer_stats = top_producers(week_df)

with st.container(horizontal=True, gap="medium"):
    cols = st.columns([0.15, 0.35, 0.15, 0.35], gap="medium")

    # Column 0 for totals
    with cols[0]:
        st.metric(
            'Weight',
            f"{week_sum_stats['Total Weight']:.2f} lb",
            width="content",
            delta = f"{week_sum_stats['Current Day Weight']:.2f} lb",
            format = None,
            delta_description= "Today"
            )

    with cols[1]:
        st.write("Top Producers by Weight")
        if week_top_producer_stats is not None:
            chart_data = week_top_producer_stats[1][0:min(len(week_top_producer_stats[1]), 5)]
            chart_data["Color"] = chart_data['Item'].apply(item_to_color)
            chart = alt.Chart(chart_data).mark_bar().encode(
                x=alt.X("Weight (lb):Q"),
                y=alt.Y("Item:N", sort="-x"),
                color=alt.Color(
                    "Color:N",
                    scale=None,
                    legend=None
                ),
                tooltip=["Item", "Weight (lb)"]
            )
            st.altair_chart(chart)
    with cols[2]:
            st.metric(
                'Value',
                f"{week_sum_stats['Total Value']:.2f}",
                width="content",
                delta = f"{sum_stats['Current Day Value']:.2f}",
                format = "dollar",
                delta_description= "Today"
                )
    
    with cols[3]:
        st.write("Top Producers by Value")
        if week_top_producer_stats is not None: 
            chart_data = week_top_producer_stats[0][0:min(len(week_top_producer_stats[0]), 5)]
            chart_data["Color"] = chart_data['Item'].apply(item_to_color)
            chart = alt.Chart(chart_data).mark_bar().encode(
                x=alt.X("Value ($):Q"),
                y=alt.Y("Item:N", sort="-x"),
                color=alt.Color(
                    "Color:N",
                    scale=None,
                    legend=None
                ),
                tooltip=["Item", "Value ($)"]
            )
            st.altair_chart(chart)

"""
## Raw Data

"""
st.dataframe(df_filter_plant[['Date', 'Item', 'Weight (lb)', 'Value ($)']])



with st.bottom:
    st.caption("Value is calculated based on the price of equivalent item at Whole Foods.")
    # # Column 1 for weekly metrics 
    # with cols[1]:
    #     st.subheader("Current Week")
    #     st.metric(
    #         'Weight',
    #         f"{sum_stats['Current Week Weight']:.2f} lb",
    #         width="content",
    #         delta = f"{sum_stats['Weight Delta']:.2f} lb",
    #         format = None,
    #         delta_description= "Relative to the same day last week."
    #         )
    #     st.metric(
    #         'Value',
    #         f"{sum_stats['Current Week Savings']:.2f}",
    #         width="content",
    #         delta = sum_stats['Savings Delta'],
    #         format = "dollar",
    #         delta_description= "Relative to the same day last week."
    #         )

    # for index, (key, value) in enumerate(sum_stats.items()):
    #     with cols[index]:
    #         st.metric(
    #             key,
    #             f"{value:.2f}",
    #             # delta=f"{max_temp_2015 - max_temp_2014:0.1f}C",
    #             width="content",
    #             format = metric_format[index]
    #         )

   
   