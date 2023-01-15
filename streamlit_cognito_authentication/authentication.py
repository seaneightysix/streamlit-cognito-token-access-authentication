import streamlit as st
from .decode_verify_jwt import verify_jwt
import requests
import base64 from jose import jwk, jwt
import os import json

# Read constants from secrets file
COGNITO_USERPOOL_ID = st.secrets["COGNITO_USERPOOL_ID"]
COGNITO_DOMAIN = st.secrets["COGNITO_DOMAIN"]
COGNITO_GROUP_NAME = st.secrets["COGNITO_GROUP_NAME"]
APP_CLIENT_ID = st.secrets["APP_CLIENT_ID"]
HOST_APP_CLIENT_ID = st.secrets["HOST_APP_CLIENT_ID"]
CLIENT_SECRET_KEY = st.secrets["CLIENT_SECRET_KEY"]
CLIENT_SECRET = st.secrets["CLIENT_SECRET"]
IS_CLIENT_SECRET = st.secrets["IS_CLIENT_SECRET"]
APP_URI = st.secrets["APP_URI"]
REGION = st.secrets["REGION"]
HTTP_PROXY = st.secrets["HTTP_PROXY"]

class Authentication:
    """
    :param type: string: type of authentication: user or token

    """

    def __init__(self, type):

        if "authenticated" not in st.session_state:
            st.session_state.authenticated = None
        if "username" not in st.session_state:
            st.session_state.username = None
        if "auth_type" not in st.session_state:
            st.session_state.authenticated = type
        self.access_token = ""
        if type== "user":
            self.html_button_login = None
            self.html_button_logout = None
            self.login_link = None
            self.logout_link = None
            self.html_css_login = None
            self.initiate_user_buttons()

    def get_env_variables(self, access_token):
        """
        Gets env variables for token endpoint
        :param access_token: string: The access token to verify with cognito
        """

        env_vars = {
            "USERPOOL_ID": COGNITO_USERPOOL_ID,
            "HOST_APP_CLIENT_ID": HOST_APP_CLIENT_ID,
            "REGION": REGION,
            "HTTP_PROXY": HTTP_PROXY,
            "token": access_token
        }
        self.access_token = access_token
        return env_vars

    def cognito_authenticate(self, auth_code=None, access_token=None):
        """
        if auth_code, then makes a post request call to cognito login endpoint
        if access_token, then makes a get call to cognito token endpoint
        """

        url = ""
        headers = None
        body = None
        response = None

        if st.session_state.auth_type == "user" and auth_code != "":
            with st.spinner(text="Signining in..."):
                #Check how to set CLIENT_SECRET
                if IS_CLIENT_SECRET:
                    CLIENT_SECRET = st.secrets["CLIENT_SECRET"]
                else:
                    CLIENT_SECRET = json.loads(os.getenv("CLIENT_SECRET"))[f"{CLIENT_SECRET_KEY}"]
                url = f"{COGNITO_DOMAIN}/oauth2/token"
                client_secret_string = f"{APP_CLIENT_ID}:{CLIENT_SECRET}"
                client_secret_encoded = str(base64.b64encode(client_secret_string.encode("utf-8")), "utf-8")         
                headers = {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Authorization": f"Basic {client_secret_encoded}"
                }
                data = {
                    "grant_type": "authorization_code",
                    "client_id": APP_CLIENT_ID,
                    "code": auth_code,
                    "redirect_uri": APP_URI
                }

                # check if need proxies
                if HTTP_PROXY != "":
                    proxies = {
                        "http": HTTP_PROXY,
                        "https": HTTP_PROXY
                    }
                    response = requests.post(url, headers, data, proxies)
                    self.update_response(response)
                else:
                    response = requests.post(url, headers, data)
                    self.update_response(response)

        # use token endpoint
        else:
            if access_token is not None:
                with st.spinner(text="Signining in..."):
                    env_vars = self.get_env_variables(access_token)


    def get_auth_code(self):
        """
        Gets authorization code for cognito login endpoint

        """
        auth_query_params = st.experimental_get_query_params()
        try:
            auth_code = dict(auth_query_params)["code"][0]
        except(KeyError, TypeError):
            print(Exception)
            auth_code = ""
        return auth_code

    # button logic and UI
    def initiate_user_buttons(self):
        self.login_link = f"{COGNITO_DOMAIN}/login?client_id={APP_CLIENT_ID}&response_type=code&scope=email+openid&redirect_uri={APP_URI}"
        self.logout_link = f"{COGNITO_DOMAIN}/logout?client_id={APP_CLIENT_ID}&logout_uri={APP_URI}"

        self.html_css_login = """
        <style>
        .button-login {
            background-color: skyblue;
            color: white !important;
            padding: 1em 1.5em;
            text-decoration: none;
            text-transform: uppercase;
        }

        .button-login:hover {
            background-color: #555;
            text-decoration: none;
        }
        
        .button-login:active {
            background-color: black;
        }

        </style>
        """

        self.html_button_login  = (
            self.html_css_login
            + f"<a href='{self.login_link}' class='button-login' target='_self'>Login</a>"
        )
        self.html_button_logout  = (
            self.html_css_login
            + f"<a href='{self.logout_link}' class='button-login' target='_self'>Log Out</a>"
        )

    def button_login(self):
        return st.markdown(f"{self.html_button_login}", unsafe_allow_html=True)

    def button_logout(self):
        return st.markdown(f"{self.html_button_logout}", unsafe_allow_html=True)
