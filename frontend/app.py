import streamlit as st
import requests

# Set app config
st.set_page_config(page_title="🧠 Mental Health Chatbot", layout="wide")

# Initialize session state
for key, value in {
    "page_number": 0,
    "general_answers": [],
    "mental_answers": [],
    "feedback": "",
    "survey_completed": False,
    "chat_history": [],
    "language": "English"
}.items():
    if key not in st.session_state:
        st.session_state[key] = value

# Apply different backgrounds
if st.session_state.page_number == 0:
    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background-image: url('https://images.unsplash.com/photo-1506744038136-46273834b3fb?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1740&q=80');
        background-size: cover;
        background-position: center;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 12px;
        font-size: 16px;
        border-radius: 10px;
        width: 200px;
        margin: auto;
        display: block;
    }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #f5f7fa;
    }
    .stRadio > div {
        display: flex;
        flex-direction: row;
        gap: 20px;
    }
    .stButton button {
        margin-right: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar only on pages 1, 2, and 3
if st.session_state.page_number != 0:
    with st.sidebar:
        st.image(
            "https://images.unsplash.com/photo-1506126613408-eca07ce68773?crop=entropy&cs=tinysrgb&fit=crop&h=300&w=400",
            caption="Stay Positive 🌿",
            use_container_width=True
        )
        st.title("🧘 Mental Health Chatbot")
        st.markdown("---")
        st.markdown("Providing compassionate mental health support, one conversation at a time. 💬")
        st.markdown("---")

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


# Default questions
default_questions = [
    "What is your age?",
    "What activities help you feel relaxed or happy?",
    "How often do you spend time with family or friends?",
    "How many hours of sleep do you usually get each night?",
    "What is your gender?",
    "How would you describe your current stress level?",
    "Are you comfortable discussing your emotions?",
    "Have you sought professional help before?",
    "Are you open to new mental health support options?",
    "What type of support do you feel would help you right now?"
]

# Mental health keywords
keywords = [
    "anxiety", "stress", "mental", "therapy", "depression", "health",
    "emotion", "mood", "trauma", "wellbeing", "self-care", "counseling",
    "burnout", "grief", "isolation", "panic", "fear", "support",
    "psychologist", "psychiatrist", "diagnosis", "mental illness", "medication", "help"
]

# Welcome Page
if st.session_state.page_number == 0:
    col1, col2 = st.columns([6, 1])

    with col2:
        st.selectbox(
            "🌐",
            ["English", "Spanish", "French", "German", "Hindi"],
            key="language",
            label_visibility="collapsed"
        )

    st.markdown("<h1 style='text-align: center; color: #333;'>🧠 Welcome to the Mental Health Companion</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #555;'>“I am here to listen and help you find the strength to overcome your challenges.” 🌟</h3>", unsafe_allow_html=True)

    start_button = st.button("Start Survey ➡️")

    if start_button:
        st.session_state.page_number = 1
        st.rerun()

# General Questions Page
elif st.session_state.page_number == 1:
    questions = default_questions
    if st.session_state.language != "English":
        questions = translations.get(st.session_state.language, default_questions)

    st.title("📝 General Background Questions")
    with st.form("general_form"):
        age = st.text_input(f"🔢 {questions[0]}")
        activities = st.text_area(f"🏖️ {questions[1]}")
        social = st.radio(f"👥 {questions[2]}", ["Rarely", "Sometimes", "Often", "Daily"])
        sleep = st.slider(f"😴 {questions[3]}", 0, 12, 7)

        col1, col2 = st.columns([1, 1])

        with col1:
            back_button = st.form_submit_button("⬅️ Back")
        with col2:
            next_button = st.form_submit_button("Next ➡️")

    if back_button:
        st.session_state.page_number = 0
        st.rerun()
    elif next_button:
        st.session_state.general_answers = [
            {"question": questions[0], "answer": age},
            {"question": questions[1], "answer": activities},
            {"question": questions[2], "answer": social},
            {"question": questions[3], "answer": str(sleep)}
        ]
        st.session_state.page_number = 2
        st.rerun()

# Mental Health Questions Page
elif st.session_state.page_number == 2 and not st.session_state.survey_completed:
    questions = default_questions
    if st.session_state.language != "English":
        questions = translations.get(st.session_state.language, default_questions)

    st.title("🧠 Mental Health Related Questions")

    with st.form("mental_form"):
        gender = st.radio(f"🚻 {questions[4]}", ["Male", "Female", "Other"])
        stress = st.slider(f"📈 {questions[5]}", 1, 10, 5)
        emotions = st.radio(f"💬 {questions[6]}", ["Yes", "No"])
        professional_help = st.radio(f"👨‍⚕️ {questions[7]}", ["Yes", "No"])
        open_support = st.radio(f"🌟 {questions[8]}", ["Yes", "No"])
        needed_support = st.text_area(f"❤️ {questions[9]}")

        col1, col2 = st.columns([1, 1])

        with col1:
            back_button = st.form_submit_button("⬅️ Back")
        with col2:
            submit_button = st.form_submit_button("Submit Survey")

    if back_button:
        st.session_state.page_number = 1
        st.rerun()
    elif submit_button:
        st.session_state.mental_answers = [
            {"question": questions[4], "answer": gender},
            {"question": questions[5], "answer": str(stress)},
            {"question": questions[6], "answer": emotions},
            {"question": questions[7], "answer": professional_help},
            {"question": questions[8], "answer": open_support},
            {"question": questions[9], "answer": needed_support}
        ]

        payload = {
            "responses": st.session_state.general_answers + st.session_state.mental_answers,
            "language": st.session_state.language
        }

        try:
            response = requests.post(
                "https://your-render-url.onrender.com/generate_feedback",
                json=payload
            )
            feedback_text = response.json().get("feedback", "Sorry, something went wrong.")
            st.session_state.feedback = feedback_text.strip()
            st.session_state.survey_completed = True
            st.success("✅ Survey submitted successfully!")
            st.rerun()
        except Exception as e:
            st.error(f"❌ Failed to get feedback: {e}")

# Chat Page after Survey
elif st.session_state.survey_completed:
    st.title("📋 Your Mental Health Support Summary")
    if st.session_state.feedback:
        st.success(st.session_state.feedback)
    else:
        st.warning("⚠️ No feedback found.")

    st.markdown("---")
    st.subheader("💬 Continue Chatting:")

    user_input = st.chat_input("Type your mental health question...")

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        try:
            # Check for keywords
            if user_input and any(word in user_input.lower() for word in keywords):
                response = requests.post(
                    "https://mental-health-chatbot-nh4y.onrender.com/generate_feedback",
                    json={
                        "responses": st.session_state.general_answers + st.session_state.mental_answers + [{"question": user_input, "answer": user_input}],
                        "language": st.session_state.language
                    }
                )
                bot_reply = response.json().get("feedback", "Sorry, something went wrong.")
            else:
                response = requests.post(
                    "https://mental-health-chatbot-nh4y.onrender.com/chat",
                    json={"question": user_input, "language": st.session_state.language}
                )
                bot_reply = response.json().get("reply", "Sorry, something went wrong.")
        except Exception as e:
            bot_reply = f"Error: {e}"

        st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
        with st.chat_message("assistant"):
            st.markdown(bot_reply)

    st.markdown("---")
    if st.button("🔄 Restart Survey"):
        for key in ["general_answers", "mental_answers", "feedback", "survey_completed", "chat_history", "page_number"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
