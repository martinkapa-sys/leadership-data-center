import streamlit as st

st.set_page_config(page_title="Leadership Data Center", layout="wide")

# ---------- STATE ----------
if "layers" not in st.session_state:
    st.session_state.layers = []

if "system_live" not in st.session_state:
    st.session_state.system_live = False

if "xla" not in st.session_state:
    st.session_state.xla = 90
    st.session_state.risk = 20

# ---------- TITLE ----------
st.title("🖥️ Build & Operate My Leadership Data Center")
st.subheader("An interactive system showing how I design, run, and stabilize organizations")

st.divider()

# ---------- PHASE 1: BUILD ----------
st.header("🏗️ Phase 1: Build the System")

layers_info = {
    "⚡ Power": "What drives me: ownership, resilience, long-term thinking.",
    "🌐 Network": "How I align stakeholders across countries and domains.",
    "🖥️ Compute": "How I make decisions and prioritize at portfolio level.",
    "🔐 Security": "How I manage risk, governance, and compliance.",
    "📊 Monitoring": "How I measure success (XLA, KPIs, continuous improvement)."
}

cols = st.columns(len(layers_info))

for i, (layer, desc) in enumerate(layers_info.items()):
    if layer not in st.session_state.layers:
        if cols[i].button(layer):
            st.session_state.layers.append(layer)

# Show active layers
st.write("### Active Layers:")
st.write(st.session_state.layers)

# Show descriptions
for layer in st.session_state.layers:
    st.info(f"{layer}: {layers_info[layer]}")

# ---------- SYSTEM GO LIVE ----------
if len(st.session_state.layers) == len(layers_info):
    st.success("🟢 System is FULLY OPERATIONAL")
    st.session_state.system_live = True

st.divider()

# ---------- PHASE 2: LIVE SYSTEM ----------
if st.session_state.system_live:

    st.header("🟢 Phase 2: System Live")

    col1, col2 = st.columns(2)
    col1.metric("User Experience (XLA)", f"{st.session_state.xla}%")
    col2.metric("Risk Level", f"{st.session_state.risk}%")

    st.divider()

    # ---------- INCIDENT ----------
    st.header("🔴 Phase 3: Incident Simulation")

    if st.button("⚠️ Trigger Incident"):
        st.session_state.xla = 60
        st.session_state.risk = 70
        st.error("Incident detected: stakeholder misalignment & delivery pressure")

    st.divider()

    # ---------- LEADERSHIP ----------
    st.header("🧠 Phase 4: Leadership Actions")

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
        st.success("System stabilized successfully")
