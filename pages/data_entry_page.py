import streamlit as st
from st_supabase_connection import SupabaseConnection

st.title("Cyano Farms Data Entry")

# Initialize connection.
conn = st.connection("supabase", type=SupabaseConnection)

# Perform query.
rows = conn.table("Crops").select("*").execute()
# Print results.


crops = set()
for row in rows.data:
    crops.add(row["crop_name"])
crops = sorted(crops)

st.write("Record Harvest")
with st.form(key="record_harvest", clear_on_submit=True, enter_to_submit=True):
    d = st.date_input("Harvest Date", format="MM/DD/YYYY", value="today")
    number = st.number_input(
        "Weight (g)", value=None, placeholder="0", min_value=0, required=True
    )

    option = st.selectbox(
        "Crop",
        crops,
        index=None,
        placeholder="Select crop...",
    )
    st.form_submit_button("Submit")


categories = set()
for row in rows.data:
    categories.add(row["category"])
categories = sorted(categories)

st.write("Add New Crop")
with st.form(key="add_crop", clear_on_submit=True, enter_to_submit=True):
    number = st.number_input(
        "Price ($/lb)", value=None, placeholder="0", min_value=0, required=True
    )
    new_crop_name = st.text_input("Crop Name", required=True)
    option = st.selectbox(
        "Category",
        categories,
        index=None,
        placeholder="Select category...",
    )
    st.form_submit_button("Submit")
