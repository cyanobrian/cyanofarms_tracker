from urllib import response

import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from st_supabase_connection import SupabaseConnection
import altair as alt

import streamlit as st
from st_supabase_connection import SupabaseConnection
from datetime import datetime

st.title("Cyano Farms Test Entry")


import streamlit as st


def check_password():
  """
  Returns True if the user had the correct password.
  """

  def password_entered():
    if st.session_state["password"] == st.secrets["PASSWORD"]:
      st.session_state["password_correct"] = True
      del st.session_state["password"]  # don't store password
    else:
      st.session_state["password_correct"] = False

  if "password_correct" not in st.session_state:
    # First run, show input for password.
    st.text_input(
        "Enter password to enable submission", type="password", on_change=password_entered, key="password"
    )
    return False
  elif not st.session_state["password_correct"]:
    # Password incorrect, show input + error.
    st.text_input(
        "Enter password to enable submission", type="password", on_change=password_entered, key="password"
    )
    st.error("Incorrect Password")
    return False
  else:
    # Password correct.
    return True

crop_submit_button = True 
harvest_submit_button = True 

if check_password():
  # Put the rest of your Streamlit app code here
  crop_submit_button = False 
  harvest_submit_button = False 


# Initialize connection.
conn = st.connection("supabase", type=SupabaseConnection)

# Perform query to get all crops from database
rows = conn.table("Crops").select("*").execute()
crops_dict = {}
for row in rows.data:
    crops_dict[row["crop_name"]] = row["crop_id"]
crops_list = sorted(crops_dict.keys())


def save_harvest():
    """
    Save the harvest data to the database. This function is called when the user submits the harvest form.

    Parameters:
    None

    Returns:
    None
    """
    date, weight, crop, notes = (
        st.session_state.h_date,
        st.session_state.h_weight,
        st.session_state.h_crop,
        st.session_state.h_notes,
    )
    dt = datetime(date.year, date.month, date.day)
    week = (
        int(dt.strftime("%U")) + 1
    )  # +1 because strftime returns 0-51 for weeks, but we want 1-52
    crop_id = crops_dict[crop]

    conn.table("Harvests").insert(
        {
            "date": str(date),
            "crop_id": crop_id,
            "weight": float(weight),
            "notes": notes,
            "week": week,
        }
    ).execute()


# Form to enter harvest data into database
st.write("Record Harvest")
with st.form(key="record_harvest", clear_on_submit=True):
    date = st.date_input(
        "Harvest Date", format="MM/DD/YYYY", value="today", key="h_date"
    )
    weight = st.text_input(
        "Weight (g)", placeholder="Enter weight...", required=True, key="h_weight"
    )
    crop = st.selectbox(
        "Crop", crops_list, index=None, placeholder="Select crop...", key="h_crop"
    )
    notes = st.text_area(
        "Notes", placeholder="Enter any notes here...", height=100, key="h_notes"
    )

    st.form_submit_button("Submit", on_click=save_harvest, disabled=harvest_submit_button)


# Get all unique crop categories in alphabetical order
categories = set()
for row in rows.data:
    categories.add(row["category"])
categories = sorted(categories)


def save_crop():
    """
    Save the crop data to the database. This function is called when the user submits the crop form.

    Parameters:
    None

    Returns:
    None
    """
    conn.table("Crops").insert(
        {
            "crop_name": st.session_state.c_name,
            "price": float(st.session_state.c_price),
            "category": st.session_state.c_category,
        }
    ).execute()


# Form to enter new crop data into database
st.write("Add New Crop or Update Price")
with st.form(key="add_crop", clear_on_submit=True, enter_to_submit=True):
    price = st.text_input("Price ($/lb)", placeholder="0", required=True, key="c_price")
    new_crop_name = st.text_input(
        "Crop Name", placeholder="Enter crop name...", required=True, key="c_name"
    )
    category = st.selectbox(
        "Category",
        categories,
        index=None,
        placeholder="Select category...",
        accept_new_options=True,
        key="c_category",
    )
    st.form_submit_button("Submit", on_click=save_crop, disabled=crop_submit_button)


# # 1. Create dummy data with 10 categories
# data = pd.DataFrame({
#     'Item': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
#     'Value': [95, 85, 75, 65, 55, 45, 35, 25, 15, 5],
#     'Begin': [0,0,0,0,0,0,0,0,0,0],
#     'Range': pd.date_range(start="2026-09-04", periods=10, freq="D"),
#     'Color':[
#     "#4A90E2",
#     "#50E3C2",
#     "#B8E986",
#     "#F5A623",
#     "#E2847A",
#     "#9B51E0",
#     "#34495E",
#     "#E74C3C",
#     "#2ECC71",
#     "#1ABC9C"
# ]
# })

# data = data.reset_index()


# # y_axis = alt.Y('index:O', sort = '-x', title = "", axis=alt.Axis(labelLimit=200))
# # chart = alt.Chart(data).mark_bar().encode(
# #     x='Value:Q',
# #     y=y_axis
# # ).properties(height=700)


# # items_to_display = data_full[0:min(len(data_full), num_to_display)]['Item'].to_list() # Get top 5 or less, all of them

# # Create bar chart
# # y_axis = alt.Y('Item:N', sort = '-x', title = "", axis=alt.Axis(labelLimit=200),
# #             scale=alt.Scale(domain = items_to_display))
# y_axis_name = 'Range:O'
# # y_axis = alt.Y(y_axis_name, sort = '-x', title = "", axis=alt.Axis(labelLimit=200),)

# max_date = pd.Timestamp.today()
# min_date = max_date + pd.Timedelta(days=5)
# y_axis = alt.Y('Range:T', sort = "-y",axis = None,  scale=alt.Scale(domain = [min_date, max_date], reverse=True))
#             # scale=alt.Scale(domain = items_to_display))

# chart = alt.Chart(data).mark_bar(size = 30).encode(
#     x=alt.X(f'Value:Q'),
#     # y=alt.Y("Item:N", sort="-x", title = "", axis= alt.Axis(labelLimit=200)),
#     y = y_axis,
#     color=alt.Color(
#         "Color:N",
#         scale=None,
#         legend=None
#     ),
#     tooltip=[alt.Tooltip('Item:N'), alt.Tooltip('Value:Q', format=".2f")]
# ).interactive(bind_x = False)
# # Add labels
# # labels = alt.Chart(data).mark_text(
# #     align="left",
# #     baseline="middle",
# #     dx=5,
# #     color="white"
# # ).encode(
# #     x=alt.X("Value:Q"),
# #     y=alt.Y("Range:T", sort="-x"),
# #     text=alt.Text("Value:Q", format=",.2f")
# # )

# # Add labels
# labels_2 = alt.Chart(data).mark_text(
#     align="right",
#     baseline="middle",
#     dx=-5,
#     color="white"
# ).encode(
#     x=alt.X("Begin:Q"),
#     y=alt.Y("Range:T", sort="-x"),
#     text=alt.Text("Item:N")
# )

# st.altair_chart(chart + labels_2)
