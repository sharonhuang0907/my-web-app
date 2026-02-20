import streamlit as st
import pandas as pd

# --- Session State to handle "Login" status ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

def login():
    st.title("Secure Portal")
    user = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if user == "admin" and password == "password":
            st.session_state['logged_in'] = True
            st.rerun() # Refresh to show the table
        else:
            st.error("Invalid credentials")

def main_app():
    st.title("Data Entry Dashboard")
    
    # Initialize an empty table if it doesn't exist
    if 'data' not in st.session_state:
        st.session_state['data'] = pd.DataFrame(columns=["ID", "Name", "Value"])

    # --- Data Entry Form ---
    with st.form("entry_form"):
        col1, col2, col3 = st.columns(3)
        id_val = col1.text_input("ID")
        name_val = col2.text_input("Name")
        value_val = col3.text_input("Value")
        
        if st.form_submit_button("Add to Table"):
            new_row = pd.DataFrame([[id_val, name_val, value_val]], columns=["ID", "Name", "Value"])
            st.session_state['data'] = pd.concat([st.session_state['data'], new_row], ignore_index=True)
            st.success("Added!")

    # --- Display Table ---
    st.subheader("Current Data")
    st.table(st.session_state['data'])
    
    if st.button("Logout"):
        st.session_state['logged_in'] = False
        st.rerun()

# --- Logic to switch between Login and Main App ---
if not st.session_state['logged_in']:
    login()
else:
    main_app()
