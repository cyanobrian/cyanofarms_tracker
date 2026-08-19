import streamlit as st
import pandas as pd 
from data import load_data, calculate_summary_stats, calculate_top_producers
from render import render_main_bar, render_top_producers_chart, render_cumulative
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
with st.expander("Complete 2026 Growing List"):
    with st.container(horizontal = True, gap = "large"):
        st.markdown("""
        **Squash**
        * Elite Zucchini
        * Pantheon Zucchini 
        * Multipik Summer Squash 
        * Butternut Squash 
        * Kabocha Squash 
        """)
        st.markdown("""
        **Leafy Greens**
        * Vates Kale (Dward Blue Scotch)
        * Red Russian Kale
        * Rainbow Swiss Chard 
        * Roquette Arugula
        * Goji Shoots 
        """)
        st.markdown("""
        **Root Veggies**
        * Rainbow Carrots
        * Icicle Radishes 
        * Detroit Dark Red Beets 
        """)
        st.markdown("""
        **Herbs**
        * Wegan Parsley
        * Genoveses Basil 
        * Cilantro 
        * Scallions
        * Chives
        * Toon (Beef & Onions Plant )
        """)
        st.markdown("""
        **Other**
        * Kala Chana (Black Chickpeas)
        * Blue Oyster Mushrooms 
        * Red Potatoes
        * Manchurian Wild Rice 
        """)

"" 
""
# images = [ 'tomatoes.jpg', 'squash_kale.jpg', 'chard.jpg', 'butternut.jpg', 'mushroom.jpg']
# paths = ['images/'+ path for path in images]
# img = [ImageOps.exif_transpose(Image.open(path)) for path in paths]

# with st.container(horizontal= True):
#     for image in img: 
#         with st.container():
#             st.image(image)

st.divider() 

st.header(f'2026 Harvests')

# Filter crops 
crop_selection = st.multiselect("Crop Selection", df['Item'].unique().sort_values(ascending = True),
                                default = df['Item'].unique(), 
                                accept_new_options=False
                                )

df_selected_crops = df[df['Item'].isin(crop_selection)]


with st.container(border = True):
    st.write("Chart Options\n")
    with st.container(horizontal=True, gap = 'medium'):
        metric_selection = st.pills("Metric", ['Weight', "Value"], default='Weight', required=True)
        peri_selection = st.pills("Period", ['Week', "Day"], default = 'Week', required=True)
        bar_height_toggle = st.pills("Bar Heights", ['Visible', "Invisible"], default = 'Visible', required=True)

    render_main_bar(df_selected_crops, peri_selection, metric_selection, bar_height_toggle)
    render_cumulative(df_selected_crops, peri_selection, metric_selection, bar_height_toggle)

sum_stats = calculate_summary_stats(df_selected_crops)
top_producer_stats = calculate_top_producers(df_selected_crops)

"""
## 2026 Season
"""
with st.container(horizontal=True, gap="small"):
    with st.container(horizontal=True, gap="medium", border= True):
        st.metric(
            'Weight',
            f"{sum_stats['Total Weight']:.2f} lb",
            width="content",
            delta = f"{sum_stats['Current Week Weight']:.2f} lb",
            format = None,
            delta_description= "Since " +  pd.offsets.Week(weekday=6).rollback(pd.Timestamp.today().normalize()).strftime('%m/%d')
            )

        if top_producer_stats is not None:
            render_top_producers_chart(top_producer_stats, "Weight (lb)", 5)

    with st.container(horizontal=True, gap="medium", border = True):
        st.metric(
            'Value',
            f"{sum_stats['Total Value']:.2f}",
            width="content",
            delta = f"{sum_stats['Current Week Value']:.2f}",
            format = "dollar",
            delta_description= "Since " +  pd.offsets.Week(weekday=6).rollback(pd.Timestamp.today().normalize()).strftime('%m/%d')
            )

        if top_producer_stats is not None: 
                render_top_producers_chart(top_producer_stats, "Value ($)", 5)

"""
## Last 7 Days

"""

week_df = df_selected_crops[df_selected_crops['Date'] > pd.Timestamp.today().normalize() - pd.Timedelta(days=7)]
week_sum_stats = calculate_summary_stats(week_df)
week_top_producer_stats = calculate_top_producers(week_df)

with st.container(horizontal=True, gap="small"):
    with st.container(horizontal=True, gap="medium", border= True):
        st.metric(
            'Weight',
            f"{week_sum_stats['Total Weight']:.2f} lb",
            width="content",
            delta = f"{week_sum_stats['Current Day Weight']:.2f} lb",
            format = None,
            delta_description= "Today"
            )

        if week_top_producer_stats is not None:
            render_top_producers_chart(week_top_producer_stats, "Weight (lb)", 5)

    with st.container(horizontal=True, gap="medium", border = True):
        st.metric(
            'Value',
            f"{week_sum_stats['Total Value']:.2f}",
            width="content",
            delta = f"{sum_stats['Current Day Value']:.2f}",
            format = "dollar",
            delta_description= "Today"
            )
        if week_top_producer_stats is not None: 
            render_top_producers_chart(week_top_producer_stats, "Value ($)", 5)

st.divider() 

"""
## Raw Data

"""
non_sparse_selected_crops = df_selected_crops[df_selected_crops['Weight (lb)'] > 0]
st.dataframe(non_sparse_selected_crops[['Date', 'Item', 'Weight (lb)', 'Value ($)']])
