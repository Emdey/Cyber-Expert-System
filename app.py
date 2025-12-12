import streamlit as st
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import time

# --- IMPORT BACKEND FUNCTIONS ---
from utils.nmap_scanner import run_network_scan
from modules.vuln_rules import check_vulnerabilities

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Cyber-Expert-System", page_icon="🛡️", layout="wide")

# --- CUSTOM THEME FUNCTION (Midnight Edition) ---
def load_glass_theme():
    """
    Injects CSS to create a Dark Glass + Midnight Blue look.
    """
    st.markdown("""
    <style>
        /* 1. Main Background - Midnight Blue to Deep Navy (NO LIGHT BLUE) */
        .stApp {
            background: linear-gradient(180deg, #020024 0%, #0a0a2e 50%, #000000 100%);
            background-attachment: fixed;
            color: #ffffff;
        }

        /* 2. Sidebar - Dark Frosted Glass */
        [data-testid="stSidebar"] {
            background-color: rgba(5, 5, 20, 0.6); 
            backdrop-filter: blur(15px);
            border-right: 1px solid rgba(255, 255, 255, 0.08);
        }

        /* 3. The "Real Glass" Card Effect */
        [data-testid="stMetric"], 
        div[data-testid="stVerticalBlock"] > div > div {
            background: rgba(255, 255, 255, 0.03); /* Extremely subtle fill */
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5); /* Deep shadow */
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.1); /* Subtle white edge */
            padding: 15px;
        }

        /* 4. Inputs - Deep Dark */
        .stTextInput > div > div > input {
            background-color: rgba(0, 0, 0, 0.6) !important;
            color: #00d4ff !important;
            border: 1px solid #334455 !important;
            border-radius: 6px;
        }
        .stTextInput > div > div > input:focus {
            border: 1px solid #00d4ff !important;
            box-shadow: 0 0 10px rgba(0, 212, 255, 0.3);
        }

        /* 5. Buttons - Stealth Neon */
        .stButton > button {
            background: rgba(0, 212, 255, 0.05);
            border: 1px solid #00d4ff;
            color: #00d4ff;
            font-family: 'Courier New', monospace;
            font-weight: bold;
            border-radius: 4px;
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            background: #00d4ff;
            color: #000000;
            box-shadow: 0 0 15px rgba(0, 212, 255, 0.6);
        }

        /* 6. Text Styling */
        h1, h2, h3 {
            color: #ffffff !important;
            font-family: 'Helvetica Neue', sans-serif;
            letter-spacing: 1px;
        }
        p, .stMarkdown, .stCaption {
            color: #b0c4de !important; /* Steel Blue text */
        }
        
        /* 7. Chat Box */
        .stChatInputContainer {
            background-color: transparent !important;
        }
    </style>
    """, unsafe_allow_html=True)

# --- 1. LOAD USER DATABASE ---
try:
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)
except FileNotFoundError:
    st.error("⚠️ Config file not found. Please create 'config.yaml'.")
    st.stop()

# --- 2. SETUP AUTHENTICATOR ---
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# --- 3. AUTHENTICATION LOGIC ---
if st.session_state.get("authentication_status"):
    authenticator.login(location='unrendered')
else:
    # User is NOT logged in -> Show Tabs
    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        authenticator.login(location='main')

    with tab2:
        try:
            email, username, name = authenticator.register_user(location='main')
            if email:
                st.success('User registered successfully! Please go to Login tab.')
                with open('config.yaml', 'w') as file:
                    yaml.dump(config, file, default_flow_style=False)
        except Exception as e:
            st.error(f"Error: {e}")

# --- 4. MAIN APP LOGIC (Only runs if Logged In) ---
if st.session_state.get("authentication_status") is False:
    pass
elif st.session_state.get("authentication_status") is None:
    pass

elif st.session_state.get("authentication_status") is True:
    
    # --- ACTIVATE THE MIDNIGHT THEME ---
    load_glass_theme()

    # =========================================================
    #  LOGGED IN AREA
    # =========================================================
    
    # Get user details
    username = st.session_state["username"]
    name = st.session_state["name"]
    
    # --- SIDEBAR ---
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/hacker.png", width=70)
        st.title("Project Sentinel")
        
        st.caption(f"Operator: {username}") 
        
        authenticator.logout(location='sidebar')
        st.markdown("---")
        
        menu = st.radio(
            "Select Module:", 
            ["Dashboard", "AI Security Analyst", "Network Scanner", "Cloud Audit", "Web Inspector", "Reports"],
        )
        st.markdown("---")
        st.info("💡 **Tip:** Use 'AI Analyst' for complex queries.")

    # --- A. DASHBOARD ---
    if menu == "Dashboard":
        st.title("🛡️ Command Center")
        st.markdown(f"### Welcome back, **{username}**")
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Threat Level", "MODERATE", "Level 3")
        col2.metric("Account Status", "Active", "Verified")
        col3.metric("Scans Performed", "0", "New Account")
        col4.metric("System Health", "98%", "Stable")
        
        st.info("System Ready. Select a tool from the sidebar.")

    # --- B. AI SECURITY ANALYST ---
    elif menu == "AI Security Analyst":
        st.header("🤖 AI Security Assistant")
        st.markdown("Chat with the Expert System. Commands: `Scan [IP]`, `Check Cloud`, `Inspect Web`.")

        USER_ICON = "🧑‍💻"
        BOT_ICON = "🤖"

        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "assistant", "content": f"Hello {username}. I am online. Ready for orders."}
            ]

        for message in st.session_state.messages:
            icon = USER_ICON if message["role"] == "user" else BOT_ICON
            with st.chat_message(message["role"], avatar=icon):
                st.markdown(message["content"])

        if prompt := st.chat_input("Enter command..."):
            st.chat_message("user", avatar=USER_ICON).write(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            with st.chat_message("assistant", avatar=BOT_ICON):
                prompt_lower = prompt.lower()
                response = ""
                
                if "cloud" in prompt_lower or "aws" in prompt_lower:
                    st.write("☁️ **Connecting to AWS Module...**")
                    time.sleep(1) 
                    response = "✅ **Cloud Audit Complete**\n\nFindings: [Waiting for Backend Engineer implementation]"
                
                elif "web" in prompt_lower or "http" in prompt_lower:
                    st.write("🕸️ **Analyzing Web Headers...**")
                    time.sleep(1)
                    response = "✅ **Web Inspection Complete**\n\nFindings: [Waiting for Logic Engineer implementation]"

                elif "scan" in prompt_lower or "ip" in prompt_lower:
                    target_ip = prompt.split()[-1] 
                    st.write(f"📡 **Scanning Network Target: {target_ip}...**")
                    scan_data = run_network_scan(target_ip)
                    risks = check_vulnerabilities(scan_data)
                    response = f"✅ **Network Scan Complete**\n\n**Findings:**\n{risks}"
                
                else:
                    response = "❌ I didn't understand. Please specify 'Network Scan', 'Cloud Check', or 'Web Inspect'."

                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

    # --- C. NETWORK SCANNER ---
    elif menu == "Network Scanner":
        st.header("📡 Network Scanner")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            target_ip = st.text_input("Target IP Address", "127.0.0.1")
        with col2:
            st.write("")
            st.write("")
            scan_triggered = st.button("🚀 Run Network Scan", type="primary")

        if scan_triggered:
            with st.spinner(f"Scanning {target_ip}..."):
                scan_data = run_network_scan(target_ip)
                risks = check_vulnerabilities(scan_data)
                
                st.success("Scan Complete")
                res_col1, res_col2 = st.columns(2)
                with res_col1:
                    st.subheader("🔍 Scan Results")
                    st.json(scan_data)
                with res_col2:
                    st.subheader("🧠 Expert Findings")
                    for r in risks:
                        st.error(r)

    # --- D. CLOUD AUDIT ---
    elif menu == "Cloud Audit":
        st.header("☁️ Cloud Infrastructure Audit")
        st.warning("⚠️ **Backend Note:** Connect `utils/cloud_scanner.py` here.")

    # --- E. WEB INSPECTOR ---
    elif menu == "Web Inspector":
        st.header("🕸️ Web Inspector")
        st.warning("⚠️ **Logic Note:** Connect `modules/web_rules.py` here.")

    # --- F. REPORTS ---
    elif menu == "Reports":
        st.header("📑 Intelligence Reports")
        report_text = f"USER: {username}\nDATE: {time.strftime('%Y-%m-%d')}\nSTATUS: Verified"
        st.download_button("📥 Download Report (PDF)", data=report_text, file_name="report.txt")