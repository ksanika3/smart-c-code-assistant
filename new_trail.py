import os
import requests
import streamlit as st
from dotenv import load_dotenv
from database import Database

# Custom CSS for better styling
def load_css():
    st.markdown("""
        <style>
        /* Modern Dark Theme */
        .main-title {
            color: #ffffff;
            text-align: center;
            padding: 25px;
            border-radius: 15px;
            margin-bottom: 30px;
            background: linear-gradient(120deg, #2C3E50, #34495E);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }
        
        .chat-container {
            border-radius: 15px;
            padding: 25px;
            margin: 15px 0;
            background-color: #2C3E50;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }
        
        .sidebar-content {
            padding: 20px;
            background: #34495E;
            border-radius: 15px;
            margin: 10px 0;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }
        
        /* Custom Button Styles */
        .stButton > button {
            width: 100%;
            background: linear-gradient(120deg, #3498DB, #2980B9);
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 8px;
            font-weight: 500;
            margin: 5px 0;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            background: linear-gradient(120deg, #2980B9, #3498DB);
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }
        
        /* Chat Message Styling */
        .user-message {
            background: #34495E;
            padding: 15px;
            border-radius: 15px;
            margin: 10px 0;
            color: white;
        }
        
        .assistant-message {
            background: #2C3E50;
            padding: 15px;
            border-radius: 15px;
            margin: 10px 0;
            color: white;
        }
        
        /* Code Block Styling */
        pre {
            background: #1E272E !important;
            padding: 15px !important;
            border-radius: 10px !important;
            border: 1px solid #3498DB !important;
        }
        
        code {
            color: #3498DB !important;
        }
        
        /* Input Field Styling */
        .stTextInput > div > div > input {
            background-color: #34495E;
            color: white;
            border: 1px solid #3498DB;
            border-radius: 8px;
            padding: 10px 15px;
        }
        
        /* Form Submit Button */
        .stFormSubmitButton > button {
            background: linear-gradient(120deg, #3498DB, #2980B9) !important;
            color: white !important;
        }
        
        .stFormSubmitButton > button:hover {
            background: linear-gradient(120deg, #2980B9, #3498DB) !important;
        }
        
        /* Sidebar Styling */
        .sidebar .sidebar-content {
            background-color: #2C3E50;
        }
        
        /* Success/Error Message Styling */
        .success-message {
            background: #27AE60;
            color: white;
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
        }
        
        .error-message {
            background: #E67E22;
            color: white;
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
        }
        </style>
    """, unsafe_allow_html=True)

def init_session_state():
    """Initialize session state variables"""
    if "initialized" not in st.session_state:
        st.session_state.initialized = True
        st.session_state.user_id = None
        st.session_state.username = None
        st.session_state.messages = []
        st.session_state.examples = [
            "Write a program to sort an array using bubble sort",
            "Create a linked list implementation",
            "Program to check if a string is palindrome",
            "Write a program to find factorial of a number",
            "Create a program for matrix multiplication"
        ]
        st.session_state.db = None
        st.session_state.page = "login"  # Default page

def login_page():
    """Handle login functionality"""
    st.markdown('<h1 class="main-title">Login to C Programming Assistant</h1>', unsafe_allow_html=True)
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit and username and password:
            user_id = st.session_state.db.verify_user(username, password)
            if user_id:
                st.session_state.user_id = user_id
                st.session_state.username = username
                st.query_params["page"] = "chat"
                st.rerun()
            else:
                st.error("Invalid username or password")
    
    if st.button("Don't have an account? Sign Up"):
        st.query_params["page"] = "signup"
        st.rerun()

def chat_page():
    """Handle chat interface"""
    st.markdown(f'<h1 class="main-title">Welcome, {st.session_state.username}! </h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        
        # Profile section
        st.markdown("### 👤 User Profile")
        st.markdown(f"**Username:** {st.session_state.username}")
        
        # Example Queries section
        st.markdown("###  Example Queries")
        for example in st.session_state.examples:
            if st.button(example, key=f"example_{example}"):
                st.session_state.messages.append({"role": "user", "content": example})
                st.session_state.db.save_chat_message(st.session_state.user_id, "user", example)
                response = get_c_code(example)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.session_state.db.save_chat_message(st.session_state.user_id, "assistant", response)
                st.rerun()
        
        # Action buttons
        st.markdown("### Actions")
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.rerun()
        
        if st.button("Logout"):
            st.session_state.user_id = None
            st.session_state.username = None
            st.session_state.messages = []
            st.session_state.page = "login"
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Main chat container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message("user", avatar="👤"):
                st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
        elif message["role"] == "assistant":
            with st.chat_message("assistant", avatar="🤖"):
                st.code(message["content"], language='c')
                if st.button("Copy Code", key=f"copy_{hash(message['content'])}"):
                    st.write("Code copied to clipboard!")
    
    # Chat input
    if prompt := st.chat_input("What C program would you like to create?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.db.save_chat_message(st.session_state.user_id, "user", prompt)
        
        with st.spinner("🤖 Generating code..."):
            response = get_c_code(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.session_state.db.save_chat_message(st.session_state.user_id, "assistant", response)
        
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def get_c_code(prompt):
    """Generate C code using Gemini API"""
    try:
        # Load environment variables
        load_dotenv()
        
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            error_message = """
            ⚠️ API key not found! Please follow these steps:
            1. Go to https://makersuite.google.com/app/apikey
            2. Create a new API key
            3. Create a file named '.env' in your project folder
            4. Add this line to the .env file:
               GEMINI_API_KEY=your_actual_api_key_here
            5. Replace 'your_actual_api_key_here' with your real API key
            6. Restart the application
            """
            st.error(error_message)
            return "Error: API key not found. Please check the instructions above."

        with st.spinner("🔄 Generating code..."):
            url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
            
            payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": f"""Write a C program for the following task: {prompt}
                                Please provide clean, efficient, and well-commented C code.
                                Include proper error handling where necessary.
                                Return only the code without any explanation."""
                            }
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.7,
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": 2048
                }
            }
            
            headers = {
                'Content-Type': 'application/json',
                'x-goog-api-key': api_key
            }
            
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result and len(result['candidates']) > 0:
                    text = result['candidates'][0]['content']['parts'][0]['text']
                    code = text.strip()
                    if code.startswith('```c'):
                        code = code[3:]
                    if code.startswith('```'):
                        code = code[3:]
                    if code.endswith('```'):
                        code = code[:-3]
                    return code.strip()
                else:
                    return "Error: No code generated in the response"
            else:
                return f"Error: API request failed with status code {response.status_code}"
    except Exception as e:
        return f"Error generating code: {str(e)}"

def signup_page():
    """Handle signup functionality"""
    st.markdown('<h1 class="main-title">Sign Up - C Programming Assistant</h1>', unsafe_allow_html=True)
    
    with st.form("signup_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        submit = st.form_submit_button("Sign Up")
        
        if submit:
            if not username or not password:
                st.error("Please fill in all fields")
            elif password != confirm_password:
                st.error("Passwords do not match")
            else:
                if st.session_state.db.register_user(username, password):
                    st.success("Account created successfully! Please login.")
                    st.query_params["page"] = "login"
                    st.rerun()
                else:
                    st.error("Username already exists. Please choose another.")
    
    if st.button("Back to Login"):
        st.query_params["page"] = "login"
        st.rerun()

def main():
    # Set page config
    st.set_page_config(
        page_title="C Programming Assistant",
        page_icon="💻",
        layout="wide",
        initial_sidebar_state="collapsed"  # Hide sidebar by default
    )
    
    # Initialize session state first
    init_session_state()
    
    # Hide default menu and footer, and add top navigation styling
    st.markdown("""
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display:none;}
        
        /* Top Navigation Styling */
        div.nav-container {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 60px;
            background-color: #2C3E50;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 20px;
            padding: 0 20px;
            z-index: 999;
        }
        
        .nav-button {
            background-color: #3498DB;
            color: white;
            padding: 8px 16px;
            border-radius: 5px;
            text-decoration: none;
            border: none;
            cursor: pointer;
            font-weight: 500;
            transition: background-color 0.3s;
        }
        
        .nav-button:hover {
            background-color: #2980B9;
        }
        
        /* Add padding to main content to account for fixed nav */
        .main-content {
            margin-top: 80px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Top Navigation using Streamlit components instead of HTML
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        cols = st.columns(3)
        with cols[0]:
            if st.button("Login", key="nav_login"):
                st.query_params["page"] = "login"
                st.rerun()
        with cols[1]:
            if st.button("Sign Up", key="nav_signup"):
                st.query_params["page"] = "signup"
                st.rerun()
        with cols[2]:
            if st.button("Chat Box", key="nav_chat"):
                if st.session_state.user_id:
                    st.query_params["page"] = "chat"
                    st.rerun()
                else:
                    st.warning("Please login first")
    
    # Load CSS
    load_css()
    
    # Initialize database connection if not already initialized
    if st.session_state.db is None:
        try:
            st.session_state.db = Database()
        except Exception as e:
            st.error(f"Database Error: {str(e)}")
            return

    # Get current page from query params
    current_page = st.query_params.get("page", "login")
    
    # Route to appropriate page
    if current_page == "signup":
        signup_page()
    elif current_page == "chat" and st.session_state.user_id:
        chat_page()
    else:
        login_page()

if __name__ == "__main__":
    main()
