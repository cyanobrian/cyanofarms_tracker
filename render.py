import altair as alt
import streamlit as st
import streamlit as st
import pandas as pd

def render_top_producers_chart(data, metric, num_to_display = 5): 
    '''
    Render the top producers charts

    Parameters: 
    data (Tuple): (Dataframe, Dataframe) with the aggregated data, returned by calculate_top_producers(df)
        Dataframe at index 0 is top producers by Weight and Dataframe at index 1 is top producers by Value 
    metric (str): either 'Weight (lb)' or 'Value ($)', metric to measure production
    num_to_display (int): display the top num_to_display producers for the metric 

    Returns: 
    None
    '''

    metric_col = { "Weight (lb)": 0, "Value ($)": 1}[metric]
    data = data[metric_col][0:min(len(data[metric_col]), num_to_display)] # Get top 5 or less, all of them 

    # Create bar chart 
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X(f'{metric}:Q'), 
        y=alt.Y("Item:N", sort="-x", title = "", axis= alt.Axis(labelLimit=200)),
        color=alt.Color(
            "Color:N",
            scale=None,
            legend=None
        ),
        tooltip=[alt.Tooltip("Item:N"), alt.Tooltip(f'{metric}:Q', format=".2f")]
    )
    # Add labels 
    labels = alt.Chart(data).mark_text(
        align="left",
        baseline="middle",
        dx=5,
        color="white"
    ).encode(
        x=alt.X(f"{metric}:Q"),
        y=alt.Y("Item:N", sort="-x"),
        text=alt.Text(f"{metric}:Q", format=",.2f")
    )
    # title=alt.TitleParams(text = f'Top Producers by {metric_name}', anchor = 
    #                                               'middle',fontWeight='normal' )
    
    st.altair_chart(chart + labels)

def render_main_bar(data, period, metric, include_bars = True):
    '''
    Render the main bar chart 

    Parameters: 
    data (Dataframe): Dataframe with the cleaned data
    period (str): either 'Week' or 'Day', period to display the data 
    metric (int): either 'Weight (lb)' or 'Value ($)', metric to measure production
    include_bars (bool): whether or not to display the height of the bars 

    Returns: 
    None
    '''
    metric_col = 'Weight (lb)' if metric == 'Weight' else 'Value ($)'

    index_col = None # Name of the column in data 
    x_axis = None # X axis object 

    if period == 'Week':
        index_col = 'Week Range'

        # need to aggregate data to week 
        data = data.groupby(['Week Range', 'Item'], as_index=False).agg({metric_col:'sum',"Color": 'first'})
        x_axis = alt.X('Week Range:O', title="Week", axis=alt.Axis(labelAngle=0))


    else: 
        index_col = 'Date'
        # Display only harvests from the past 30 days to prevent overcrowding if choosing days  
        max_date = pd.Timestamp.today()
        min_date = max_date - pd.Timedelta(days=30)

        x_axis = alt.X('Date:T', title='Date', axis=alt.Axis(format = '%m/%d', labelAngle=0),
                       scale=alt.Scale(domain = [min_date, max_date]))

    bar = alt.Chart(data).mark_bar().encode(
            x= x_axis,
            y=alt.Y(f'{metric_col}:Q', title=metric_col),
            color = alt.Color(
                    "Color:N",
                    scale=None,
                    legend=None
                ),
            tooltip=[ # Info to display when hovering over the bars
                alt.Tooltip(index_col),
                alt.Tooltip("Item:N"),
                alt.Tooltip(f'{metric_col}:Q', format=".2f"),
            ],
        ).interactive(bind_y = False)
    st.header(f"Harvest by {period}")

    if not include_bars:
        st.altair_chart(bar) 
        return 
    
    # Include labels of bar height if specified 
    bar_heights = data.groupby(index_col, as_index=False)[metric_col].sum()
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


def render_cumulative(data, period, metric, include_bars):
    metric_col = 'Weight (lb)' if metric == 'Weight' else 'Value ($)'

    x_axis = None
    if period == 'Week':
        # Aggregate data by week 
        data = data.groupby(['Week Range'], as_index=False).agg({metric_col:'sum'})
        x_axis = alt.X('Week Range:O', title="Week", axis=alt.Axis(labelAngle=0))
    else: 
        # Aggregate data by day 
        data = data.groupby(['Date'], as_index=False).agg({metric_col:'sum'})
        max_date = pd.Timestamp.today()
        min_date = max_date - pd.Timedelta(days=30)

        # Display only past 30 days 
        x_axis = alt.X('Date:T', title='Date', axis=alt.Axis(format = '%m/%d', labelAngle=0),
                       scale=alt.Scale(domain = [min_date, max_date]))


    # Add cumulative sum column 
    cum_col = f'Cumulative {metric_col}'
    data[cum_col] = data[metric_col].cumsum()

    bar = alt.Chart(data).mark_line().encode(
            x= x_axis,
            y=alt.Y(f'{cum_col}:Q', title=cum_col),
            tooltip=[
                alt.Tooltip(metric_col),
                alt.Tooltip("Item:N"),
                alt.Tooltip(f'{cum_col}:Q', format=".2f"),
            ],
        ).interactive(bind_y = False)
    st.header(f"Cumulative Harvest by {period}")

    if not include_bars:
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



def render_leaderboard(data, metric): 
    '''
    Render the top producers charts

    Parameters: 
    data (Tuple): (Dataframe, Dataframe) with the aggregated data, returned by calculate_top_producers(df)
        Dataframe at index 0 is top producers by Weight and Dataframe at index 1 is top producers by Value 
    metric (str): either 'Weight (lb)' or 'Value ($)', metric to measure production
    num_to_display (int): display the top num_to_display producers for the metric 

    Returns: 
    None
    '''

    metric_col = f'Current {metric}'
    metric_change = f'Weight Change (lb)'
    # Create bar chart 
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X(f'{metric_col}:Q'), 
        y=alt.Y("Item:N", sort="-x", title = "", axis= alt.Axis(labelLimit=200)),
        color=alt.Color(
            "Color:N",
            scale=None,
            legend=None
        ),
        tooltip=[alt.Tooltip("Item:N"), alt.Tooltip(f'{metric_col}:Q', format=".2f")]
    )
    # Add labels 
    labels = alt.Chart(data).mark_text(
        align="left",
        baseline="middle",
        dx=5,
        color="white"
    ).encode(
        x=alt.X(f"{metric_col}:Q"),
        y=alt.Y("Item:N", sort="-x"),
        text=alt.Text(f"{metric_col}:Q", format=",.2f")
    )
    labels_2 = alt.Chart(data).mark_text(
        align="right",
        baseline="middle",
        dx=5,
        color="white"
    ).encode(
        x=alt.X(f"{metric_change}:Q"),
        y=alt.Y("Item:N", sort="-x"),
        text=alt.Text(f"{metric_change}:Q", format=",.2f")
    )
    # title=alt.TitleParams(text = f'Top Producers by {metric_name}', anchor = 
    #                                               'middle',fontWeight='normal' )
    
    st.altair_chart(chart + labels+labels_2)