import streamlit as st
from .decode_verify_jwt import verify_jwt
import requests
from jose import jwk, jwt

# Read constants from secrets file
COGNITO_USERPOOL_ID = st.secrets["COGNITO_USERPOOL_ID"]
COGNITO_DOMAIN = st.secrets["COGNITO_DOMAIN"]
COGNITO_GROUP_NAME = st.secrets["COGNITO_GROUP_NAME"]
APP_CLIENT_ID = st.secrets["APP_CLIENT_ID"]
HOST_APP_CLIENT_ID = st.secrets["HOST_APP_CLIENT_ID"]
APP_URI = st.secrets["APP_URI"]
REGION = st.secrets["REGION"]
HTTP_PROXY = st.secrets["HTTP_PROXY"]

class AuthenticationToken:
    """
    :param type: string: type of authentication: user or token

    """

    def __init__(self):

        if "authenticated" not in st.session_state:
            st.session_state.authenticated = None
        if "logout" not in st.session_state:
            st.session_state.logout = False
        if "useremail" not in st.session_state:
            st.session_state.useremail = None
        self.access_token = ""

        if HTTP_PROXY != "":
            self.proxies = {
                "http": HTTP_PROXY,
                "https": HTTP_PROXY
            }
        else:
            self.proxies = ""

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

    def cognito_authenticate(self, access_token=None):
        """
         makes a get call to cognito token endpoint
        """

        url = ""
        headers = None
        response = None
 
        if access_token is not None:
            with st.spinner(text="Signining in..."):
                env_vars = self.get_env_variables(access_token)
                verify_results = verify_jwt(env_vars, proxies = self.proxies)
                if (verify_results is False):
                    print("Error in token signature verification")
                    st.session_state.authenticated = False
                    return

                # then check if user is in cognito group
                is_in_group = self.user_token_decode(access_token)
                if is_in_group is False:
                    print("User not in cognito user pool group")
                    st.session_state.authenticated = False
                    return

                # now call cognito api with token
                url = f"{COGNITO_DOMAIN}/oauth2/userInfo"
                headers = {
                    "Authorization": f"Bearer {access_token}"                  
                }
                # check if need proxies
                print(f"check if need proxies: {self.proxies} {HTTP_PROXY}")
                if HTTP_PROXY != "":                  
                    response = requests.post(url, headers=headers, proxies = self.proxies)
                    print(f'RESPONSE TOKEN {response.json()}')
                    self.update_response(response)
                else:
                    response = requests.post(url, headers=headers)
                    print(f'RESPONSE TOKEN {response.json()}')
                    self.update_response(response)
    
    def user_token_decode(self, token_response):
        is_in_group = False
        decoded_token = ""
        if token_response != "":
            decoded_token = jwt.decode(token_response, '', algorithms=['RS256'], audience=APP_CLIENT_ID, options={
                    "verify_signature": False,
                    "verify_iss": False,
                    "verify_sub": False,
                    "verify_at_hash": False
            })
            is_in_group = self.check_user_groups(decoded_token)
        return is_in_group

    def check_user_groups(self, decoded_token):
        cognito_pool_groups = decoded_token["cognito:groups"]
        print(f'cognito_pool_groups {cognito_pool_groups}')
        is_in_group = any(COGNITO_GROUP_NAME in gp for gp in cognito_pool_groups)
        print(f'is_in_group {is_in_group}')
        return is_in_group

    def update_response(self, token_response):
        if token_response.status_code == 200:
            st.session_state.authenticated = True
            st.session_state.logout = False
            st.session_state.useremail = token_response.json()["email"]
        else:
            st.session_state.authenticated = False
            st.session_state.logout = True
            

    def login_widget(self, form_name: str='Login'):
        login_form = st.form('Login', clear_on_submit=True)
        login_form.subheader(form_name)
        access_token = login_form.text_input("Access Token", value="", key="my_input")
        submitted = login_form.form_submit_button("Login")

        if access_token != "" and submitted:
            self.cognito_authenticate(access_token)

        return st.session_state.authenticated, st.session_state.useremail

    def logout(self, button_name='Logout'):
        if st.sidebar.button(button_name):
            st.session_state.authenticated = None
            st.session_state.useremail = None