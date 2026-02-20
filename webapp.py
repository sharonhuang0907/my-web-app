import streamlit as st
import pandas as pd
import requests
from requests.auth import HTTPBasicAuth

# --- CONFIGURABLE HOST LIST ---
HOST_OPTIONS = [
    "wd2-impl-services1.workday.com",
    "wd3-impl-services2.workday.com",
    "wd-production.workday.com"
]

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

def test_connection(tenant, user, password, host):
    """Attempts to connect to the Workday Tenant using Basic Auth."""
    # Constructing a common Workday endpoint URL
    # Note: You may need to adjust this URL path based on your specific API needs
    url = f"https://{host}/ccx/api/v1/{tenant}/userInfo"
    
    try:
        # We make a simple GET request to test the credentials
        response = requests.get(
            url, 
            auth=HTTPBasicAuth(user, password),
            timeout=10
        )
        
        # Check if the status code is successful (200-299)
        if response.status_code == 200:
            return True, "Successfully connected"
        elif response.status_code == 401:
            return False, "Failed: Unauthorized (Wrong Username/Password)"
        else:
            return False, f"Failed: Received status code {response.status_code}"
            
    except requests.exceptions.ConnectionError:
        return False, "Failed: Could not connect to the host. Check the URL."
    except Exception as e:
        return False, f"Failed: {str(e)}"

def login():
    _, col_mid, _ = st.columns([1, 2, 1])
    
    with col_mid:
        with st.container(border=True):
            st.markdown("### Connect to a Tenant")
            
            tenant = st.text_input("Tenant:", value="workdayproserv_dpt2")
            user_id = st.text_input("Userid:", value="wd-implementer")
            password = st.text_input("Password:", type="password")
            host = st.selectbox("Host:", options=HOST_OPTIONS)
            
            st.write("---")
            
            col_ok, col_cancel = st.columns([1, 1])
            with col_ok:
                if st.button("OK", use_container_width=True, type="primary"):
                    with st.spinner("Connecting..."):
                        success, message = test_connection(tenant, user_id, password, host)
                        
                        if success:
                            st.success(message)
                            st.session_state['logged_in'] = True
                            st.session_state['tenant'] = tenant
                            # Small delay so user sees the "Success" message
                            st.rerun()
                        else:
                            st.error(message)
            
            with col_cancel:
                if st.button("Cancel", use_container_width=True):
                    st.info("Connection cancelled.")

def main_app():
    st.title(f"Authenticated: {st.session_state['tenant']}")
    if st.button("Logout"):
        st.session_state['logged_in'] = False
        st.rerun()
    # Your table code goes here...

if not st.session_state['logged_in']:
    login()
else:
    main_app()
