import streamlit as st
from database import Database
import time

# Custom CSS for better styling
def load_css():
    st.markdown("""
        <style>
        .main-title {
            color: #ffffff;
            text-align: center;
            padding: 25px;
            border-radius: 15px;
            margin-bottom: 30px;
            background: linear-gradient(120deg, #2C3E50, #34495E);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }
        .login-container {
            max-width: 500px;
            margin: 0 auto;
            padding: 30px;
            background-color: #2C3E50;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            color: white;
        }
        .stButton > button {
            width: 100%;
            background: linear-gradient(120deg, #E74C3C, #C0392B);
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 8px;
            font-weight: 500;
            margin: 20px 0;
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            background: linear-gradient(120deg, #C0392B, #E74C3C);
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }
        .signup-link {
            text-align: center;
            margin-top: 20px;
            padding: 15px;
            background: #34495E;
            border-radius: 8px;
            color: #3498DB;
        }
        .signup-link a {
            color: #E74C3C !important;
            text-decoration: none;
            font-weight: bold;
        }
        .signup-link a:hover {
            color: #C0392B !important;
            text-decoration: underline;
        }
        /* Input field styling */
        .stTextInput > div > div > input {
            background-color: #34495E;
            color: white;
            border: 1px solid #3498DB;
            border-radius: 8px;
            padding: 10px 15px;
        }
        .stTextInput > div > div > input:focus {
            border-color: #E74C3C;
            box-shadow: 0 0 0 1px #E74C3C;
        }
        /* Success/Error message styling */
        .stSuccess {
            background-color: #27AE60 !important;
            color: white !important;
            padding: 15px !important;
            border-radius: 8px !important;
        }
        .stError {
            background-color: #C0392B !important;
            color: white !important;
            padding: 15px !important;
            border-radius: 8px !important;
        }
        </style>
    """, unsafe_allow_html=True)

# Initialize database in session state if not already initialized
if 'db' not in st.session_state:
    try:
        st.session_state.db = Database()
    except Exception as e:
        st.error(f"Database Error: {str(e)}")
        st.session_state.db = None

# Initialize session state
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'username' not in st.session_state:
    st.session_state.username = None
if 'messages' not in st.session_state:
    st.session_state.messages = []

st.set_page_config(
    page_title="Login - C Programming Assistant",
    page_icon="🔐",
    layout="centered"
)

def switch_to_main():
    st.switch_page("new_trail.py")

def login_page():
    # Load custom CSS
    load_css()
    
    st.markdown('<h1 class="main-title">Welcome Back! </h1>', unsafe_allow_html=True)
    
    # If database is not working, show error
    if st.session_state.db is None:
        st.error("Database connection failed. Please check your configuration.")
        return
    
    # If already logged in, redirect to main page
    if st.session_state.user_id:
        switch_to_main()
        return
    
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    with st.form("login_form"):
        st.markdown("### Login to Your Account")
        username = st.text_input("👤 Username", placeholder="Enter your username")
        password = st.text_input("🔑 Password", type="password", placeholder="Enter your password")
        submit_button = st.form_submit_button("Login")
        
        if submit_button:
            if username and password:
                try:
                    with st.spinner("Authenticating..."):
                        user_id = st.session_state.db.verify_user(username, password)
                        if user_id:
                            st.session_state.user_id = user_id
                            st.session_state.username = username
                            st.success(" Login successful! Redirecting...")
                            time.sleep(1)
                            switch_to_main()
                        else:
                            st.error(" Invalid username or password")
                except Exception as e:
                    st.error(f" Login error: {str(e)}")
            else:
                st.warning(" Please enter both username and password")

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown('<div class="signup-link">', unsafe_allow_html=True)
    st.markdown("Don't have an account? [Sign Up](/Sign_Up) ✨")
    st.markdown("</div>", unsafe_allow_html=True)

login_page() 