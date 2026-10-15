import streamlit as st
import google.generativeai as genai
import os

# --- PAGE CONFIG & UI POLISH ---
st.set_page_config(page_title="Women's Health Guide", page_icon="🌸", layout="wide")

# Custom CSS to improve button and text appearance
st.markdown("""
    <style>
    .stButton>button { border-radius: 8px; font-weight: bold; }
    .stDownloadButton>button { background-color: #ff4b4b; color: white; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

# --- API SETUP ---
API_KEY = st.secrets.get("GEMINI_API_KEY", "")
if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-3.6-flash')
else:
    st.error("⚠️ Please set your GEMINI_API_KEY in the Streamlit secrets dashboard.")

# --- SIDEBAR: DISCLAIMER ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3050/3050431.png", width=80)
    st.title("About This App")
    st.error("⚠️ **Strict Medical Disclaimer:** This tool provides educational information only and is **NOT a diagnostic tool**. Always consult a gynecologist or healthcare provider for an accurate diagnosis.")
    st.markdown("Built for Hackathon 2026. Empowering women's health literacy across regional languages.")

# --- MAIN NAVIGATION TABS ---
tab1, tab2, tab3 = st.tabs(["🌸 Symptom Checker", "🔍 AI General Search & FAQ", "📞 Helplines & Public Clinics"])

# ==========================================
# TAB 1: SYMPTOM CHECKER & DOCTOR EXPORT
# ==========================================
with tab1:
    st.header("Understand Your Symptoms")
    st.markdown("Describe what you are experiencing. **You can type in English, Hindi, Tamil, Telugu, or any regional language.**")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        user_input = st.text_area("Symptoms:", placeholder="E.g., I've been missing my periods for 3 months... or मुझे बहुत थकान लगती है", height=150)
        pain_level = st.slider("Current Pain Level (1 = None, 10 = Severe)", 1, 10, 1)
        
    with col2:
        st.markdown("**Common Factors (Optional):**")
        acne = st.checkbox("Severe Acne / Breakouts")
        fatigue = st.checkbox("Unexplained Fatigue")
        weight = st.checkbox("Sudden Weight Gain")
    
    SYSTEM_PROMPT = """
    You are an empathetic, informative women's health assistant. 
    User Symptoms: "{user_input}"
    Pain Level: {pain_level}/10
    Additional Factors: Acne ({acne}), Fatigue ({fatigue}), Weight Gain ({weight}).

    1. Detect the language of the input and respond entirely in that same language.
    2. Extract and organize the symptoms clearly.
    3. Provide general educational information about what these symptoms *could* relate to.
    4. If symptoms align with PCOS, gently mention these are common traits, but explicitly state that clinical testing is required.
    5. NEVER say "You have..." or diagnose the user. Always use "These symptoms can sometimes be associated with..."
    """
    
    if st.button("Analyze Symptoms", type="primary"):
        if user_input.strip() == "":
            st.warning("Please enter your symptoms first.")
        else:
            with st.spinner("Analyzing securely..."):
                try:
                    formatted_prompt = SYSTEM_PROMPT.format(
                        user_input=user_input, pain_level=pain_level, 
                        acne=acne, fatigue=fatigue, weight=weight
                    )
                    response = model.generate_content(formatted_prompt)
                    
                    st.subheader("💡 Analysis & Next Steps")
                    st.write(response.text)
                    
                    # Generate a downloadable report for a doctor
                    report_content = f"Patient Symptom Report\n\nSymptoms: {user_input}\nPain Level: {pain_level}/10\nAdditional Factors: Acne({acne}), Fatigue({fatigue}), Weight Gain({weight})\n\nAI Notes:\n{response.text}"
                    st.download_button(
                        label="📄 Download Report for Doctor",
                        data=report_content,
                        file_name="Symptom_Report.txt",
                        mime="text/plain"
                    )
                except Exception as e:
                    st.error(f"An error occurred: {e}")

# ==========================================
# TAB 2: AI GENERAL SEARCH & FAQ
# ==========================================
with tab2:
    st.header("Search Women's Health Topics")
    st.markdown("Ask any general question about menstrual health, PCOS, nutrition, or wellness.")
    
    search_query = st.text_input("Ask a question:", placeholder="E.g., What are the best foods to eat if I have PCOS?")
    
    if st.button("Search"):
        if search_query:
            with st.spinner("Searching..."):
                search_prompt = f"Provide a brief, medically accurate, and highly empathetic answer to this general women's health question: '{search_query}'. Do not diagnose."
                search_response = model.generate_content(search_prompt)
                st.info(search_response.text)
                
    st.divider()
    st.subheader("📌 Frequently Asked Questions")
    with st.expander("What is the difference between normal cramps and severe pain?"):
        st.write("Mild cramping is common during menstruation. However, pain that stops you from doing daily activities, causes nausea, or isn't relieved by standard painkillers could be a sign of conditions like endometriosis and should be discussed with a doctor.")
    with st.expander("How is PCOS diagnosed?"):
        st.write("PCOS is typically diagnosed by a gynecologist using the Rotterdam criteria. They will look for irregular periods, physical signs of high androgens (like acne or excess hair), and perform an ultrasound to check for cysts on the ovaries.")

# ==========================================
# TAB 3: HELPLINES & PUBLIC CLINICS
# ==========================================
with tab3:
    st.header("📞 National Helplines & Support")
    st.markdown("Verified 24/7 emergency and support lines in India.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.success("**NCW Women Helpline:** 14490 (24x7 Digital Complaint & Counselling)")
        st.success("**National Health Helpline:** 104 (Free medical advice & doctor connection)")
    with col_b:
        st.info("**Tele-MANAS:** 14416 (Govt. Mental Health Support & Therapy)")
        st.info("**Emergency Response:** 112 (Police, Fire, Medical)")

    st.divider()
    st.header("🏥 Public Clinics & Mental Health Centers (Bengaluru)")