import altair as alt
import streamlit as st

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

    st.altair_chart(chart + labels)


def render_main_bar(data, granularity, metric, include_bars = True):
    index_col = 'Week Range' if granularity=='Week' else 'Date'
    metric_col = 'Weight (lb)' if metric == 'Weight' else 'Value ($)'
    if granularity != 'Day':
        data = (
            data.groupby([index_col, 'Item'], as_index=False)
            .agg({
                metric_col:'sum',
                "Color": 'first'
            })
        )
        data.rename(columns = {'c': metric_col}, inplace = True)



    axis_label = {'Week': 'Week Range:O', 'Day': "Date:T"}[granularity]
    x_axis = None
    if granularity == 'Week': 
        x_axis = alt.X(axis_label, title="Week", axis=alt.Axis(labelAngle=0))
    else: 
        x_axis = alt.X(axis_label, title='Date', axis=alt.Axis(format = '%m/%d', labelAngle=0))

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
        )
    st.header(f"Harvest by {granularity}")

    if not include_bars:
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