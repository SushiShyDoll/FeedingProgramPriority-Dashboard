import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import random

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Malnutrition & Stunting Geo-Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# GLOBAL CSS
# =========================
st.markdown("""
<style>
/* Import Poppins */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

:root {
  --background: #FDF9FB; 
  --foreground: #2D242D;
  --card: #FFFFFF;
  --primary: #D88AAE; 
  --accent: #B388FF;  
  --border: #F3E6EC;
  --radius: 14px;
}

/* FORCE LIGHT MODE COLORS */
.stApp { background-color: var(--background) !important; }
[data-testid="stSidebar"] { background-color: #FFF5F9 !important; border-right: 1px solid var(--border) !important; }
h1, h2, h3, h4, h5, h6, p, label, span { color: #1F2937 !important; }

/* ========================================================================= */
/* NUCLEAR FIX FOR "KEY" TEXT & SIDEBAR TOGGLE */
/* ========================================================================= */

/* 1. HIDE THE BUTTON ELEMENT ITSELF */
[data-testid="sidebar-button"] {
    display: none !important;
    width: 0 !important;
    height: 0 !important;
    opacity: 0 !important;
    pointer-events: none !important;
    position: absolute !important;
    top: -9999px !important;
    left: -9999px !important;
}

/* 2. HIDE THE HEADER CONTAINER THAT MIGHT HOLD THE TEXT */
[data-testid="stSidebarHeader"] {
    display: none !important;
    height: 0 !important;
}

/* 3. PUSH SIDEBAR CONTENT UP TO COVER ANY REMAINING GAP */
[data-testid="stSidebar"] > div:first-child {
    padding-top: 0px !important;
}

[data-testid="stSidebarNav"] {
    padding-top: 0px !important;
    margin-top: -20px !important; /* Adjust if needed to pull content up */
}

/* 4. HIDE COLLAPSE CONTROL ARROW */
[data-testid="collapsedControl"] {
    display: none !important;
}

/* 5. FONT FIX: PREVENT ICONS FROM TURNING INTO TEXT */
/* This rule says: apply Poppins to everything EXCEPT things that look like icons */
.stApp, div:not(.material-icons):not(.material-symbols-rounded), 
span:not(.material-icons):not(.material-symbols-rounded), 
p, label, h1, h2, h3, h4, h5, h6 { 
    font-family: 'Poppins', sans-serif !important; 
}

/* ========================================================================= */
/* RESPONSIVE LAYOUT LOGIC */
/* ========================================================================= */

/* DESKTOP (Width > 768px) */
@media (min-width: 768px) {
    [data-testid="stSidebar"] {
        min-width: 400px !important;
        max-width: 400px !important;
    }
}

/* MOBILE (Width <= 768px) */
/* We MUST re-enable the button on mobile, or users can't open/close the menu.
   But we will style it carefully to avoid the "key" text glitch. */
@media (max-width: 768px) {
    [data-testid="stSidebar"] {
        min-width: 100% !important;
        max-width: 100% !important;
    }

    /* Re-enable header on mobile so button can exist */
    [data-testid="stSidebarHeader"] {
        display: flex !important;
        height: auto !important;
    }

    [data-testid="sidebar-button"] {
        display: flex !important;
        position: fixed !important; /* Float it */
        top: 10px !important;
        left: 10px !important;
        width: 45px !important;
        height: 45px !important;
        z-index: 100000 !important;
        opacity: 1 !important;
        pointer-events: auto !important;
        background-color: white !important;
        border-radius: 8px !important;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1) !important;
        justify-content: center !important;
        align-items: center !important;
        
        /* HIDE INTERNAL TEXT (The "key..." glitch) */
        color: transparent !important;
        font-size: 0 !important;
    }

    /* Hide the SVG arrow */
    [data-testid="sidebar-button"] svg {
        display: none !important;
    }

    /* Force new icon */
    [data-testid="sidebar-button"]::before {
        content: "☰" !important;
        font-family: sans-serif !important; /* Safe font for symbol */
        font-size: 24px !important;
        color: var(--primary) !important;
        display: block !important;
        visibility: visible !important;
    }
}

/* ========================================================================= */
/* REST OF STYLING */
/* ========================================================================= */

/* Chat UI */
.chat-row { display: flex; width: 100%; margin-bottom: 15px; clear: both; }
.chat-row.assistant { justify-content: flex-start; }
.chat-row.assistant .chat-bubble { background-color: #F3F4F6; color: #1F2937 !important; border-bottom-left-radius: 2px; }
.chat-row.user { justify-content: flex-end; }
.chat-row.user .chat-bubble { background-color: var(--primary); color: white !important; border-bottom-right-radius: 2px; text-align: left; }
.chat-bubble { padding: 12px 18px; border-radius: 18px; max-width: 80%; font-size: 14px; box-shadow: 0px 2px 5px rgba(0,0,0,0.05); }
.chat-timestamp { font-size: 10px; opacity: 0.7; margin-top: 6px; display: block; color: inherit !important; }
.user .chat-timestamp { text-align: right; }

/* Sidebar Panels */
div[data-testid="stSidebarUserContent"] .stRadio > div { gap: 12px; }
div[data-testid="stSidebarUserContent"] label[data-baseweb="radio"] {
    background-color: white !important; padding: 22px !important; border-radius: 12px;
    border: 1px solid var(--border); transition: all 0.3s ease; width: 100%; margin-bottom: 8px;
    box-shadow: 0px 2px 5px rgba(216, 138, 174, 0.05);
}
div[data-testid="stSidebarUserContent"] label[data-baseweb="radio"]:hover { border-color: var(--primary); transform: translateX(8px); }

/* Cards */
.card { background-color: var(--card); border-radius: var(--radius); padding: 25px; box-shadow: 0px 6px 20px rgba(216, 138, 174, 0.1); border: 1px solid var(--border); margin-bottom: 20px; }
.kpi-title { font-size: 13px; color: #6B7280 !important; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px; }
.kpi-value { font-size: 30px; font-weight: 700; color: var(--foreground) !important; }

/* Sex Icon Cards */
.sex-icon-card { display: flex; align-items: center; padding: 20px; border-radius: 16px; background: white; border: 1px solid var(--border); box-shadow: 0px 4px 10px rgba(0,0,0,0.03); transition: all 0.3s ease; }
.sex-icon-card:hover { transform: translateY(-3px); box-shadow: 0px 10px 20px rgba(216, 138, 174, 0.12); }
.icon-circle { width: 55px; height: 55px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 26px; margin-right: 15px; }
.male-icon { background: linear-gradient(135deg, #FFE4F0 0%, #F3E6EC 100%); color: #D88AAE !important; border: 2px solid #F3E6EC; }
.female-icon { background: linear-gradient(135deg, #F3E8FF 0%, #EDE9FE 100%); color: #B388FF !important; border: 2px solid #EDE9FE; }
.icon-text-container { display: flex; flex-direction: column; }
.icon-label { font-size: 12px; font-weight: 600; color: #9CA3AF; text-transform: uppercase; }
.icon-value { font-size: 22px; font-weight: 700; color: #1F2937; }

/* Nutritionist Chansey Character */
.chansey-character { position: relative; width: 80px; height: 80px; margin: 0 auto 10px auto; }
.chansey-body { position: absolute; width: 60px; height: 65px; background: linear-gradient(135deg, #f4c2d8 0%, #e8a0c0 50%, #d88aae 100%); border-radius: 50% 50% 48% 48%; top: 8px; left: 10px; box-shadow: inset -8px -8px 15px rgba(200, 100, 150, 0.3); z-index: 1; }
.chansey-egg { position: absolute; width: 28px; height: 32px; background: linear-gradient(135deg, #fff9e6 0%, #f5f0dc 100%); border-radius: 50%; top: 32px; left: 26px; border: 2px solid #e8a0c0; z-index: 2; }
.chansey-arm-left { position: absolute; width: 18px; height: 32px; background: linear-gradient(135deg, #f4c2d8 0%, #e8a0c0 100%); border-radius: 40% 30% 50% 60%; top: 28px; left: 2px; transform: rotate(-25deg); }
.chansey-arm-right { position: absolute; width: 18px; height: 32px; background: linear-gradient(135deg, #f4c2d8 0%, #e8a0c0 100%); border-radius: 30% 40% 60% 50%; top: 28px; right: 2px; transform: rotate(25deg); }
.chansey-foot-left { position: absolute; width: 16px; height: 12px; background: linear-gradient(135deg, #d88aae 0%, #c97a9e 100%); border-radius: 50% 50% 40% 40%; bottom: 0; left: 18px; }
.chansey-foot-right { position: absolute; width: 16px; height: 12px; background: linear-gradient(135deg, #d88aae 0%, #c97a9e 100%); border-radius: 50% 50% 40% 40%; bottom: 0; right: 18px; }
.chansey-eye-left { position: absolute; width: 5px; height: 5px; background: #2c1810; border-radius: 50%; top: 22px; left: 22px; z-index: 3; }
.chansey-eye-right { position: absolute; width: 5px; height: 5px; background: #2c1810; border-radius: 50%; top: 22px; right: 22px; z-index: 3; }
.chansey-smile { position: absolute; width: 20px; height: 10px; border: 2px solid #2c1810; border-top: none; border-radius: 0 0 50% 50%; top: 30px; left: 30px; z-index: 3; }
.chansey-hat { position: absolute; width: 38px; height: 22px; background: white; border-radius: 50% 50% 0 0; top: -2px; left: 21px; border: 2px solid #f4c2d8; z-index: 4; }
.chansey-hat-cross { position: absolute; width: 10px; height: 12px; background: #4ade80; border-radius: 0 50% 50% 0; top: 50%; left: 50%; transform: translate(-50%, -50%) rotate(-30deg); }
.chansey-hair-left { position: absolute; width: 12px; height: 16px; background: linear-gradient(135deg, #f4c2d8 0%, #e8a0c0 100%); border-radius: 50% 20% 50% 50%; top: 6px; left: 18px; transform: rotate(-20deg); }
.chansey-hair-right { position: absolute; width: 12px; height: 16px; background: linear-gradient(135deg, #f4c2d8 0%, #e8a0c0 100%); border-radius: 20% 50% 50% 50%; top: 6px; right: 18px; transform: rotate(20deg); }
</style>
""", unsafe_allow_html=True)

# =========================
# DATA LOADING
# =========================
coords_data = {
    'NameHospital': ['Borders','Lothian','Fife','Lanarkshire','Ayrshire and Arran','Dumfries and Galloway','Forth Valley','Grampian','Greater Glasgow and Clyde','Highland','Orkney','Shetland','Tayside','Western Isles'],
    'lat': [55.56, 55.91, 56.23, 55.77, 55.46, 55.07, 56.12, 57.22, 55.86, 57.48, 58.98, 60.15, 56.60, 58.21],
    'lon': [-2.78, -3.21, -3.15, -3.93, -4.61, -3.61, -3.89, -2.48, -4.34, -4.22, -2.96, -1.15, -3.42, -6.39]
}
coords_df = pd.DataFrame(coords_data)

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("BMIData.csv")
    except:
        df = pd.DataFrame({'NameHospital': ['Borders', 'Lothian'], 'SchoolYear': [2023, 2023], 'Sex': ['Male', 'Female'], 'EpiUnderweight': [5, 10], 'EpiHealthyWeight': [80, 70], 'EpiOverweightAndObese': [15, 20], 'EpiOverweight': [10, 15], 'EpiObese': [5, 5], 'ValidCounts': [100, 100]})
    df['NameHospital'] = df['NameHospital'].str.strip()
    df = pd.merge(df, coords_df, on="NameHospital", how="inner")
    df["UnderweightRate"] = (df["EpiUnderweight"] / df["ValidCounts"]) * 100
    df["HealthyWeightRate"] = (df["EpiHealthyWeight"] / df["ValidCounts"]) * 100
    df["OverweightObeseRate"] = (df["EpiOverweightAndObese"] / df["ValidCounts"]) * 100
    return df

df = load_data()

# =========================
# SMART AI LOGIC
# =========================
def get_chansey_response(user_input, data):
    user_input = user_input.lower()
    latest_year = data["SchoolYear"].max()
    
    if "analysis" in user_input and "geographic" in user_input:
        current_data = data[data["SchoolYear"] == latest_year]
        top_prio = current_data.sort_values("UnderweightRate", ascending=False).iloc[0]
        avg_rate = current_data["UnderweightRate"].mean()
        return (f"Based on the **Geographic Priority Map** for {latest_year}: \n\n"
                f"📍 **{top_prio['NameHospital']}** is the highest priority cluster with an underweight rate of **{top_prio['UnderweightRate']:.2f}%**. \n"
                f"📈 The current average rate across Scotland is **{avg_rate:.2f}%**. Areas shaded darker on the map require immediate nutritional intervention.")

    if "all years" in user_input or "historical" in user_input:
        total_rec = data["ValidCounts"].sum()
        year_range = f"{data['SchoolYear'].min()} - {data['SchoolYear'].max()}"
        return f"Across the full historical scope ({year_range}), we have assessed **{total_rec:,}** total student records. The data suggests localized clusters of nutritional stress in the {latest_year} period."

    if any(word in user_input for word in ["priority", "highest", "worst", "underweight", "need"]):
        top_row = data[data["SchoolYear"] == latest_year].sort_values("UnderweightRate", ascending=False).iloc[0]
        return f"In {latest_year}, **{top_row['NameHospital']}** is the highest priority health board with a **{top_row['UnderweightRate']:.2f}%** underweight rate."
    
    if any(word in user_input for word in ["hello", "hi", "hey"]):
        return "Hello! I'm Nutritionist Chansey. I can provide a deep analysis of the Geographic Priority Map or Historical trends. What would you like to explore?"
    
    if any(word in user_input for word in ["dumb", "stupid", "potato"]):
        return "I'm a healthcare assistant AI, focused on nutrition! While I don't know much about potatoes, I can tell you which health boards have the highest nutritional needs."

    return "I can provide an in-depth analysis of the data! Try asking: 'Give an in-depth analysis of the geographic priority map'."

# =========================
# SIDEBAR NAVIGATION & AI
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I'm Nutritionist Chansey ✨ How can I help you analyze our student health data today?", "time": datetime.now().strftime("%I:%M %p")}]

if "last_page" not in st.session_state:
    st.session_state.last_page = "📍 Geographic Priority Map"

with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px; padding-top: 20px;">
        <div class="chansey-character">
            <div class="chansey-hair-left"></div><div class="chansey-hair-right"></div>
            <div class="chansey-hat"><div class="chansey-hat-cross"></div></div>
            <div class="chansey-body"><div class="chansey-eye-left"></div><div class="chansey-eye-right"></div><div class="chansey-smile"></div><div class="chansey-egg"></div></div>
            <div class="chansey-arm-left"></div><div class="chansey-arm-right"></div>
            <div class="chansey-foot-left"></div><div class="chansey-foot-right"></div>
        </div>
        <h3 style="color: #d88aae !important; margin-bottom: 0;">Nutritionist Chansey</h3>
        <p style="color: #888 !important; font-size: 14px;">Healthcare Assistant AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🧭 MENU")
    page = st.radio(label="Select a view", options=["📍 Geographic Priority Map", "📈 Historical Performance", "📊 Demographic Analysis", "🍕 Weight Category Distribution", "📄 Master Data Table"], label_visibility="collapsed")
    
    # FIX: PERSISTENCE - reset chat flag on page change so it doesn't pop up
    if page != st.session_state.last_page:
        st.session_state.chat_open = False
        st.session_state.last_page = page

    st.markdown("---")
    if st.button("💬 Chat with Nutritionist Chansey", use_container_width=True):
        st.session_state.chat_open = True

# --- DIALOG LOGIC ---
if st.session_state.get("chat_open"):
    @st.dialog("Nutritionist Chansey — Health Insights", width="large")
    def show_chat():
        st.markdown("""<div style="background: linear-gradient(to right, #F472B6, #D88AAE); padding: 25px; border-radius: 15px 15px 0 0; color: white !important;"><h2 style="margin:0; color:white !important; font-size:24px;">Nutritionist Chansey ✨</h2></div>""", unsafe_allow_html=True)
        chat_container = st.container(height=450)
        with chat_container:
            for m in st.session_state.messages:
                div_class = "user" if m["role"] == "user" else "assistant"
                st.markdown(f"""<div class="chat-row {div_class}"><div class="chat-bubble">{m["content"]}<span class="chat-timestamp">{m["time"]}</span></div></div>""", unsafe_allow_html=True)
        if prompt := st.chat_input("Type your message..."):
            st.session_state.messages.append({"role": "user", "content": prompt, "time": datetime.now().strftime("%I:%M %p")})
            response = get_chansey_response(prompt, df)
            st.session_state.messages.append({"role": "assistant", "content": response, "time": datetime.now().strftime("%I:%M %p")})
            st.rerun()
    show_chat()

# =========================
# DASHBOARD BODY
# =========================
st.markdown("""<div style="margin-bottom: 25px;"><h1>Malnutrition & Stunting Geo-Dashboard</h1><p style="color: #6B7280 !important; font-size: 16px;">Mapping BMI data of elementary students to identify feeding program priorities.</p></div>""", unsafe_allow_html=True)

if page == "📍 Geographic Priority Map":
    st.caption("Identify geographic nutritional clusters and filter by severity")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    mf1, mf2 = st.columns([1, 2])
    with mf1:
        years_options = ["All Years"] + sorted(df['SchoolYear'].unique().tolist(), reverse=True)
        map_year = st.selectbox("Select School Year", options=years_options)
    with mf2:
        severity_range = st.slider("Filter by Underweight Severity Rate (%)", float(df['UnderweightRate'].min()), float(df['UnderweightRate'].max()), (float(df['UnderweightRate'].min()), float(df['UnderweightRate'].max())))
    st.markdown('</div>', unsafe_allow_html=True)
    
    if map_year == "All Years":
        map_filtered_df = df.groupby(["NameHospital", "lat", "lon"]).agg({"ValidCounts": "sum", "UnderweightRate": "mean"}).reset_index()
        year_display = "2001 - 2023 (Avg)"
    else:
        map_filtered_df = df[df['SchoolYear'] == map_year]
        year_display = str(map_year)
    map_filtered_df = map_filtered_df[(map_filtered_df['UnderweightRate'] >= severity_range[0]) & (map_filtered_df['UnderweightRate'] <= severity_range[1])]

    k1, k2, k3, k4 = st.columns(4)
    with k1: st.markdown(f'<div class="card"><div class="kpi-title">TOTAL ASSESSED</div><div class="kpi-value">{int(map_filtered_df["ValidCounts"].sum()):,}</div></div>', unsafe_allow_html=True)
    with k2: st.markdown(f'<div class="card"><div class="kpi-title">AVG UNDERWEIGHT</div><div class="kpi-value">{map_filtered_df["UnderweightRate"].mean():.2f}%</div></div>', unsafe_allow_html=True)
    with k3: tp = map_filtered_df.sort_values("UnderweightRate", ascending=False).iloc[0]["NameHospital"] if not map_filtered_df.empty else "N/A"; st.markdown(f'<div class="card"><div class="kpi-title">PRIORITY TARGET</div><div class="kpi-value">{tp}</div></div>', unsafe_allow_html=True)
    with k4: st.markdown(f'<div class="card"><div class="kpi-title">VIEWMODE</div><div class="kpi-value" style="font-size:20px;">{year_display}</div></div>', unsafe_allow_html=True)

    col_map, col_dist = st.columns([2, 1])
    with col_map:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader(f"Geographic Severity Heatmap ({year_display})")
        fig_map = go.Figure(go.Scattermapbox(lat=map_filtered_df['lat'], lon=map_filtered_df['lon'], mode='markers+text', marker=go.scattermapbox.Marker(size=55, color=map_filtered_df['UnderweightRate'], colorscale=[[0, "#F3E6EC"], [0.5, "#D88AAE"], [1.0, "#9B4DCA"]], showscale=True, opacity=0.9), text=map_filtered_df['UnderweightRate'].apply(lambda x: f"{x:.1f}"), textfont=dict(size=12, color='white', family='Poppins', weight=700), hovertext=map_filtered_df['NameHospital']))
        fig_map.update_layout(mapbox=dict(style="carto-positron", center={"lat": 56.5, "lon": -4.0}, zoom=5.3), margin=dict(l=0, r=0, t=0, b=0), height=550, template="plotly_white")
        st.plotly_chart(fig_map, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col_dist:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Regional Ranking")
        fig_dist = px.bar(map_filtered_df.sort_values("UnderweightRate", ascending=True), y="NameHospital", x="UnderweightRate", orientation='h', color="UnderweightRate", color_continuous_scale=[[0, "#D88AAE"], [1.0, "#9B4DCA"]])
        fig_dist.update_layout(height=550, margin=dict(l=0, r=0, t=20, b=0), showlegend=False, coloraxis_showscale=False, template="plotly_white")
        st.plotly_chart(fig_dist, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "📈 Historical Performance":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    f1, f2, f3, f4 = st.columns([2, 1, 2, 2])
    with f1: loc_options = ["All Locations"] + sorted(df['NameHospital'].unique().tolist()); sel_boards = st.multiselect("Filter by Health Board", options=loc_options, default=["All Locations"])
    with f2: sel_sex = st.multiselect("Filter by Sex", options=sorted(df['Sex'].unique()), default=sorted(df['Sex'].unique()))
    with f3: cat_map = {"Underweight Rate (%)": "UnderweightRate", "Healthy Rate (%)": "HealthyWeightRate", "Overweight Rate (%)": "OverweightObeseRate"}; sel_cats = st.multiselect("Select Categories", options=list(cat_map.keys()), default=["Underweight Rate (%)"])
    with f4: year_range = st.slider("Year Range", int(df['SchoolYear'].min()), int(df['SchoolYear'].max()), (int(df['SchoolYear'].min()), int(df['SchoolYear'].max())))
    st.markdown('</div>', unsafe_allow_html=True)
    trend_data = df.copy()
    if sel_boards and "All Locations" not in sel_boards: trend_data = trend_data[trend_data['NameHospital'].isin(sel_boards)]
    trend_data = trend_data[trend_data['Sex'].isin(sel_sex)]
    trend_data = trend_data[(trend_data['SchoolYear'] >= year_range[0]) & (trend_data['SchoolYear'] <= year_range[1])]
    if not trend_data.empty:
        agg = trend_data.groupby("SchoolYear")[[cat_map[c] for c in sel_cats]].mean().reset_index()
        fig_trend = px.line(agg, x="SchoolYear", y=[cat_map[c] for c in sel_cats], markers=True, color_discrete_sequence=["#D88AAE", "#10B981", "#B388FF"])
        fig_trend.update_layout(height=550, hovermode="x unified", template="plotly_white"); st.plotly_chart(fig_trend, use_container_width=True)

elif page == "📊 Demographic Analysis":
    curr_df = df[df["SchoolYear"] == df["SchoolYear"].max()]; c1, c2 = st.columns([1, 1.5])
    with c1:
        st.markdown('<div class="card">', unsafe_allow_html=True); st.subheader("📍 Priority Ranking")
        prio_df = curr_df.groupby("NameHospital")["UnderweightRate"].mean().sort_values(ascending=False).reset_index()
        for i, row in prio_df.head(8).iterrows(): st.markdown(f"**{i+1}. {row['NameHospital']}** — `{row['UnderweightRate']:.2f}%` underweight")
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="card">', unsafe_allow_html=True); st.subheader("Underweight by Sex")
        sex_df = curr_df.groupby("Sex")["UnderweightRate"].mean().reset_index()
        m_rate = sex_df[sex_df['Sex'] == 'Male']['UnderweightRate'].values[0] if 'Male' in sex_df['Sex'].values else 0
        f_rate = sex_df[sex_df['Sex'] == 'Female']['UnderweightRate'].values[0] if 'Female' in sex_df['Sex'].values else 0
        k_male, k_female = st.columns(2)
        with k_male: st.markdown(f'<div class="sex-icon-card"><div class="icon-circle male-icon">♂️</div><div class="icon-text-container"><span class="icon-label">Male Average</span><span class="icon-value">{m_rate:.2f}%</span></div></div>', unsafe_allow_html=True)
        with k_female: st.markdown(f'<div class="sex-icon-card"><div class="icon-circle female-icon">♀️</div><div class="icon-text-container"><span class="icon-label">Female Average</span><span class="icon-value">{f_rate:.2f}%</span></div></div>', unsafe_allow_html=True)
        fig_sex = px.bar(sex_df, x="Sex", y="UnderweightRate", color="Sex", color_discrete_map={"Male": "#D88AAE", "Female": "#B388FF"})
        fig_sex.update_layout(showlegend=False, height=350, template="plotly_white"); st.plotly_chart(fig_sex, use_container_width=True); st.markdown('</div>', unsafe_allow_html=True)

# =========================
# RESTORED: WEIGHT CATEGORY DISTRIBUTION
# =========================
elif page == "🍕 Weight Category Distribution":
    st.caption("Detailed view of BMI status across population segments")
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    f1, f2, f3 = st.columns(3)
    
    with f1:
        year_opts = ["All Years"] + sorted(df['SchoolYear'].unique().tolist(), reverse=True)
        sel_year = st.selectbox("Select Year", year_opts)
    with f2:
        loc_opts = ["All Locations"] + sorted(df['NameHospital'].unique().tolist())
        sel_loc = st.selectbox("Select Location", loc_opts)
    with f3:
        sex_opts = ["Both Sex"] + sorted(df['Sex'].unique().tolist())
        sel_sex = st.selectbox("Select Sex", sex_opts)
    st.markdown('</div>', unsafe_allow_html=True)

    # Filter data logic
    filtered_df = df.copy()
    if sel_year != "All Years":
        filtered_df = filtered_df[filtered_df['SchoolYear'] == sel_year]
    if sel_loc != "All Locations":
        filtered_df = filtered_df[filtered_df['NameHospital'] == sel_loc]
    if sel_sex != "Both Sex":
        filtered_df = filtered_df[filtered_df['Sex'] == sel_sex]

    # Aggregate counts for the pie chart
    totals = {
        "Healthy": filtered_df['EpiHealthyWeight'].sum(),
        "Underweight": filtered_df['EpiUnderweight'].sum(),
        "Overweight": filtered_df['EpiOverweight'].sum(),
        "Obese": filtered_df['EpiObese'].sum()
    }
    pie_df = pd.DataFrame(totals.items(), columns=["Category", "Count"])

    # Visual Display
    st.markdown('<div class="card">', unsafe_allow_html=True)
    if pie_df["Count"].sum() > 0:
        fig_pie = px.pie(
            pie_df, 
            values="Count", 
            names="Category",
            hole=0.45,
            color="Category",
            color_discrete_map={
                "Healthy": "#10B981", 
                "Underweight": "#F59E0B", 
                "Overweight": "#D88AAE", 
                "Obese": "#B388FF"
            }
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        fig_pie.update_layout(
            height=500,
            margin=dict(t=20, b=20, l=0, r=0),
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5),
            template="plotly_white"
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.warning("No data found for the selected filters.")
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "📄 Master Data Table":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.dataframe(df[['SchoolYear', 'NameHospital', 'Sex', 'UnderweightRate', 'HealthyWeightRate', 'OverweightObeseRate', 'ValidCounts']].sort_values(['SchoolYear'], ascending=False), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)