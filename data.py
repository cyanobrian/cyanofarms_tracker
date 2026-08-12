import gspread
from google.oauth2.service_account import Credentials
import pandas as pd 

def load_data():
    # Load the data as a dataframe, clean out empty data, and return a pandas Dataframe 
    # 1. Define the scope of the application
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
    ]

    # 2. Authenticate using your credentials JSON file
    cred = Credentials.from_service_account_file("credentials.json", scopes=scopes)
    client = gspread.authorize(cred)

    # 3. Open the spreadsheet by its exact title or URL
    with open("raw_data_url.txt", "r") as file:
        url = file.read()
    spreadsheet = client.open_by_url(url)
    # 4. Select the specific worksheet (tab)
    worksheet = spreadsheet.worksheet("Harvesting")  # Get the Harvesting tab 

    # 5. Extract the data 
    data = worksheet.get('A1:H200') # Get it without $ sign in amounts

    # 6. Import to Dataframe 
    df = pd.DataFrame(data, columns=data[0])
    df = df.drop(0) # Drop the first row now that it's the column label  

    # 7. Clean the data 
    df = df[df['Item'] != ''] # Remove rows where 'Item' is an empty string
    df = df[(df['Item'] != 'Chickpeas') & (df['Item'] != 'Beet Greens')] # Remove since harverst too insignificant


    # Convert all strings to numbers in columns where appropriate 
    col_to_num = ['Weight (g)','Weight (lb)', 'Lowerbound Value ($)','Value ($)', 'Week']
    df['Value ($)'] = df['Value ($)'].str.replace('$', '', regex=False)
    df['Lowerbound Value ($)'] = df['Lowerbound Value ($)'].str.replace('$', '', regex=False)

    for col in col_to_num: 
        df[col] = pd.to_numeric(df[col])

    df['Date'] = pd.to_datetime(df['Date'])

    return df 

def calculate_summary_stats(df):
    summary_stats = {} 

    # Total Weight from Season 
    summary_stats['Total Weight'] = df['Weight (lb)'].sum()

    # Weight from Current Week
    current_week = df[df['Week'] == df["Week"].max()]
    summary_stats['Current Week Weight'] = current_week['Weight (lb)'].sum()

    # All Time Value
    summary_stats['Total Value'] = df['Value ($)'].sum()

    # Current Week Value 
    summary_stats['Current Week Value'] = current_week['Value ($)'].sum()


    current_day = df[df['Date'] == pd.Timestamp.today().normalize()]
    summary_stats['Current Day Weight'] = current_day['Weight (lb)'].sum()
    summary_stats['Current Day Value'] = current_day['Value ($)'].sum()

    # Get harvest data from up to current weekday, last week 
    # prev_week = df[(df['Week'] == df["Week"].max()-1) &
    #                 (df['Date'] <= pd.Timestamp.today().normalize() - pd.Timedelta(days=7))]
    # prev_week_weight = prev_week['Weight (lb)'].sum()
    # prev_week_savings = prev_week['Value ($)'].sum()

    # curr_week_weight = curr_week['Weight (lb)'].sum()
    # curr_week_savings = curr_week['Value ($)'].sum()


    # Percent Change to Previous Week
    # summary_stats['Weight Delta'] = (curr_week_weight - prev_week_weight)
    # summary_stats['Savings Delta'] = (curr_week_savings - prev_week_savings)
    # print(summary_stats)
    return summary_stats

def top_producers(df): 
    df_item_pivot = pd.pivot_table(df, values=['Weight (lb)', 'Value ($)'], index='Item', aggfunc='sum')
    best_value = df_item_pivot.sort_values('Value ($)', ascending=False)
    best_weight = df_item_pivot.sort_values('Weight (lb)', ascending=False)

    # curr_week = df[df['Date'] >= pd.Timestamp.today().normalize() - pd.Timedelta(days=7)]
    # df_week_item_pivot = pd.pivot_table(curr_week, values=['Weight (lb)', 'Value ($)'], index='Item', aggfunc='sum')

    # best_week_value = None
    # best_week_weight = None
    # if len(df_item_pivot) >= 1: 
    #     best_week_value= df_week_item_pivot.sort_values('Value ($)', ascending=False)
    #     best_week_weight = df_week_item_pivot.sort_values('Weight (lb)', ascending=False)

    # return (best_value, best_weight, best_week_value, best_week_weight)
    return (best_value, best_weight)




df = load_data()
# print(pd.pivot_table(df, values=['Weight (lb)', 'Value ($)'], columns=['Week', 'Item'], aggfunc='sum'))
# print(calculate_summary_stats(df).keys())
