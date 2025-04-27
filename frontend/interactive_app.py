import streamlit as st
import json
import requests

st.set_page_config(page_title="🧠 Mental Health Chatbot")

# Background styling
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://raw.githubusercontent.com/samadarshini-bommala/mental-health-chatbot/main/frontend/background.png");
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center;
    background-attachment: fixed;
}
</style>
""", unsafe_allow_html=True)

st.title("🧠 Mental Health Support - Interactive Mode")

# Language selection
language = st.selectbox("Choose your language:", ["English", "Spanish", "French", "German", "Hindi"])
st.session_state.language = language

# Load questions
with open("questions.json", "r") as f:
    all_questions = json.load(f)

# Language translations for questions
translations = {
    "Spanish": [
        "¿Cuál es tu edad?",
        "¿Te sientes cómodo discutiendo tus emociones con otros?",
        "¿Has sido diagnosticado con alguna condición de salud mental?",
        "¿Crees que tu salud mental afecta tu productividad?",
        "¿Has buscado ayuda profesional en el pasado?",
        "¿Estás abierto a probar nuevas opciones de apoyo de salud mental?",
        "¿Qué tipo de apoyo sientes que te ayudaría ahora?"
    ],
    "French": [
        "Quel est votre âge?",
        "Vous sentez-vous à l'aise de parler de vos émotions avec les autres?",
        "Avez-vous été diagnostiqué avec des troubles de santé mentale?",
        "Croyez-vous que votre santé mentale affecte votre productivité?",
        "Avez-vous déjà demandé de l'aide professionnelle?",
        "Êtes-vous ouvert à essayer de nouvelles options de soutien en santé mentale?",
        "Quel type de soutien pensez-vous qui vous aiderait maintenant?"
    ],
    "German": [
        "Wie alt sind Sie?",
        "Fühlen Sie sich wohl dabei, Ihre Gefühle mit anderen zu besprechen?",
        "Wurden Sie mit psychischen Erkrankungen diagnostiziert?",
        "Glauben Sie, dass Ihre psychische Gesundheit Ihre Produktivität beeinflusst?",
        "Haben Sie schon professionelle Hilfe in Anspruch genommen?",
        "Sind Sie offen für neue Unterstützungsangebote zur psychischen Gesundheit?",
        "Welche Art von Unterstützung würde Ihnen jetzt helfen?"
    ],
    "Hindi": [
        "आपकी उम्र क्या है?",
        "क्या आप दूसरों के साथ अपनी भावनाओं पर चर्चा करने में सहज हैं?",
        "क्या आपको किसी मानसिक स्वास्थ्य स्थिति का निदान किया गया है?",
        "क्या आपको लगता है कि आपका मानसिक स्वास्थ्य आपकी उत्पादकता को प्रभावित करता है?",
        "क्या आपने पहले पेशेवर मदद ली है?",
        "क्या आप मानसिक स्वास्थ्य सहायता के नए विकल्पों को आज़माने के लिए तैयार हैं?",
        "आपको अभी किस प्रकार के समर्थन की आवश्यकता महसूस होती है?"
    ]
}

questions = all_questions if language == "English" else translations.get(language, all_questions)

# Session state setup
if "answers" not in st.session_state:
    st.session_state.answers = []
if "feedback" not in st.session_state:
    st.session_state.feedback = ""

# Survey Section
st.header("📝 Complete the Survey")

# Language selection
language = st.selectbox("Choose your language:", ["English", "Spanish", "French", "German", "Hindi"])
st.session_state.language = language
with st.form("survey_form"):
    user_responses = []
    for i, q in enumerate(questions):
        st.markdown(
            f"""
            <div style='background-color: #f0f9ff; padding: 10px; border-radius: 8px; font-size: 15px; margin-bottom: 10px;'>
                <strong>{q}</strong>
            </div>
            """,
            unsafe_allow_html=True
        )

        if any(kw in q.lower() for kw in ["diagnosed", "comfortable", "believe your productivity", "sought professional help", "open to trying"]):
            answer = st.radio("", ["Yes", "No"], key=f"q_{i}")
        elif "support do you feel would help you right now" in q.lower():
            answer = st.text_input("", key=f"q_{i}")
        else:
            answer = st.text_input("", key=f"q_{i}")
        user_responses.append({"question": q, "answer": answer})

    submitted = st.form_submit_button("Submit Survey")
    if submitted:
        st.success("✅ Thank you for submitting the survey!")
        st.session_state.answers = user_responses
        try:
            response = requests.post(
                "http://127.0.0.1:8000/generate_feedback",
                json={"responses": st.session_state.answers, "language": st.session_state.language}
            )
            feedback_text = response.json().get("feedback", "Sorry, something went wrong.")
            feedback_text = feedback_text.replace(
                "⚠️ I'm sorry, I can only generate feedback for mental health-related questions.", ""
            ).strip()
            
            # Always store feedback on submission
            st.session_state.feedback = feedback_text
        except Exception as e:
            st.session_state.feedback = f"Error: {e}"

# Display Support Summary
if st.session_state.feedback:
    st.subheader("Your Support Summary")
    st.markdown(st.session_state.feedback)

# Follow-up interaction
followup = st.chat_input("You can ask more questions here...")
if followup:
    keywords = [
        "anxiety", "stress", "mental", "therapy", "depression", "health",
        "emotion", "mood", "trauma", "wellbeing", "self-care", "counseling",
        "burnout", "grief", "isolation", "panic", "fear", "support",
        "psychologist", "psychiatrist", "diagnosis", "mental illness"
    ]
    if any(word in followup.lower() for word in keywords):
        try:
            response = requests.post(
                "http://127.0.0.1:8000/generate_feedback",
                json={"responses": st.session_state.answers + [{"question": followup, "answer": followup}], "language": st.session_state.language}
            )
            followup_reply = response.json().get("feedback", "Sorry, something went wrong.")
        except Exception as e:
            followup_reply = f"Error: {e}"
    else:
        followup_reply = "I'm sorry, I can only answer questions related to mental health. 💬"

    with st.chat_message("user"):
        st.markdown(f"""
        <div style='background-color: #e6f7ff; padding: 10px; border-radius: 8px;'>
            {followup}
        </div>
        """, unsafe_allow_html=True)
    with st.chat_message("assistant"):
        st.markdown(f"""
        <div style='background-color: #fff7e6; padding: 10px; border-radius: 8px;'>
            {followup_reply}
        </div>
        """, unsafe_allow_html=True)
