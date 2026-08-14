import streamlit as st
import pandas as pd 
from data import load_data, calculate_summary_stats, calculate_top_producers
from render import render_main_bar, render_top_producers_chart
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

Cyano Farms is an organic smallholder farm operated by Brian. We’ve supplied over 20 families from a variety of fresh fruits, vegetables, mushrooms, and seedlings. During the 2026 season, we've grown over 300 plants from seed including leafy greens, tomatoes, zucchini, and herbs. 

At the core of everything we do is a commitment to organic and sustainable agricultural practices. We used only upcycled materials, diverting hundreds of pounds of waste from the landfill to construct our raised beds, trellises, and plant covers. In addition, we collect gray or rain water to water out plants and use only organic pesticides and fertilizers. 

"""

"" 
""
# images = [ 'tomatoes.jpg', 'squash_kale.jpg', 'chard.jpg', 'butternut.jpg', 'mushroom.jpg']
# paths = ['images/'+ path for path in images]
# img = [ImageOps.exif_transpose(Image.open(path)) for path in paths]


# st.image(img, width= 300)


st.header(f'2026 Harvests')

# Fitler crops 
crop_selection = st.multiselect("Select crops", df['Item'].unique().sort_values(ascending = True),
                                default = df['Item'].unique(), 
                                accept_new_options=False
                                )




df_filter_plant = df[df['Item'].isin(crop_selection)]




metric_selection, agg_selection, bar_height_toggle = 'Weight', 'Week', 'True'
with st.container(border = True):
    st.write("Chart Options")
    cols = st.columns([0.10, 0.10, 0.8], gap="medium")
    with cols[0]: 
        metric_selection = st.pills("Metric", ['Weight', "Value"], default='Weight', required=True)

    with cols[1]: 
        agg_selection = st.pills("Aggregation", ['Week', "Day"], default = 'Week', required=True)
    with cols[2]: 
        bar_height_toggle = st.toggle("Bar Height Labels", value = True)

    render_main_bar(df_filter_plant, agg_selection, metric_selection, bar_height_toggle)

        


sum_stats = calculate_summary_stats(df_filter_plant)
top_producer_stats = calculate_top_producers(df_filter_plant)

"""
## 2026 Season
"""
with st.container(horizontal=True, gap="medium"):
    cols = st.columns([0.5, 0.5], border= True, gap="medium")
    with cols[0]:
        sub_cols_1 = st.columns([0.1, 0.4], gap="medium")
        with sub_cols_1[0]:
            st.metric(
                'Weight',
                f"{sum_stats['Total Weight']:.2f} lb",
                width="content",
                delta = f"{sum_stats['Current Week Weight']:.2f} lb",
                format = None,
                delta_description= "Since " +  pd.offsets.Week(weekday=6).rollback(pd.Timestamp.today().normalize()).strftime('%m/%d')
                )

        with sub_cols_1[1]:
            st.write("Top Producers by Weight")
            if top_producer_stats is not None:
                render_top_producers_chart(top_producer_stats, "Weight (lb)", 5)
    with cols[1]:
        sub_cols_2 = st.columns([0.1, 0.4], gap="medium")
        with sub_cols_2[0]:
            st.metric(
                'Value',
                f"{sum_stats['Total Value']:.2f}",
                width="content",
                delta = f"{sum_stats['Current Week Value']:.2f}",
                format = "dollar",
                delta_description= "Since " +  pd.offsets.Week(weekday=6).rollback(pd.Timestamp.today().normalize()).strftime('%m/%d')
                )

        with sub_cols_2[1]:
            st.write("Top Producers by Value")
            if top_producer_stats is not None: 
                    render_top_producers_chart(top_producer_stats, "Value ($)", 5)

"""
## Last 7 Days

"""

week_df = df_filter_plant[df_filter_plant['Date'] > pd.Timestamp.today().normalize() - pd.Timedelta(days=7)]
week_sum_stats = calculate_summary_stats(week_df)
week_top_producer_stats = calculate_top_producers(week_df)

with st.container(horizontal=True, gap="medium"):
    cols = st.columns([0.5, 0.5], border= True, gap="medium")
    with cols[0]:
        sub_cols_1 = st.columns([0.1, 0.4], gap="medium")
        with sub_cols_1[0]:
            st.metric(
                'Weight',
                f"{week_sum_stats['Total Weight']:.2f} lb",
                width="content",
                delta = f"{week_sum_stats['Current Day Weight']:.2f} lb",
                format = None,
                delta_description= "Today"
                )
        with sub_cols_1[1]:
            st.write("Top Producers by Weight")
            if week_top_producer_stats is not None:
                render_top_producers_chart(week_top_producer_stats, "Weight (lb)", 5)

    with cols[1]:
        sub_cols_2 = st.columns([0.1, 0.4], gap="medium")
        with sub_cols_2[0]:
            st.metric(
                'Value',
                f"{week_sum_stats['Total Value']:.2f}",
                width="content",
                delta = f"{sum_stats['Current Day Value']:.2f}",
                format = "dollar",
                delta_description= "Today"
                )
    
        with sub_cols_2[1]:
            st.write("Top Producers by Value")
            if week_top_producer_stats is not None: 
                render_top_producers_chart(week_top_producer_stats, "Value ($)", 5)


"""
## Raw Data

"""
st.dataframe(df_filter_plant[['Date', 'Item', 'Weight (lb)', 'Value ($)']])
