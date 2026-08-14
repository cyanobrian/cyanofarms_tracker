import streamlit as st
import altair as alt
import pandas as pd 
from data import load_data, calculate_summary_stats, top_producers, item_to_color
from PIL import Image, ImageOps

def top_producers_chart(metric_name, data, num_to_display = 5): 
    # Given metric (str), "Value" or "Weight"
    # Data （tuple) with two dataframes
    # return a bar chart object with the top 5 producing plants
    metric = {"Value ($)": 0, "Weight (lb)": 1}[metric_name]

    data = data[metric][0:min(len(data[metric]), num_to_display)] # Get top 5
    data["Color"] = data['Item'].apply(item_to_color)
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X(f'{metric_name}:Q'), 
        y=alt.Y("Item:N", sort="-x", title = "", axis= alt.Axis(labelLimit=200)),
        color=alt.Color(
            "Color:N",
            scale=None,
            legend=None
        ),
        tooltip=["Item", metric_name]
    )
    return chart

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

""  # Add a little vertical space. Same as st.write("").
""
# images = [ 'tomatoes.jpg', 'squash_kale.jpg', 'chard.jpg', 'butternut.jpg', 'mushroom.jpg']
# paths = ['images/'+ path for path in images]
# img = [ImageOps.exif_transpose(Image.open(path)) for path in paths]


# st.image(img, width= 300)

# # Filter by date range 
# start_date, end_date = st.select_slider(
#     "Select a date range",
#     options= df['Date'].unique(),
#     value=(df['Date'].min(), df['Date'].max()),
# )
# df_filter_plant_date = df_filter_plant[df_filter_plant['Date'].between(start_date, end_date)]

st.header(f'Harvests')
crop_selection = st.multiselect( "Select crops", df['Item'].unique().sort_values(ascending = True),
                                default = df['Item'].unique(), accept_new_options=False
                                )
df_filter_plant = df[df['Item'].isin(crop_selection)]
df_filter_plant['Color'] = df_filter_plant['Item'].apply(item_to_color)

@st.fragment
def render_top_chart(data, granularity, metric):
    index_col = 'Week Range' if granularity=='Week' else 'Date'
    metric_col = 'Weight (lb)' if metric == 'Weight' else 'Value ($)'

    pivoted_data = data.pivot_table(values=metric_col, index=[index_col, 'Item'], aggfunc='sum', fill_value= 0, observed = False).reset_index()
    pivoted_data = pivoted_data[pivoted_data['Item'].isin(crop_selection)]
    pivoted_data['Color'] = pivoted_data['Item'].apply(item_to_color)

    axis_label = {'Week': 'Week Range:O', 'Day': "Date:T"}[granularity]

    x_axis = None
    if granularity == 'Week': 
        x_axis = alt.X(axis_label, title="Week", axis=alt.Axis(labelAngle=0))
    else: 
        x_axis = alt.X(axis_label, title='Date', axis=alt.Axis(format = '%m/%d', labelAngle=0))

    bar = alt.Chart(pivoted_data).mark_bar().encode(
            x= x_axis,
            y=alt.Y(f'{metric_col}:Q', title=metric_col),
            color = alt.Color(
                    "Color:N",
                    scale=None,
                    legend=None
                ),
            tooltip=[
                alt.Tooltip(axis_label),
                alt.Tooltip("Item:N"),
                alt.Tooltip(f'{metric_col}:Q', format=".2f"),
            ],
        )
    
    st.header(f"Harvest by {granularity}")
    st.altair_chart(bar)   



cols = st.columns([0.10, 0.90], gap="medium")
with cols[0]: 
    metric_selection = st.pills("Metric", ['Weight', "Value"], default='Weight', required=True)

with cols[1]: 
    agg_selection = st.pills("Aggregation", ['Week', "Day"], default = 'Week', required=True)
        

with st.container(horizontal=True, gap="medium"):  
    render_top_chart(df, agg_selection, metric_selection)



# st.header(f"Harvest by {agg_selection}")
# chart = render_top_chart(df, agg_selection, metric_selection)
# st.altair_chart(chart)

# tab1, tab2 = st.tabs(["Week", "Day"])
# with tab1:
#     st.header("Harvest by Week")
#     chart = render_top_chart(df, 'Week', metric_selection)
#     st.altair_chart(chart)
# with tab2:
#     st.header("Harvest by Day")
#     chart = render_top_chart(df, 'Day', metric_selection)
#     st.altair_chart(chart)

sum_stats = calculate_summary_stats(df_filter_plant)
top_producer_stats = top_producers(df_filter_plant)

"""
## 2026 Season
"""
with st.container(horizontal=True, gap="medium"):
    cols = st.columns([0.125, 0.375, 0.125, 0.375], gap="medium")

    # Column 0 for totals
    with cols[0]:
        st.metric(
            'Weight',
            f"{sum_stats['Total Weight']:.2f} lb",
            width="content",
            delta = f"{sum_stats['Current Week Weight']:.2f} lb",
            format = None,
            
            delta_description= "Since " +  pd.offsets.Week(weekday=6).rollback(pd.Timestamp.today().normalize()).strftime('%m/%d')
            )

    with cols[1]:
        st.write("Top Producers by Weight")
        if top_producer_stats is not None:
            st.altair_chart(top_producers_chart("Weight (lb)", top_producer_stats, 5))

    with cols[2]:
        st.metric(
            'Value',
            f"{sum_stats['Total Value']:.2f}",
            width="content",
            delta = f"{sum_stats['Current Week Value']:.2f}",
            format = "dollar",
            delta_description= "Since " +  pd.offsets.Week(weekday=6).rollback(pd.Timestamp.today().normalize()).strftime('%m/%d')
            )

    with cols[3]:
        st.write("Top Producers by Value")
        if top_producer_stats is not None: 
            st.altair_chart(top_producers_chart("Value ($)", top_producer_stats, 5))

"""
## Last 7 Days

"""
week_df = df_filter_plant[df_filter_plant['Date'] > pd.Timestamp.today().normalize() - pd.Timedelta(days=7)]
week_sum_stats = calculate_summary_stats(week_df)
week_top_producer_stats = top_producers(week_df)

with st.container(horizontal=True, gap="medium"):
    cols = st.columns([0.125, 0.375, 0.125, 0.375], gap="medium")

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
            st.altair_chart(top_producers_chart("Weight (lb)", week_top_producer_stats, 5))

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
            st.altair_chart(top_producers_chart("Value ($)", week_top_producer_stats, 5))


"""
## Raw Data

"""
st.dataframe(df_filter_plant[['Date', 'Item', 'Weight (lb)', 'Value ($)']])
