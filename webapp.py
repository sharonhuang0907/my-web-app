import streamlit as st
import pandas as pd

# --- CONFIGURABLE HOST LIST ---
HOST_OPTIONS = [
    "wd2-impl-services1.workday.com",
    "wd3-impl-services2.workday.com",
    "wd-production.workday.com"
]

# Initialize session state for connection details if they don't exist
if 'tenant' not in st.session_state:
    st.session_state['tenant'] = "workdayproserv_dpt2"
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = "wd-implementer"
if 'host_idx' not in st.session_state:
    st.session_state['host_idx'] = 0
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

def login():
    # Centering the login box slightly
    _, col_mid, _ = st.columns([1, 2, 1])
    
    with col_mid:
        with st.container(border=True):
            st.markdown("### Connect to a Tenant")
            
            # These inputs now update the session_state automatically
            tenant = st.text_input("Tenant:", value=st.session_state['tenant'])
            user_id = st.text_input("Userid:", value=st.session_state['user_id'])
            password = st.text_input("Password:", type="password")
            
            # Host dropdown
            host = st.selectbox(
                "Host:", 
                options=HOST_OPTIONS, 
                index=st.session_state['host_idx']
            )
            
            st.write("---") # Visual separator
            
            col_ok, col_cancel = st.columns([1, 1])
            with col_ok:
                if st.button("OK", use_container_width=True, type="primary"):
                    # Save current entries to session state before logging in
                    st.session_state['tenant'] = tenant
                    st.session_state['user_id'] = user_id
                    st.session_state['host_idx'] = HOST_OPTIONS.index(host)
                    
                    # Validation
                    if user_id == "admin" and password == "password":
                        st.session_state['logged_in'] = True
                        st.rerun()
                    else:
                        st.error("Invalid credentials")
            
            with col_cancel:
                if st.button("Cancel", use_container_width=True):
                    st.warning("Connection cancelled.")

def main_app():
    st.title(f"Connected: {st.session_state['tenant']}")
    st.info(f"Logged in as: {st.session_state['user_id']} | Host: {HOST_OPTIONS[st.session_state['host_idx']]}")
    
    # --- Data Table Logic ---
    if 'data' not in st.session_state:
        st.session_state['data'] = pd.DataFrame(columns=["ID", "Name", "Value"])

    with st.form("entry_form"):
        c1, c2, c3 = st.columns(3)
        id_v = c1.text_input("ID")
        name_v = c2.text_input("Name")
        val_v = c3.text_input("Value")
        if st.form_submit_button("Add to Table"):
            new_row = pd.DataFrame([[id_v, name_v, val_v]], columns=["ID", "Name", "Value"])
            st.session_state['data'] = pd.concat([st.session_state['data'], new_row], ignore_index=True)
    
    st.dataframe(st.session_state['data'], use_container_width=True)
    
    if st.button("Logout"):
        st.session_state['logged_in'] = False
        st.rerun()

# Router
if not st.session_state['logged_in']:
    login()
else:
    main_app()
