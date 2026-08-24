import pandas as pd 
import streamlit as st
from streamlit_gsheets import GSheetsConnection

def item_to_color(item):
    '''
    Given an crop, return the corresponding color hex code 

    Parameters: 
    item (str): name of the crop 

    Returns: 
    str: corresponding color hex value 
    '''
    # Converts items to corresponding hex code colors 
    colors = {
    "Arugula": "#4F8A3D",
    "Basil": "#245E32",
    "Beet Greens": "#88AE47",
    "Butternut Squash": "#E19A3C",
    "Chickpeas": "#D4A84F",
    "Kale, Vates": "#176B6B",
    "Kale, Red Russian": "#874F68",
    "Oyster Mushrooms": "#A99B8C",
    "Summer Squash": "#E0C13A",
    "Swiss Chard": "#2E7D6B",
    "Tomatoes": "#C8463D",
    "Zucchini, Elite": "#054705",
    "Zucchini, Pantheon": "#6E8B2E"
    }
    if item not in colors: 
        return "#525252"
    return colors[item]


def load_data():
    '''
    Load the data from the google sheet in secrets.toml and necessary data cleaning operations 

    Parameters: 
    None 

    Returns: 
    Dataframe: Dataframe of cleaned data 
    '''
    # Create a connection object
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(worksheet="Harvesting",ttl="10m",usecols=list(range(0,7)),nrows=200)

    # Clean the data 
    df = df.dropna(axis = 0, subset = ['Date', 'Item']) # Remove rows where 'Date' or 'Item' are Na
    df['Item'] = df['Item'].astype('category')     # Convert a category

    # Convert all strings to numbers in columns where appropriate 
    col_to_num = ['Weight (g)','Weight (lb)', 'Lowerbound Value ($)','Value ($)']
    for col in col_to_num: 
        df[col] = pd.to_numeric(df[col])

    # Convert date to Pandas datetime object 
    df['Date'] = pd.to_datetime(df['Date'])

    # Create a sparse representation of datan by inserting 0 for each crop on days when no harvests, 
    df = df.pivot_table(values=['Weight (lb)', 'Value ($)'], index=['Date', 'Item'], aggfunc='sum', fill_value= 0, observed = False).reset_index()

    # Add Week Range 
    week_begin_date = df['Date'].apply(lambda date: pd.offsets.Week(weekday=6).rollback(date.normalize()))
    week_end_date = week_begin_date.apply(lambda x: x + pd.Timedelta(days=6))
    df.insert(0, "Week Range", 
        [f"{d1.strftime('%m/%d')}-{d2.strftime('%m/%d')}" for d1, d2 in zip(week_begin_date, week_end_date)]

    )
    # Add Color
    df['Color'] = df['Item'].apply(item_to_color)
    return df

def calculate_summary_stats(df):
    '''
    Calculate metrics to display on dashboard 
    Parameters: 
    df (Dataframe): Dataframe with the cleaned data

    Returns: 
    Dictionary: contains value for total weight and value of entire season, 
        current week (since most recent Sunday), and current day 
    '''
    summary_stats = {} 

    # Season Total Data 
    summary_stats['Total Weight'] = df['Weight (lb)'].sum()
    summary_stats['Total Value'] = df['Value ($)'].sum()

    # Current Week Data 
    most_recent_saturday = pd.offsets.Week(weekday=5).rollback(pd.Timestamp.today().normalize())
    current_week = df[df['Date'] > most_recent_saturday] 

    summary_stats['Current Week Weight'] = current_week['Weight (lb)'].sum()
    summary_stats['Current Week Value'] = current_week['Value ($)'].sum()

    # Current Day Data
    current_day = df[df['Date'] == pd.Timestamp.today().normalize()]
    
    summary_stats['Current Day Weight'] = current_day['Weight (lb)'].sum()
    summary_stats['Current Day Value'] = current_day['Value ($)'].sum()

    return summary_stats

def calculate_top_producers(df): 
    '''
    Calculate top producing crops by weight and value   
    Parameters: 
    df (Dataframe): Dataframe with the cleaned data

    Returns: 
    Tuple: (Dataframe, Dataframe), contains the top producers by weight at 0 and top producers by value 1 
    None: If the length of the argument Dataframe  is 0 
    '''
    if len(df) == 0: 
        return None
    # Aggregate the data based on Item and get the sum of weight and value 
    aggreg_data = df.groupby('Item', as_index=False).agg({
                            'Weight (lb)':'sum',
                            'Value ($)': 'sum',
                            "Color": 'first'
                        })
    
    # Sort the data 
    best_value = aggreg_data.sort_values('Value ($)', ascending=False).reset_index(drop=True)
    best_weight = aggreg_data.sort_values('Weight (lb)', ascending=False).reset_index(drop=True)
    return (best_weight, best_value)

def position_change(df, time): 
    None
# def get_cumulative_data(df): 
#     '''
#     Calculate a cumulative sum of the data 

#     Parameters: 
#     df (Dataframe): Dataframe with the cleaned data

#     Returns: 
#     '''
#     index_col = 'Date' # 'Week Range'
#     metric_col = 'Weight (lb)' #'Value ($)'
#     data = df.groupby([index_col], as_index=False).agg({metric_col:'sum'})
#     df[f'Cumulative {metric_col}'] = df[metric_col].cumsum()

def calculate_change(df, metric, comparison_date): 
    '''
    Calculate change in position for top performing crops
    Parameters: 
    df (Dataframe): Dataframe with the cleaned data

    Returns: 
    Tuple: (Dataframe, Dataframe), contains the top producers by weight at 0 and top producers by value 1 
    None: If the length of the argument Dataframe  is 0 
    '''
    if len(df) == 0: 
        return None
    
    metric_col = 'Weight (lb)' if metric == 'Weight' else 'Value ($)'

    prev_df = df[df['Date'] < comparison_date]

    agg_data = lambda x, m: x.groupby('Item', as_index=False).agg({
                            m:'sum',
                            "Color": 'first'
                        }).sort_values(m, ascending=False).reset_index(drop= True).reset_index()

    prev = agg_data(prev_df, metric_col)
    curr = agg_data(df, metric_col)

    merged = pd.merge(curr, prev, on='Item')
    merged['Rank Change'] = merged['index_y']-merged['index_x']

    merged.drop(columns='Color_y', inplace= True)
    merged.rename(columns={f'{metric_col}_x': f'Current {metric_col}', 
                           f'{metric_col}_y': f'Previous {metric_col}',
                           'index_x': 'Current Rank', 
                           'index_y': 'Previous Rank', 
                           'Color_x': 'Color'
    }, inplace=True)
    unit = '(lb)' if metric == 'Weight' else '($)'
    merged[f'{metric} Change {unit}'] = merged[f'Current {metric_col}'] - merged[f'Previous {metric_col}']
    # Reorder columns 
    merged = merged[['Item', 'Color', 'Current Rank', 'Previous Rank', 'Rank Change', 
                     f'Current {metric_col}', f'Previous {metric_col}', f'{metric} Change {unit}']]

    merged = merged[['Item', 'Current Rank', 'Rank Change', 
                         f'Current {metric_col}', f'{metric} Change {unit}']]
    # merged[['Item', metric_col, ],]
    return merged 

# df = load_data()
# agged = df.groupby('Item', as_index=False).agg({
#     'Weight (lb)':'sum',
#     'Value ($)': 'sum',
#     "Color": 'first'
#     })

# calculate_top_producers_change(df, 'Weight')
# print(calculate_top_producers(calculate_top_producers(df)[1]))
# get_cumulative_data(df)