import streamlit as st
import math

# --- CONFIG ---
st.set_page_config(page_title="Solar Guru", page_icon="☀️", layout="centered")

# --- LANGUAGE DICT ---
LANG = {
    "English": {
        "welcome": "Welcome to Solar Guru ☀️",
        "subtitle": "Check if Solar is worth for YOUR area",
        "lang_select": "Select Language",
        "login": "Login",
        "username": "Username",
        "password": "Password",
        "terms": "I agree to Terms & Conditions",
        "next": "Next",
        "how_to": "How to Use This App",
        "s1": "1. Enter your Location",
        "s2": "2. Enter Roof Area & Per Unit Cost",
        "s3": "3. Get Full Financial & Production Report",
        "input_title": "Enter Your Details",
        "location": "Location (e.g., Chennai)",
        "roof_area": "Roof Area (sq.ft)",
        "unit_cost": "Electricity Cost per Unit (Rs.)",
        "calculate": "Calculate Report",
        "output_title": "Your Solar Report",
        "panels_needed": "Panels Required",
        "system_size": "System Size",
        "daily_prod": "Daily Production",
        "yearly_prod": "Yearly Production",
        "setup_cost": "Total Setup Cost",
        "yearly_profit": "Yearly Savings / Profit",
        "monthly_profit": "Monthly Savings",
        "payback": "Payback Period",
        "thankyou": "Thank You! Go Solar, Save Future! 🌱"
    },
    "Tamil": {
        "welcome": "Solar Guru Ku Varaverkirom ☀️",
        "subtitle": "Unga Area ku Solar Worth Ah nu Paarppom",
        "lang_select": "Mozhi Therndedukkavum",
        "login": "Login",
        "username": "Payar",
        "password": "Password",
        "terms": "Terms & Conditions ku Sammathikiren",
        "next": "Aduthathu",
        "how_to": "App Eppadi Use Pannanum",
        "s1": "1. Location Enter Pannunga",
        "s2": "2. Roof Area & Per Unit Rate Enter Pannunga",
        "s3": "3. Full Financial Report Vaangunga",
        "input_title": "Vivarangalai Enter Pannunga",
        "location": "Location (e.g., Chennai)",
        "roof_area": "Mottai Maadi Area (sq.ft)",
        "unit_cost": "1 Unit Min Kattanam (Rs.)",
        "calculate": "Report Paar",
        "output_title": "Unga Solar Report",
        "panels_needed": "Thevaiyana Panels",
        "system_size": "System Size",
        "daily_prod": "Daily Production",
        "yearly_prod": "Yearly Production",
        "setup_cost": "Total Setup Cost",
        "yearly_profit": "Varuda Labam / Savings",
        "monthly_profit": "Maatha Labam",
        "payback": "Investment Thirumba Vara Aagum Kaalam",
        "thankyou": "Nandri! Solar ku Maaringa! 🌱"
    }
}

# --- STATE ---
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'
if 'lang' not in st.session_state:
    st.session_state.lang = 'English'

def t(key):
    return LANG[st.session_state.lang][key]

# --- 1. WELCOME SCREEN ---
if st.session_state.page == 'welcome':
    st.title(t("welcome"))
    st.subheader(t("subtitle"))
    st.session_state.lang = st.selectbox(t("lang_select"), ["English", "Tamil"])
    
    with st.form("login_form"):
        st.text_input(t("username"))
        st.text_input(t("password"), type="password")
        terms = st.checkbox(t("terms"))
        submitted = st.form_submit_button(t("login"))
        if submitted:
            if not terms:
                st.error("Please Accept Terms!")
            else:
                st.session_state.page = 'slides'
                st.rerun()

# --- 2. HOW TO USE SLIDES ---
elif st.session_state.page == 'slides':
    st.header(t("how_to"))
    st.info(f"☀️ {t('s1')}\n\n🏠 {t('s2')}\n\n📊 {t('s3')}")
    st.image("https://images.unsplash.com/photo-1509391366360-2e959784a276", caption="Solar Power")
    if st.button(t("next")):
        st.session_state.page = 'input'
        st.rerun()

# --- 3. INPUT SCREEN ---
elif st.session_state.page == 'input':
    st.header(t("input_title"))
    location = st.text_input(t("location"), "Chennai")
    roof_area = st.number_input(t("roof_area"), min_value=100, value=500)
    unit_cost = st.number_input(t("unit_cost"), min_value=1.0, value=8.0)

    if st.button(t("calculate")):
        st.session_state.location = location
        st.session_state.roof_area = roof_area
        st.session_state.unit_cost = unit_cost
        st.session_state.page = 'output'
        st.rerun()

# --- 4. OUTPUT / REPORT ---
elif st.session_state.page == 'output':
    st.header(t("output_title"))
    st.write(f"📍 Location: **{st.session_state.location}**")

    # ---- CORE CALCULATION ----
    PANEL_AREA = 20 # sq ft per panel
    PANEL_WATT = 0.4 # 400W = 0.4kW
    SUN_HOURS = 5.2
    EFFICIENCY = 0.80 # 20% loss
    COST_PER_KW = 60000 # Rs 60k per kW

    usable_area = st.session_state.roof_area * 0.8 # 80% usable
    num_panels = math.floor(usable_area / PANEL_AREA)
    system_kw = num_panels * PANEL_WATT
    daily_kwh = system_kw * SUN_HOURS * EFFICIENCY
    yearly_kwh = daily_kwh * 365
    setup_cost = system_kw * COST_PER_KW
    yearly_savings = yearly_kwh * st.session_state.unit_cost
    monthly_savings = yearly_savings / 12
    payback = setup_cost / yearly_savings if yearly_savings > 0 else 0

    col1, col2 = st.columns(2)
    col1.metric(t("panels_needed"), f"{num_panels} Panels")
    col2.metric(t("system_size"), f"{system_kw:.2f} kW")
    
    st.metric(t("daily_prod"), f"{daily_kwh:.2f} kWh / Units")
    st.metric(t("yearly_prod"), f"{yearly_kwh:.0f} kWh / Units")
    st.metric(t("setup_cost"), f"Rs. {setup_cost:,.0f}")
    st.metric(t("yearly_profit"), f"Rs. {yearly_savings:,.0f}")
    st.metric(t("monthly_profit"), f"Rs. {monthly_savings:,.0f}")
    st.success(f"⏳ {t('payback')}: {payback:.1f} Years")

    st.balloons()
    st.header(t("thankyou"))
    if st.button("Start Again"):
        st.session_state.page = 'welcome'
        st.rerun()
