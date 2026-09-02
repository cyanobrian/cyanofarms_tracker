import streamlit as st
import pandas as pd 
from data import load_data, calculate_summary_stats, calculate_top_producers, calculate_change
from render import render_main_bar, render_top_producers_chart, render_cumulative, render_leaderboard
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
        include_bars = st.pills("Bar Heights", ['Show', "Hide"], default = 'Show', required=True) == 'Show'

    render_main_bar(df_selected_crops, peri_selection, metric_selection, include_bars)
    render_cumulative(df_selected_crops, peri_selection, metric_selection, include_bars)
    # render_leaderboard(calculate_change(df_selected_crops, 'Weight'), 'Weight (lb)')
    
    # st.header('Leaderboard')
    # options = {
    #             'Today':pd.Timestamp.today().normalize(),
    #             'Current Week': pd.offsets.Week(weekday=6).rollback(pd.Timestamp.today().normalize()),
    #             'Last 7 Days': pd.Timestamp.today().normalize() - pd.Timedelta(days=6),
    #             'Last 30 Days':pd.Timestamp.today().normalize() - pd.Timedelta(days=29),
    #             }
    # comparison_date = st.pills("Comparison Date", options.keys(), selection_mode="single", required= True, default='Today')
    # rank_data = calculate_change(df_selected_crops, metric_selection, options[comparison_date])

    # st.dataframe(rank_data)


    # def style_director(val):
    #     colors_select = {
    #     "Arugula": "#4F8A3D",
    #     "Basil": "#245E32",
    #     "Beet Greens": "#88AE47",
    #     "Chickpeas": "#D4A84F",
    #     "Kale, Vates": "#176B6B",
    #     "Kale, Red Russian": "#874F68",
    #     "Oyster Mushrooms": "#A99B8C",
    #     "Summer Squash": "#B89C1F",
    #     "Swiss Chard": "#2E7D6B",
    #     "Tomatoes": "#C8463D",
    #     "Zucchini, Elite": "#054705",
    #     "Zucchini, Pantheon": "#6E8B2E"
    #     }
    #     color = colors_select.get(val, "#e5e7eb")

    #     return (
    #         f"background-color: {color};"
    #         "border-radius: 6px;"
    #         "color: #FFFFFF;"
    #         "padding: 5px 5px;"
    #         "font-weight: bold;"
    #         "border : 0.5px solid white"
    #         "display: inline-block;"
    #     )


    # styled = rank_data.style.map(style_director, subset=["Item"])
    # st.table(styled)
    # if metric_selection == 'Weight': 
    #     with st.container(horizontal=True):
    #         for index, rows in rank_data.iterrows():
    #             st.metric(f'{index+1}. {rows['Item']}', f'{rows['Current Weight (lb)']:.2f} lb',
    #                     delta = f'{rows['Rank Change']:+};  +{rows['Weight Change (lb)']:.2f} lb',
    #                     delta_arrow='off',
    #                     delta_color='off')

    # else: 
    #     with st.container(horizontal=True):
    #         for index, rows in rank_data.iterrows():
    #             st.metric(f'{index+1}. {rows['Item']}', f'${rows['Current Value ($)']:.2f}',
    #                     delta = f'{rows['Rank Change']:+};  +${rows['Value Change ($)']:.2f}',
    #                     # delta = [f'{rows['Rank Change']:+}',  f'+${rows['Value Change ($)']:.2f}'],
    #                     delta_arrow='off',
    #                     delta_color='off')
    #     # print(rows['Current Weight (lb)'])


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
# print(non_sparse_selected_crops)
st.dataframe(non_sparse_selected_crops[['Date', 'Item', 'Weight (lb)', 'Value ($)']])
