import streamlit as st
import time

# --- IMPORT BACKEND FUNCTIONS ---
# These functions connect to the files you created in utils/ and modules/
# currently, they return "fake" data until your teammates write the real code.
from utils.nmap_scanner import run_network_scan
from modules.vuln_rules import check_vulnerabilities

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Cyber-Expert-System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/hacker.png", width=70)
    st.title("Project Sentinel")
    st.caption("v1.0.5 | System: ONLINE 🟢")
    st.markdown("---")
    
    # NAVIGATION MENU
    menu = st.radio(
        "Select Module:", 
        ["Dashboard", "AI Security Analyst", "Network Scanner", "Cloud Audit", "Web Inspector", "Reports"],
    )
    
    st.markdown("---")
    st.info("💡 **Tip:** Use the 'AI Analyst' for complex queries.")

# --- 1. DASHBOARD (The Executive View) ---
if menu == "Dashboard":
    st.title("🛡️ Command Center")
    st.markdown("### Real-Time Security Overview")
    
    # Executive Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Threat Level", "MODERATE", "Level 3")
    col2.metric("Active Scans", "0", "Idle")
    col3.metric("Vulns Detected", "12", "+2 today")
    col4.metric("System Health", "98%", "Stable")
    
    st.markdown("---")
    
    # Quick Status
    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("📡 Live Activity Log")
        st.code("10:00:01 - System Init... OK\n10:05:23 - Nmap Module Loaded... OK\n10:10:45 - User Admin logged in...", language="bash")
    with c2:
        st.subheader("⚠️ Top Risks")
        st.warning("• SSH Port 22 Open (Public)")
        st.warning("• S3 Bucket 'finance' Public")
        st.info("• Web Server Header Missing")

# --- 2. AI SECURITY ANALYST (The Smart Bridge) ---
elif menu == "AI Security Analyst":
    st.header("🤖 AI Security Assistant")
    st.markdown("Chat with the Expert System. Commands: `Scan [IP]`, `Check Cloud`, `Inspect Web`.")

    # Custom Icons
    USER_ICON = "🧑‍💻"
    BOT_ICON = "🤖"

    # Initialize Chat History
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "I am online. Ready for orders."}
        ]

    # Display History
    for message in st.session_state.messages:
        icon = USER_ICON if message["role"] == "user" else BOT_ICON
        with st.chat_message(message["role"], avatar=icon):
            st.markdown(message["content"])

    # Chat Input
    if prompt := st.chat_input("Enter command..."):
        # Show User Message
        st.chat_message("user", avatar=USER_ICON).write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # --- SMART LOGIC ---
        with st.chat_message("assistant", avatar=BOT_ICON):
            prompt_lower = prompt.lower()
            response = ""
            
            # A. CLOUD COMMANDS
            if "cloud" in prompt_lower or "aws" in prompt_lower:
                st.write("☁️ **Connecting to AWS Module...**")
                time.sleep(1) # Simulated delay
                response = "✅ **Cloud Audit Complete**\n\nFindings: [Waiting for Backend Engineer implementation]"
            
            # B. WEB COMMANDS
            elif "web" in prompt_lower or "http" in prompt_lower:
                st.write("🕸️ **Analyzing Web Headers...**")
                time.sleep(1)
                response = "✅ **Web Inspection Complete**\n\nFindings: [Waiting for Logic Engineer implementation]"

            # C. NETWORK COMMANDS
            elif "scan" in prompt_lower or "ip" in prompt_lower:
                target_ip = prompt.split()[-1] 
                st.write(f"📡 **Scanning Network Target: {target_ip}...**")
                
                # Call Real Backend
                scan_data = run_network_scan(target_ip)
                risks = check_vulnerabilities(scan_data)
                
                response = f"✅ **Network Scan Complete**\n\n**Findings:**\n{risks}"
            
            # D. UNKNOWN
            else:
                response = "❌ I didn't understand. Please specify 'Network Scan', 'Cloud Check', or 'Web Inspect'."

            # Show and Save Response
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# --- 3. NETWORK SCANNER (Fixed Layout) ---
elif menu == "Network Scanner":
    st.header("📡 Network Scanner")
    st.markdown("Manual tool for Port Scanning and Service Detection.")
    
    # Layout: Input on left, Button on right
    col1, col2 = st.columns([3, 1])
    
    with col1:
        target_ip = st.text_input("Target IP Address", "127.0.0.1")
        
    with col2:
        st.write("") # Spacer
        st.write("") # Spacer
        # THE TRIGGER BUTTON
        scan_triggered = st.button("🚀 Run Network Scan", type="primary")

    # RESULTS AREA (Only shows IF button is clicked)
    if scan_triggered:
        with st.spinner(f"Scanning {target_ip}..."):
            # 1. Call the Backend (Simulated for now)
            scan_data = run_network_scan(target_ip)
            
            # 2. Call the Logic (Simulated for now)
            risks = check_vulnerabilities(scan_data)
            
            st.success("Scan Complete")
            
            # Layout: Results split into two big columns
            res_col1, res_col2 = st.columns(2)
            
            with res_col1:
                st.subheader("🔍 Scan Results")
                st.json(scan_data)
            
            with res_col2:
                st.subheader("🧠 Expert Findings")
                if not risks:
                    st.info("No vulnerabilities detected.")
                else:
                    for r in risks:
                        st.error(r)

# --- 4. CLOUD AUDIT (Manual Button) ---
elif menu == "Cloud Audit":
    st.header("☁️ Cloud Infrastructure Audit")
    st.markdown("Check AWS S3 Buckets for public access risks.")
    
    aws_profile = st.selectbox("Select AWS Profile", ["default", "prod-env", "dev-env"])
    
    if st.button("Run Cloud Check"):
        st.info(f"Using Profile: {aws_profile}")
        # Placeholder for real connection
        st.warning("⚠️ **Backend Note:** Connect `utils.cloud_scanner.py` here.")

# --- 5. WEB INSPECTOR (Manual Button) ---
elif menu == "Web Inspector":
    st.header("🕸️ Web Inspector")
    st.markdown("Scan websites for SQL Injection and missing headers.")
    
    url = st.text_input("Target URL", "https://example.com")
    
    if st.button("Analyze Headers"):
        # Placeholder for real connection
        st.warning("⚠️ **Logic Note:** Connect `modules.web_rules.py` here.")

# --- 6. REPORTS ---
elif menu == "Reports":
    st.header("📑 Intelligence Reports")
    st.markdown("Download comprehensive security summaries.")
    
    report_text = f"SECURITY REPORT\nDate: {time.strftime('%Y-%m-%d')}\nStatus: VULNERABLE\n\n1. Network: Port 22 Open\n2. Cloud: 1 Public Bucket"
    
    st.text_area("Report Preview", report_text, height=200)
    st.download_button("📥 Download Report (PDF)", data=report_text, file_name="report.txt")