import streamlit as st 
from streamlit_gsheets import GSheetsConnection
import pandas as pd 
conn = st.connection("gsheets", type=GSheetsConnection)
data = conn.read( worksheet="Harvesting",
ttl="10m",
usecols=list(range(0,7)),
nrows=200
)
print(data)

