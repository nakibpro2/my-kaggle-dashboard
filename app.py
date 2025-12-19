import streamlit as st
import os
import subprocess
import json
from streamlit_option_menu import option_menu

# --- PAGE CONFIG ---
st.set_page_config(page_title="Kaggle Admin Pro", page_icon="🚀", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; background-color: #007bff; color: white; font-weight: bold; }
    .stCode { background-color: #1e1e1e !important; color: #dcdcdc !important; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- KAGGLE API SETUP (FIXED) ---
def setup_kaggle():
    # ১. ইউজারনেম ও কী চেক করা
    if "KAGGLE_USERNAME" not in st.secrets or "KAGGLE_KEY" not in st.secrets:
        st.error("❌ Secrets পাওয়া যায়নি! Streamlit Settings > Secrets-এ তথ্য যোগ করুন।")
        st.stop()

    user = st.secrets["KAGGLE_USERNAME"]
    key = st.secrets["KAGGLE_KEY"]

    # ২. এনভায়রনমেন্ট ভ্যারিয়েবল সেট করা (এটি সবচেয়ে বেশি কার্যকর)
    os.environ['KAGGLE_USERNAME'] = user
    os.environ['KAGGLE_KEY'] = key

    # ৩. kaggle.json ফাইল তৈরি করা (ফলব্যাক হিসেবে)
    kaggle_dir = os.path.expanduser('~/.kaggle')
    if not os.path.exists(kaggle_dir):
        os.makedirs(kaggle_dir)
    
    config_path = os.path.join(kaggle_dir, 'kaggle.json')
    with open(config_path, 'w') as f:
        json.dump({"username": user, "key": key}, f)
    
    os.chmod(config_path, 0o600)

# সেটআপ রান করা
setup_kaggle()

# --- SIDEBAR MENU ---
with st.sidebar:
    selected = option_menu(
        menu_title="Kaggle Control",
        options=["Dashboard", "Datasets", "Competitions", "Notebooks"],
        icons=["speedometer2", "database", "trophy", "code-slash"],
        menu_icon="robot",
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "#fafafa"},
            "nav-link-selected": {"background-color": "#007bff"},
        }
    )

# --- COMMAND RUNNER FUNCTION ---
def run_cmd(cmd):
    try:
        # সরাসরি এনভায়রনমেন্ট ভ্যারিয়েবল ব্যবহার করে কমান্ড রান করা
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Error: {result.stderr}"
    except Exception as e:
        return str(e)

# --- APP LOGIC ---
st.title(f"🚀 Kaggle {selected}")

if selected == "Dashboard":
    st.subheader("System Status")
    c1, c2 = st.columns(2)
    c1.success(f"Connected as: `{st.secrets['KAGGLE_USERNAME']}`")
    c2.info("Environment: Streamlit Cloud (Linux)")
    
    st.markdown("---")
    st.markdown("### 🛠 Custom Command")
    custom_cmd = st.text_input("যেকোনো Kaggle কমান্ড লিখুন", placeholder="kaggle datasets list")
    if st.button("Execute"):
        with st.spinner('Running...'):
            output = run_cmd(custom_cmd)
            st.code(output)

elif selected == "Datasets":
    query = st.text_input("Dataset খুঁজুন (উদা: titanic, covid19)", placeholder="Search datasets...")
    if st.button("Search Datasets"):
        res = run_cmd(f"kaggle datasets list -s {query}")
        st.code(res)

elif selected == "Competitions":
    if st.button("সব Active Competitions দেখুন"):
        res = run_cmd("kaggle competitions list")
        st.code(res)

elif selected == "Notebooks":
    st.subheader("Notebook Status")
    nb_slug = st.text_input("Notebook Slug দিন (user/notebook-name)", placeholder="ইন্টারনেট থেকে কপি করে দিন")
    if st.button("Check Status"):
        if nb_slug:
            res = run_cmd(f"kaggle kernels status {nb_slug}")
            st.text_area("Result", res, height=150)
        else:
            st.warning("দয়া করে একটি Slug দিন।")
