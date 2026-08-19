import altair as alt
import streamlit as st
# import plotly.graph_objects as go
import streamlit as st
import pandas as pd

def render_top_producers_chart(data, metric_name, num_to_display = 5): 
    # Given metric (str), "Value" or "Weight"
    # Data （tuple) with two dataframes
    # return a bar chart object with the top 5 producing plants
    metric = { "Weight (lb)": 0, "Value ($)": 1}[metric_name]

    data = data[metric][0:min(len(data[metric]), num_to_display)] # Get top 5
    # data["Color"] = data['Item'].apply(item_to_color)

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
    labels = alt.Chart(data).mark_text(
        align="left",
        baseline="middle",
        dx=5,
        color="white"
    ).encode(
        x=alt.X(f"{metric_name}:Q"),
        y=alt.Y("Item:N", sort="-x"),
        text=alt.Text(f"{metric_name}:Q", format=",.2f")
    )
    # title=alt.TitleParams(text = f'Top Producers by {metric_name}', anchor = 
    #                                               'middle',fontWeight='normal' )
    
    st.altair_chart(chart + labels)


# def render_main_bar(data, granularity, metric, include_bars=True):

#     index_col = 'Week Range' if granularity == 'Week' else 'Date'
#     metric_col = 'Weight (lb)' if metric == 'Weight' else 'Value ($)'

#     # Aggregate if using weekly data
#     if granularity != 'Day':
#         data = (
#             data.groupby([index_col, 'Item'], as_index=False)
#             .agg({
#                 metric_col: 'sum',
#                 'Color': 'first'
#             })
#         )

#     st.header(f"Harvest by {granularity}")

#     # Create total for each time period
#     bar_heights = (
#         data.groupby(index_col, as_index=False)[metric_col]
#         .sum()
#     )

#     fig = go.Figure()

#     # Add bars
#     if include_bars:
#         for item in data['Item'].unique():

#             item_data = data[data['Item'] == item]

#             color = item_data['Color'].iloc[0]

#             fig.add_trace(
#                 go.Bar(
#                     x=item_data[index_col],
#                     y=item_data[metric_col],
#                     name=item,
#                     marker_color=color,
#                     hovertemplate=(
#                         f"{index_col}: %{{x}}<br>"
#                         f"Item: {item}<br>"
#                         f"{metric_col}: %{{y:.2f}}"
#                         "<extra></extra>"
#                     )
#                 )
#             )

#     # Add total labels above each bar
#     if include_bars:

#         fig.add_trace(
#             go.Scatter(
#                 x=bar_heights[index_col],
#                 y=bar_heights[metric_col],
#                 mode='text',
#                 text=bar_heights[metric_col].map(lambda x: f"{x:.2f}"),
#                 textposition='top center',
#                 textfont=dict(
#                     color='#e2e8f0'
#                 ),
#                 showlegend=False,
#                 hoverinfo='skip'
#             )
#         )

#     # Horizontal scrolling
#     # Increase this to make each time period wider.
#     chart_width = max(800, len(bar_heights) * 80)

#     fig.update_layout(
#         width=chart_width,
#         height=500,

#         barmode='stack',

#         xaxis=dict(
#             title='Week' if granularity == 'Week' else 'Date',
#             type='category',
#             tickangle=0,
#         ),

#         yaxis=dict(
#             title=metric_col
#         ),

#         showlegend=False,

#         margin=dict(
#             l=50,
#             r=20,
#             t=30,
#             b=50
#         )
#     )

#     # Streamlit horizontal scroll container
#     st.markdown(
#         f"""
#         <div style="
#             width: 100%;
#             overflow-x: auto;
#             overflow-y: hidden;
#         ">
#             <div style="width: {chart_width}px;">
#         """,
#         unsafe_allow_html=True
#     )

#     st.plotly_chart(
#         fig,
#         # use_container_width=False,
#         config={
#             'displayModeBar': False
#         }
#     )

#     st.markdown(
#         """
#             </div>
#         </div>
#         """,
#         unsafe_allow_html=True
#     )
def render_main_bar(data, period, metric, include_bars = 'Visible'):
    index_col = 'Week Range' if period=='Week' else 'Date'
    metric_col = 'Weight (lb)' if metric == 'Weight' else 'Value ($)'
    if period != 'Day':
        data = (
            data.groupby([index_col, 'Item'], as_index=False)
            .agg({
                metric_col:'sum',
                "Color": 'first'
            })
        )
        data.rename(columns = {'c': metric_col}, inplace = True)



    axis_label = {'Week': 'Week Range:O', 'Day': "Date:T"}[period]
    x_axis = None
    if period == 'Week': 
        x_axis = alt.X(axis_label, title="Week", axis=alt.Axis(labelAngle=0))
    else: 
        # By default, display only harvests from the past 30 days to prevent overcrowding 
        max_date = data[index_col].max()
        min_date = max_date - pd.Timedelta(days=30)
        x_axis = alt.X(axis_label, title='Date', axis=alt.Axis(format = '%m/%d', labelAngle=0),
                       scale=alt.Scale(domain = [min_date, max_date]))

    bar = alt.Chart(data).mark_bar().encode(
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
        ).interactive(name = "moomoo", bind_y = False)
    st.header(f"Harvest by {period}")

    if include_bars == 'Invisible':
        st.altair_chart(bar) 
        return 
    
    # Include labels if specified 
    bar_heights = (
        data
        .groupby(index_col, as_index=False)[metric_col]
        .sum()
    )
    labels = alt.Chart(bar_heights).mark_text(
        align="center",
        baseline="bottom",
        dy=-5,
        color= "#e2e8f0"
    ).encode(
        x=x_axis,
        y=alt.Y(f'{metric_col}:Q'),
        text=alt.Text(
            f'{metric_col}:Q',
            format=".2f"
        )
    )
    st.altair_chart(bar + labels)   


def render_cumulative(data, period, metric, include_bars = 'Visible'):
    index_col = 'Week Range' if period=='Week' else 'Date'
    metric_col = 'Weight (lb)' if metric == 'Weight' else 'Value ($)'

    # Add cumulative sum column 
    data = data.groupby([index_col], as_index=False).agg({metric_col:'sum'})
    cum_col = f'Cumulative {metric_col}'
    data[cum_col] = data[metric_col].cumsum()


    axis_label = {'Week': 'Week Range:O', 'Day': "Date:T"}[period]
    x_axis = None
    if period == 'Week': 
        x_axis = alt.X(axis_label, title="Week", axis=alt.Axis(labelAngle=0))
    else: 
        x_axis = alt.X(axis_label, title='Date', axis=alt.Axis(format = '%m/%d', labelAngle=0))

    bar = alt.Chart(data).mark_line().encode(
            x= x_axis,
            y=alt.Y(f'{cum_col}:Q', title=cum_col),
            tooltip=[
                alt.Tooltip(axis_label),
                alt.Tooltip("Item:N"),
                alt.Tooltip(f'{cum_col}:Q', format=".2f"),
            ],
        ).interactive(name = "moomoo", bind_y = False)
    st.header(f"Cumulative Harvest by {period}")
    if include_bars == 'Invisible':
        st.altair_chart(bar) 
        return 
    
    # Include labels if specified 
    labels = alt.Chart(data).mark_text(
        align="center",
        baseline="bottom",
        dy=-5,
        color= "#e2e8f0"
    ).encode(
        x=x_axis,
        y=alt.Y(f'{cum_col}:Q'),
        text=alt.Text(
            f'{cum_col}:Q',
            format=".2f"
        )
    )
    st.altair_chart(bar + labels)   