import streamlit as st
import time
import pandas as pd
import numpy as np
from streamlit_cognito_authentication import AuthenticationToken

st.set_page_config(page_title="Cognito and Streamlit Demo")

### START streamlit_cognito_authentication code ###
auth_placeholder = st.empty()
with auth_placeholder.container():

    cognito_authenticate = AuthenticationToken()
    if not st.session_state.authenticated:      
        authentication_status, username = cognito_authenticate.login_widget('Login')
        if authentication_status == False:
            st.error("Access token is not valid")
        elif authentication_status == None:
            st.warning("Please enter an access token")
if st.session_state.authenticated:
    auth_placeholder.empty()

    auth_sidebar_placeholder = st.empty()
    with auth_sidebar_placeholder.container():
        cognito_authenticate.logout("Logout")
    if st.session_state.logout:
        auth_sidebar_placeholder.empty()
### END streamlit_cognito_authentication code ###

    # ----- MAINPAGE OF YOUR APP GOES HERE -----
    # ----- REMEMBER TO KEEP YOUR APP CODE INDENTED AT THIS LEVEL -----

    st.title(":bar_chart: Demo app with cognito authentication")
    st.markdown("##")
    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()
    last_rows = np.random.randn(1, 1)
    chart = st.line_chart(last_rows)

    for i in range(1, 101):
        new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
        status_text.text("%i%% Complete" % i)
        chart.add_rows(new_rows)
        progress_bar.progress(i)
        last_rows = new_rows
        time.sleep(0.05)

    progress_bar.empty()

    # Streamlit widgets automatically run the script from top to bottom. Since
    # this button is not connected to any other logic, it just causes a plain
    # rerun.
    st.button("Re-run")