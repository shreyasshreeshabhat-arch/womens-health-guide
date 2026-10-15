import streamlit as st
import google.generativeai as genai
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Women's Health Guide", page_icon="🌸", layout="centered")

# --- API SETUP ---
# For local testing, set an environment variable. For deployment, use st.secrets
API_KEY = st.secrets.get("GEMINI_API_KEY", "")
if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    st.error("Please set your GEMINI_API_KEY")

# --- UI & DISCLAIMER ---
st.title("🌸 Women's Health & Symptom Guide")
st.error("⚠️ **Strict Medical Disclaimer:** This tool provides educational information only and is **NOT a diagnostic tool**. It cannot replace professional medical advice. Always consult a gynecologist or healthcare provider for an accurate diagnosis.")

st.markdown("Describe what you are experiencing in your own words. **You can type in English, Hindi, Tamil, Telugu, or any regional language.**")

user_input = st.text_area("Symptoms:", placeholder="E.g., I've been missing my periods for 3 months and breaking out in acne... or मुझे बहुत थकान लगती है और बाल झड़ रहे हैं।", height=150)

# --- AI PROMPT ENGINEERING (The Secret Sauce) ---
SYSTEM_PROMPT = """
You are an empathetic, informative women's health assistant. A user has provided the following symptom description: "{user_input}"

Your tasks:
1. Detect the language of the input. Your entire response MUST be in that same language.
2. Extract and organize the symptoms clearly.
3. Provide general educational information about what these symptoms *could* relate to.
4. If the symptoms align with Polycystic Ovary Syndrome (PCOS), gently mention that these are common traits of PCOS, but explicitly state that PCOS involves a spectrum of symptoms and requires clinical testing (like ultrasounds or blood panels) to confirm.
5. Provide a "Next Steps" section recommending they track these symptoms (e.g., cycle tracking) and consult a healthcare provider.
6. NEVER say "You have..." or "This means you have...". Always use phrases like "These symptoms can sometimes be associated with..."
"""

if st.button("Understand My Symptoms", type="primary"):
    if user_input.strip() == "":
        st.warning("Please enter your symptoms first.")
    else:
        with st.spinner("Analyzing securely..."):
            try:
                model = genai.GenerativeModel('gemini-3.6-flash')
                response = model.generate_content(SYSTEM_PROMPT.format(user_input=user_input))
                
                st.subheader("💡 Understanding Your Symptoms")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")