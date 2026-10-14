import streamlit as st
from st_supabase_connection import SupabaseConnection
from datetime import datetime

st.title("Cyano Farms Data Entry")

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

    st.form_submit_button("Submit", on_click=save_harvest)


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
    st.form_submit_button("Submit", on_click=save_crop)
