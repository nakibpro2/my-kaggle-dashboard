import streamlit as st
import os
import subprocess
from streamlit_option_menu import option_menu

# --- PAGE CONFIG ---
st.set_page_config(page_title="Kaggle Admin Pro", page_icon="🚀", layout="wide")

# --- CUSTOM CSS FOR BEAUTIFUL UI ---
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #20beff; color: white; border: none; }
    .stTextInput>div>div>input { border-radius: 5px; }
    .reportview-container .main .block-container { padding-top: 2rem; }
    </style>
    """, unsafe_allow_html=True)

# --- KAGGLE API SETUP ---
def setup_kaggle():
    kaggle_dir = os.path.expanduser('~/.kaggle')
    if not os.path.exists(kaggle_dir):
        os.makedirs(kaggle_dir)
    
    try:
        user = st.secrets["KAGGLE_USERNAME"]
        key = st.secrets["KAGGLE_KEY"]
        with open(os.path.join(kaggle_dir, 'kaggle.json'), 'w') as f:
            f.write(f'{{"username":"{user}","key":"{key}"}}')
        os.chmod(os.path.join(kaggle_dir, 'kaggle.json'), 0o600)
    except:
        st.error("Secrets-এ Kaggle API Key পাওয়া যায়নি!")

setup_kaggle()

# --- SIDEBAR MENU ---
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Dashboard", "Datasets", "Competitions", "Notebooks", "Settings"],
        icons=["house", "cloud-download", "trophy", "journal-code", "gear"],
        menu_icon="cast",
        default_index=0,
    )

# --- APP LOGIC ---
st.title(f"🚀 Kaggle {selected}")

def run_cmd(cmd):
    try:
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        return output.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return e.output.decode('utf-8')

if selected == "Dashboard":
    st.subheader("Account Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Status", "Connected", "Kaggle API")
    col2.metric("Environment", "Streamlit Cloud")
    col3.metric("Security", "Encrypted")
    
    st.info("আপনার সব কমান্ড এখান থেকে কন্ট্রোল করুন।")

elif selected == "Datasets":
    query = st.text_input("Dataset খুঁজুন", placeholder="e.g. titanic")
    if st.button("Search"):
        res = run_cmd(f"kaggle datasets list -s {query}")
        st.code(res)

elif selected == "Competitions":
    if st.button("Active Competitions দেখুন"):
        res = run_cmd("kaggle competitions list")
        st.code(res)

elif selected == "Notebooks":
    st.subheader("Run or Pull Notebooks")
    nb_name = st.text_input("Notebook Slug")
    if st.button("Check Notebook Status"):
        res = run_cmd(f"kaggle kernels status {nb_name}")
        st.success(res)

elif selected == "Settings":
    st.write("আপনার API সেটিংস নিরাপদ আছে।")
    if st.button("Clear Cache"):
        st.cache_data.clear()
        st.success("Cache cleared!")