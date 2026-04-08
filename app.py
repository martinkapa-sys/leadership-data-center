import streamlit as st

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Leadership Data Center",
    layout="wide"
)

# ---------- PREMIUM DARK UI ----------
st.markdown("""
<style>

/* Background */
.stApp {
    background: radial-gradient(circle at top, #0e1117, #05070d);
    color: #e6edf3;
    font-family: 'Segoe UI', sans-serif;
}

/* Titles */
h1 {
    color: #58a6ff;
    font-weight: 600;
}
h2, h3 {
    color: #79c0ff;
}

/* Glass cards */
.card {
    background: rgba(22, 27, 34, 0.7);
    padding: 20px;
    border-radius: 12px;
    border: 1px solid rgba(88, 166, 255, 0.2);
    backdrop-filter: blur(6px);
}

/* Status colors */
.green {color: #3fb950;}
.red {color: #f85149;}
.orange {color: #d29922;}

/* Buttons */
.stButton>button {
    border-radius: 8px;
    height: 45px;
    font-weight: 500;
    background-color: #161b22;
    color: white;
    border: 1px solid #30363d;
}
.stButton>button:hover {
    border: 1px solid #58a6ff;
    color: #58a6ff;
}

/* Metrics */
.metric-card {
    background: #161b22;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
    border: 1px solid #30363d;
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

if "incident" not in st.session_state:
    st.session_state.incident = False

# ---------- HEADER ----------
st.title("🖥️ Martin Kapa – Leadership Data Center")
st.caption("Real-time simulation of leadership, system design, and operational stability")

st.divider()

# ---------- SYSTEM STATUS ----------
status = "🟢 STABLE"
status_class = "green"

if st.session_state.incident:
    status = "🔴 INCIDENT"
    status_class = "red"
elif st.session_state.system_live:
    status = "🟡 ACTIVE"
    status_class = "orange"

st.markdown(f"<h3 class='{status_class}'>System Status: {status}</h3>", unsafe_allow_html=True)

st.divider()

# ---------- PHASE 1: BUILD ----------
st.header("🏗️ Architecture Layer Activation")

layers_info = {
    "⚡ Power": "Resilience, ownership, long-term thinking.",
    "🌐 Network": "Stakeholder alignment across regions.",
    "🖥️ Compute": "Decision-making and prioritization.",
    "🔐 Security": "Risk, governance, compliance.",
    "📊 Monitoring": "KPIs, XLA, continuous improvement."
}

cols = st.columns(5)

for i, (layer, desc) in enumerate(layers_info.items()):
    with cols[i]:
        if layer not in st.session_state.layers:
            if st.button(layer):
                st.session_state.layers.append(layer)
        else:
            st.markdown(f"""
            <div class="card">
            <b>{layer}</b><br><br>
            {desc}
            </div>
            """, unsafe_allow_html=True)

# Activate system
if len(st.session_state.layers) == len(layers_info):
    st.session_state.system_live = True
    st.success("All layers active – System operational")

st.divider()

# ---------- PHASE 2: PERFORMANCE ----------
if st.session_state.system_live:

    st.header("📊 System Performance Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
        <h3>XLA</h3>
        <h2>{st.session_state.xla}%</h2>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card">
        <h3>Delivery</h3>
        <h2>HIGH</h2>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
        <h3>Risk</h3>
        <h2>{st.session_state.risk}%</h2>
        </div>
        """, unsafe_allow_html=True)

    st.subheader("System Health")

    st.progress(st.session_state.xla / 100)
    st.progress(1 - st.session_state.risk / 100)

    st.divider()

    # ---------- INCIDENT ----------
    st.header("🚨 Incident Control")

    if st.button("⚠️ Trigger Critical Incident"):
        st.session_state.incident = True
        st.session_state.xla = 60
        st.session_state.risk = 70

        st.markdown("""
        <div class="card red">
        <b>CRITICAL ALERT</b><br><br>
        • Stakeholder misalignment<br>
        • Delivery pressure rising<br>
        • Risk exposure increasing
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # ---------- LEADERSHIP ----------
    st.header("🧠 Leadership Actions")

    col1, col2, col3 = st.columns(3)

    if col1.button("Align Stakeholders"):
        st.session_state.xla += 10
        st.session_state.risk -= 10

    if col2.button("Prioritize Execution"):
        st.session_state.xla += 10
        st.session_state.risk -= 10

    if col3.button("Stabilize System"):
        st.session_state.xla = 92
        st.session_state.risk = 15
        st.session_state.incident = False

        st.markdown("""
        <div class="card green">
        ✅ System stabilized<br><br>
        Performance restored. Risk under control.
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # ---------- FUTURE ----------
    st.markdown("### 🚀 Next Evolution")
    st.markdown("""
    <div class="card">
    AI-driven, self-healing workplace experience systems.<br><br>
    From reactive → predictive → autonomous.
    </div>
    """, unsafe_allow_html=True)
