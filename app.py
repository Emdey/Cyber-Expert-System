import streamlit as st
import time

# --- IMPORT YOUR TEAM'S MODULES ---
# This connects app.py to the empty files you created.
# If these files don't exist, this will crash. Ensure you created them!
from utils.nmap_scanner import run_network_scan
from modules.vuln_rules import check_vulnerabilities

# --- PAGE CONFIG ---
st.set_page_config(page_title="Cyber-Expert-System", page_icon="🛡️", layout="wide")

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/hacker.png", width=60)
    st.title("Project Sentinel")
    st.success("System: ONLINE 🟢")
    menu = st.radio("Navigation", ["Chat Terminal", "Manual Scanner", "Reports"])

# --- MAIN CHAT INTERFACE ---
if menu == "Chat Terminal":
    st.title("🛡️ Security Operations Chat")
    
    # 1. Initialize Chat History
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "System Online. Command me. (e.g., 'Scan 127.0.0.1')"}
        ]

    # 2. Display Old Messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 3. Handle User Input
    if prompt := st.chat_input("Enter command..."):
        # Show User Message
        st.chat_message("user").write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # --- THE BRIDGE LOGIC ---
        with st.chat_message("assistant"):
            if "scan" in prompt.lower():
                # Extract IP (Simplified logic: grab the last word)
                target_ip = prompt.split()[-1] 
                
                st.write(f"⚙️ **Running Modules...**")
                
                # A. CALL BACKEND (The Hands)
                # This calls the function inside utils/nmap_scanner.py
                scan_data = run_network_scan(target_ip)
                
                # B. CALL LOGIC (The Brain)
                # This calls the function inside modules/vuln_rules.py
                risks = check_vulnerabilities(scan_data)
                
                # C. REPORT BACK
                if not scan_data:
                    response = f"⚠️ Scan initiated on **{target_ip}**, but the Backend Module returned empty data.\n\n*(Reminder: The Backend Engineer needs to write the code in `utils/nmap_scanner.py`)*"
                else:
                    response = f"✅ **Scan Complete for {target_ip}**\n\n**Findings:**\n{risks}"
                
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            
            else:
                response = "I didn't understand. Try saying 'Scan [IP Address]'."
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

elif menu == "Manual Scanner":
    st.warning("⚠️ Switch to 'Chat Terminal' to talk to the bot.")

elif menu == "Reports":
    st.info("📄 Reports module coming in Phase 3.")