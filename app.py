import streamlit as st
import pandas as pd 
from data import load_data, calculate_summary_stats, top_producers
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

Cyano Farms is an organic smallholder farm located 45 minutes west of Boston. We’ve supplied over 20 families from a variety of fresh fruits, vegetables, mushrooms, and seedlings. During the 2026 season, we've grown over 300 plants from seed including leafy greens, tomatoes, zucchini, and herbs. 

At the core of everything we do is a commitment to organic and sustainable practices. We used only upcycled materials, diverting hundreds of pounds of waste from the landfill to construct our raised beds, trellises, and plant covers. In addition, we use exclusively gray or rain water and organic pesticides and fertilizers. 

"""

""  # Add a little vertical space. Same as st.write("").
""
images = ['butternut.jpg', 'chard.jpg', 'mushroom.jpg', 'squash_kale.jpg', 'tomatoes.jpg' ]
paths = ['images/'+ path for path in images]
img = [ImageOps.exif_transpose(Image.open(path)) for path in paths]


st.image(img, width= 300)


"""
## 2026
"""
# Filter by plant
plant_selection = st.multiselect(
    "Select food",
    df['Item'].unique(),
    default = df['Item'].unique(),
    accept_new_options=False
)


df_filter_plant = df[df['Item'].isin(plant_selection)]

# # Filter by date range 
# start_date, end_date = st.select_slider(
#     "Select a date range",
#     options= df['Date'].unique(),
#     value=(df['Date'].min(), df['Date'].max()),
# )
# df_filter_plant_date = df_filter_plant[df_filter_plant['Date'].between(start_date, end_date)]


st.bar_chart(df_filter_plant, x="Week", y="Weight (lb)", color='Item', stack=True)


sum_stats = calculate_summary_stats(df_filter_plant)
top_producer_stats = top_producers(df_filter_plant)

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
            st.bar_chart(top_producer_stats[1][0:min(len(top_producer_stats[1]), 5)], 
                            y = 'Weight (lb)', horizontal = True, sort = False)

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
            st.bar_chart(top_producer_stats[0][0:min(len(top_producer_stats[1]), 5)], 
                            y = 'Value ($)', y_label = "Value ($)", horizontal = True, sort = False)

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
            st.bar_chart(week_top_producer_stats[1][0:min(len(week_top_producer_stats[1]), 5)], y = 'Weight (lb)', horizontal = True, sort = False)
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
            st.bar_chart(week_top_producer_stats[0][0:min(len(week_top_producer_stats[1]), 5)], y = 'Value ($)', y_label = "Value ($)", horizontal = True, sort = False)


"""
## Raw Data

"""
st.dataframe(df[['Date', 'Item', 'Weight (lb)', 'Value ($)']])



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

   
   