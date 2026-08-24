import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

print(pd.Timestamp.now('US/Eastern').normalize())
print(pd.offsets.Week(weekday=5).rollback(pd.Timestamp.now('US/Eastern').normalize()))
# df = pd.DataFrame({
#     'Position': range(1, 10001),  # Example range, adjust according to your data
#     'Value': np.random.randn(10000)  # Random data for demonstration
# })

# fig = px.line(df, x='Position', y='Value')

# fig.update_layout(
#     xaxis=dict(
#         rangeslider=dict(
#             visible=True
#         ),
#         type="linear"
#     )
# )

# st.plotly_chart(fig, use_container_width=True)
