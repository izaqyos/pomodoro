"""
A simple Streamlit app to demonstrate the watch mode feature.
Run this with watch mode enabled to see changes instantly reflect in the browser.

Usage:
    streamlit run test_watch_mode.py --server.runOnSave=true

or using our provided scripts:
    ./run_pomodoro.sh -w test_watch_mode.py
    ./run_pomodoro.py -w test_watch_mode.py
    run_pomodoro.bat -w test_watch_mode.py
"""

import streamlit as st
import time
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Watch Mode Demo",
    page_icon="⏱️",
    layout="centered"
)

# Header
st.title("🔄 Watch Mode Demonstration")
st.markdown("This app demonstrates the automatic reload feature of watch mode.")

# Current time display
st.subheader("Current Server Time")
current_time = datetime.now().strftime("%H:%M:%S")
st.markdown(f"## {current_time}")
st.markdown("This time will update when you save changes to the code.")

# Counter that increases on code changes
if 'counter' not in st.session_state:
    st.session_state.counter = 0

st.subheader("Code Change Counter")
st.metric(label="Number of code changes", value=st.session_state.counter)
st.session_state.counter += 1

# Instructions
st.markdown("---")
st.subheader("How to test watch mode:")
st.markdown("""
1. Edit this file while the app is running
2. Save your changes
3. Watch the browser automatically reload with your changes

Try making these sample changes:
- Change the title color
- Add a new widget
- Modify the text in any of the markdown sections
""")

# Add a sample widget to modify
st.markdown("---")
st.subheader("Sample Widget to Modify")
st.slider("Test slider", min_value=0, max_value=100, value=50)

# Footer with timestamp
st.markdown("---")
st.caption(f"Last loaded: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.caption("To see immediate changes, make sure watch mode is enabled.") 