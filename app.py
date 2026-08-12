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

Cyano Farms is an organic smallholder farm located 45 minutes west of Boston. We’ve supplied over 20 families from a variety of fresh fruits, vegetables, mushrooms, and seedlings. During the 2026 growign season, we've grown over 300 plants from seed including leafy greens, tomatoes, zucchini, and herbs. 

At the core of everything we do is a commitment to organic and sustainable practices. We used only upcycled materials, diverting hundreds of pounds of waste from the landfill to construct our raised beds, trellises, and plant covers. In addition, we use exclusively gray or rain water and organic pesticides and fertilizers. 

"""

""  # Add a little vertical space. Same as st.write("").
""
images = ['butternut.jpg', 'chard.jpg', 'mushroom.jpg', 'squash_kale.jpg', 'tomatoes.jpg' ]
paths = ['images/'+ path for path in images]
img = [ImageOps.exif_transpose(Image.open(path)) for path in paths]


st.image(img, width= 300)


"""
## 2026 Growing Season
"""
options = st.multiselect(
    "Select food",
    df['Item'].unique(),
    default = df['Item'].unique()
)

start_color, end_color = st.select_slider(
    "Select a date range",
    options= df['Date'],
    value=(df['Date'].min(), df['Date'].max()),
)


df = df[df['Item'].isin(options)]


pd.pivot_table(df, values=['Weight (lb)', 'Value ($)'], columns=['Week', 'Item'], aggfunc='sum')
st.bar_chart(df, x="Week", y="Weight (lb)", color="Item", stack=True)

sum_stats = calculate_summary_stats(df)
top_producer_stats = top_producers(df)

with st.container(horizontal=True, gap="medium"):
    cols = st.columns([0.25, 0.75], gap="medium")

    # Column 0 for totals
    with cols[0]:
        st.metric(
            'Weight',
            f"{sum_stats['Total Weight']:.2f} lb",
            width="content",
            delta = f"{sum_stats['Current Week Weight']:.2f} lb",
            format = None,
            delta_description= "Current Week"
            )

        with cols[1]:
            st.write("Top Producers by Weight")
            st.bar_chart(top_producer_stats[1][0:5], y = 'Weight (lb)', horizontal = True, sort = False)

with st.container(horizontal=True, gap="medium"):
    cols = st.columns([0.25, 0.75], gap="medium")

    # Column 0 for totals
    with cols[0]:
        st.metric(
            'Value',
            f"{sum_stats['Total Value']:.2f}",
            width="content",
            delta = f"{sum_stats['Current Week Value']:.2f}",
            format = "dollar",
            delta_description= "Current Week"
            )

        with cols[1]:
            st.write("Top Producers by Value")
            st.bar_chart(top_producer_stats[0][0:5], y = 'Value ($)', y_label = "Value ($)", horizontal = True, sort = False)
"""
## Last 7 Days

"""
week_df = df[df['Date'] > pd.Timestamp.today().normalize() - pd.Timedelta(days=7)]
week_sum_stats = calculate_summary_stats(week_df)
week_top_producer_stats = top_producers(week_df)

with st.container(horizontal=True, gap="medium"):
    cols = st.columns([0.25, 0.75], gap="medium")

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
            st.bar_chart(week_top_producer_stats[1][0:5], y = 'Weight (lb)', horizontal = True, sort = False)

with st.container(horizontal=True, gap="medium"):
    cols = st.columns([0.25, 0.75], gap="medium")

    # Column 0 for totals
    with cols[0]:
        st.metric(
            'Value',
            f"{week_sum_stats['Total Value']:.2f}",
            width="content",
            delta = f"{sum_stats['Current Day Value']:.2f}",
            format = "dollar",
            delta_description= "Today"
            )

        with cols[1]:
            st.write("Top Producers by Value")
            st.bar_chart(week_top_producer_stats[0][0:5], y = 'Value ($)', y_label = "Value ($)", horizontal = True, sort = False)

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

   
   