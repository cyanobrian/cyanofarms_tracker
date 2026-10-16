import streamlit as st
from st_supabase_connection import SupabaseConnection
from datetime import datetime

st.title("Cyano Farms Data Entry")


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
            "Enter password to enable submission",
            type="password",
            on_change=password_entered,
            key="password",
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password incorrect, show input + error.
        st.text_input(
            "Enter password to enable submission",
            type="password",
            on_change=password_entered,
            key="password",
        )
        st.error("Incorrect Password")
        return False
    else:
        # Password correct.
        return True


crop_submit_button = True
harvest_submit_button = True

if check_password():
    crop_submit_button = False
    harvest_submit_button = False

def get_crop_data(): 
    '''
    Connect to database and get the name of crops and crop categories from the database. 
    
    Parameters: 
    None 

    Returns: 
    conn: connection object to the database
    crops_dict: dict, a dictionary of crop names and their corresponding crop IDs
    categories: list, a list of unique crop categories in alphabetical order
    '''
    # Initialize connection.
    conn = st.connection("supabase", type=SupabaseConnection)

    # Perform query to get all crops from database
    rows = conn.table("Crops").select("*").execute()
    crops_dict = {}
    for row in rows.data:
        crops_dict[row["crop_name"]] = row["crop_id"]
    crops_dict = dict(sorted(crops_dict.items()))


    # Get all unique crop categories in alphabetical order
    categories = set()
    for row in rows.data:
        categories.add(row["category"])
    categories = sorted(categories)

    return conn, crops_dict, categories

conn, crops_dict, categories = get_crop_data()

def save_harvest():
    """
    Check the weight is valid and crop is selected. If no errors, save the harvest data to the database. 
    This function is called when the user submits the harvest form.

    Parameters:
    None

    Returns:
    None
    """

    try:
        error_message = "Invalid weight"
        date, weight, crop, notes = (
            st.session_state.h_date,
            st.session_state.h_weight,
            st.session_state.h_crop,
            st.session_state.h_notes,
        )
        weight = float(weight)
        if weight <= 0:
            error_message = "Weight must be a positive number."
            raise ValueError()
        if crop is None or str.strip(crop) == "":
            error_message = "Crop cannot be empty."
            raise ValueError()
    except ValueError:
        st.error(error_message)

    else: 
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
    crop = st.selectbox(
        "Crop", crops_dict.keys(), index=None, placeholder="Select crop...", key="h_crop"
    )
    weight = st.text_input(
        "Weight (g)", placeholder="Enter weight...", required=True, key="h_weight"
    )

    notes = st.text_area(
        "Notes", placeholder="Enter any notes here...", height=100, key="h_notes"
    )

    st.form_submit_button("Submit", on_click=save_harvest, disabled= harvest_submit_button)



def save_crop():
    """
    Check the price is valid, category is selected, and name is not empty. If no errors, save the crop data to the database. 
    This function is called when the user submits the crop form.

    Parameters:
    None

    Returns:
    None
    """
    try:
        error_message = "Invalid price"
        price = float(st.session_state.c_price)
        name = st.session_state.c_name
        category = st.session_state.c_category

        if category is None or str.strip(category) == "":
            error_message = "Category cannot be empty."
            raise ValueError()
        if price <= 0:
            error_message = "Price must be a positive number."
            raise ValueError()
        if str.strip(name) == "": 
            error_message = "Crop name cannot be empty."
            raise ValueError()
    except ValueError:
        st.error(error_message)
    else: 
        conn.table("Crops").insert(
            {
                "crop_name": name,
                "price": price,
                "category": category,
            }
        ).execute()




# Form to enter new crop data into database
st.write("Add New Crop")
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
    st.form_submit_button("Submit", on_click=save_crop, disabled= crop_submit_button)

