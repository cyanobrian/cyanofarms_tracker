import pandas as pd 
import streamlit as st
from streamlit_gsheets import GSheetsConnection

def item_to_color(item):
    # Converts series of items to hex code colors 
    colors = {
    "Arugula": "#4F8A3D",
    "Basil": "#245E32",
    "Beet Greens": "#88AE47",
    "Chickpeas": "#D4A84F",
    "Kale, Vates": "#176B6B",
    "Kale, Red Russian": "#874F68",
    "Oyster Mushrooms": "#A99B8C",
    "Summer Squash": "#E0C13A",
    "Swiss Chard": "#2E7D6B",
    "Tomatoes": "#C8463D",
    "Zucchini, Elite": "#054705",
    "Zucchini, Costata Romanesco": "#6E8B2E"
    }

    return colors[item]


def load_data():
    # Create a connection object.
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(worksheet="Harvesting",ttl="10m",usecols=list(range(0,7)),nrows=200)

    # Clean the data 
    df = df.dropna(axis = 0, subset = ['Date', 'Item']) # Remove rows where 'Date' or 'Item' are Na
    df['Item'] = df['Item'].astype('category')     # Convert a category

    # Convert all strings to numbers in columns where appropriate 
    col_to_num = ['Weight (g)','Weight (lb)', 'Lowerbound Value ($)','Value ($)']
    for col in col_to_num: 
        df[col] = pd.to_numeric(df[col])

    # Convert week column to the week start day 
    df['Date'] = pd.to_datetime(df['Date'])

    # insert 0 for each crop on days when no harvests 
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
    if len(df) == 0: 
        return None
    df_item_pivot = pd.pivot_table(df, values=['Weight (lb)', 'Value ($)'], index='Item', aggfunc='sum')
    best_value = df_item_pivot.sort_values('Value ($)', ascending=False).reset_index()
    best_weight = df_item_pivot.sort_values('Weight (lb)', ascending=False).reset_index()
    best_value['Color'] = best_value['Item'].apply(item_to_color)
    best_weight['Color'] = best_weight['Item'].apply(item_to_color)

    return (best_weight, best_value)




# df = load_data()
