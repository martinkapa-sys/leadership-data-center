import streamlit as st

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Leadership Data Center",
    layout="wide"
)

# ---------- DARK THEME ----------
st.markdown("""
    <style>
    body {
        background-color: #0e1117;
        color: #e6edf3;
    }
    .stApp {
        background-color: #0e1117;
    }
    h1, h2, h3 {
        color: #58a6ff;
    }
    .stMetric {
        background-color: #161b22;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- STATE ----------
if "layers" not in st.session_state:
    st.session_state.layers = []

if "system_live" not in st.session_state:
    st.session_state.system_live = False

if "xla" not in st.session_state:
    st.session_state.xla = 90
    st.session_state.risk = 20

# ---------- TITLE ----------
st.title("🖥️ Martin Kapa – Leadership Data Center")
st.caption("Live system simulation: design, operation, and stabilization of complex organizations")

st.divider()

# ---------- PHASE 1: BUILD ----------
st.header("🏗️ System Architecture")

layers_info = {
    "⚡ Power": "Drives resilience, ownership, and long-term vision.",
    "🌐 Network": "Aligns stakeholders across countries and domains.",
    "🖥️ Compute": "Decision-making and portfolio prioritization.",
    "🔐 Security": "Governance, risk management, and compliance.",
    "📊 Monitoring": "XLA, KPIs, and continuous improvement."
}

cols = st.columns(5)

for i, (layer, desc) in enumerate(layers_info.items()):
    with cols[i]:
        if layer not in st.session_state.layers:
            if st.button(layer):
                st.session_state.layers.append(layer)
        else:
            st.success(f"{layer}\n\n{desc}")

# Show system activation
if len(st.session_state.layers) == len(layers_info):
    st.success("🟢 All systems active – Data Center is OPERATIONAL")
    st.session_state.system_live = True

st.divider()

# ---------- PHASE 2: LIVE SYSTEM ----------
if st.session_state.system_live:

    st.header("📊 System Performance")

    col1, col2, col3 = st.columns(3)

    col1.metric("User Experience (XLA)", f"{st.session_state.xla}%", delta="+2%")
    col2.metric("Delivery Speed", "High")
    col3.metric("Risk Level", f"{st.session_state.risk}%", delta="-5%")

    st.subheader("System Health")

    st.progress(st.session_state.xla / 100)
    st.progress(1 - st.session_state.risk / 100)

    st.divider()

    # ---------- INCIDENT ----------
    st.header("🚨 Incident Simulation")

    if st.button("⚠️ Trigger Critical Incident"):
        st.session_state.xla = 60
        st.session_state.risk = 70

        st.error("""
        🔴 CRITICAL ALERT  
        - Stakeholder misalignment detected  
        - Delivery pressure increasing  
        - Risk exposure rising  
        """)

    st.divider()

    # ---------- LEADERSHIP ----------
    st.header("🧠 Leadership Control Panel")

    col1, col2, col3 = st.columns(3)

    if col1.button("Align Stakeholders"):
        st.session_state.xla += 10
        st.session_state.risk -= 10
        st.info("Alignment improved across key stakeholders")

    if col2.button("Prioritize Execution"):
        st.session_state.xla += 10
        st.session_state.risk -= 10
        st.info("Focus restored on high-impact initiatives")

    if col3.button("Stabilize System"):
        st.session_state.xla = 92
        st.session_state.risk = 15
        st.success("✅ System stabilized. Performance restored.")

    st.divider()

    # ---------- FUTURE VISION ----------
    st.markdown("### 🚀 Next Evolution")
    st.write("AI-driven, self-healing workplace experience systems.")
