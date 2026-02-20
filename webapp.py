import streamlit as st
import pandas as pd

# --- CONFIGURABLE HOST LIST ---
# You can add or remove addresses from this list
HOST_OPTIONS = [
    "wd2-impl-services1.workday.com",
    "wd3-impl-services2.workday.com",
    "wd-production.workday.com"
]

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

def login():
    # Use a container to mimic the "Connect to a Tenant" box
    with st.container(border=True):
        st.subheader("Connect to a Tenant")
        
        # Using columns to align labels and inputs like a classic Windows dialog
        tenant = st.text_input("Tenant:", value="workdayproserv_dpt2")
        user_id = st.text_input("Userid:", value="wd-implementer")
        password = st.text_input("Password:", type="password")
        host = st.selectbox("Host:", options=HOST_OPTIONS)
        
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("OK", use_container_width=True):
                # Simple validation logic
                if user_id == "admin" and password == "password":
                    st.session_state['logged_in'] = True
                    st.rerun()
                else:
                    st.error("Invalid credentials")
        with col2:
            if st.button("Cancel"):
                st.info("Connection cancelled.")

# ... rest of your main_app() code stays the same ...
