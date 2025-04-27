import streamlit as st
import requests
import os

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

# Styling and Background setup
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

# Sidebar for pages after Welcome
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

# Main Questions
questions = [
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

# Translations
translations = {
    "Spanish": [
        "¿Cuál es tu edad?",
        "¿Qué actividades te ayudan a relajarte o ser feliz?",
        "¿Con qué frecuencia pasas tiempo con familia o amigos?",
        "¿Cuántas horas duermes normalmente cada noche?",
        "¿Cuál es tu género?",
        "¿Cómo describirías tu nivel actual de estrés?",
        "¿Te sientes cómodo discutiendo tus emociones?",
        "¿Has buscado ayuda profesional antes?",
        "¿Estás abierto a nuevas opciones de apoyo en salud mental?",
        "¿Qué tipo de apoyo sientes que te ayudaría ahora?"
    ],
    "French": [
        "Quel est votre âge?",
        "Quelles activités vous aident à vous détendre ou à être heureux?",
        "À quelle fréquence passez-vous du temps avec votre famille ou vos amis?",
        "Combien d'heures dormez-vous généralement chaque nuit?",
        "Quel est votre genre?",
        "Comment décririez-vous votre niveau actuel de stress?",
        "Êtes-vous à l'aise pour discuter de vos émotions?",
        "Avez-vous déjà demandé de l'aide professionnelle?",
        "Êtes-vous ouvert à de nouvelles options de soutien en santé mentale?",
        "Quel type de soutien pensez-vous qui vous aiderait maintenant?"
    ],
    "German": [
        "Wie alt sind Sie?",
        "Welche Aktivitäten helfen Ihnen, sich zu entspannen oder glücklich zu sein?",
        "Wie oft verbringen Sie Zeit mit Familie oder Freunden?",
        "Wie viele Stunden schlafen Sie normalerweise jede Nacht?",
        "Was ist Ihr Geschlecht?",
        "Wie würden Sie Ihr aktuelles Stresslevel beschreiben?",
        "Fühlen Sie sich wohl dabei, Ihre Emotionen zu besprechen?",
        "Haben Sie jemals professionelle Hilfe gesucht?",
        "Sind Sie offen für neue Optionen zur psychischen Unterstützung?",
        "Welche Art von Unterstützung würde Ihnen jetzt helfen?"
    ],
    "Hindi": [
        "आपकी उम्र क्या है?",
        "कौन सी गतिविधियाँ आपको आराम या खुशी का अनुभव कराती हैं?",
        "आप कितनी बार परिवार या दोस्तों के साथ समय बिताते हैं?",
        "आप आमतौर पर हर रात कितने घंटे सोते हैं?",
        "आपका लिंग क्या है?",
        "आप अपने वर्तमान तनाव स्तर का वर्णन कैसे करेंगे?",
        "क्या आप अपनी भावनाओं पर चर्चा करने में सहज हैं?",
        "क्या आपने पहले पेशेवर मदद ली है?",
        "क्या आप मानसिक स्वास्थ्य समर्थन के नए विकल्पों के लिए तैयार हैं?",
        "अब किस प्रकार के समर्थन से आपको मदद मिल सकती है?"
    ]
}

# Update questions based on selected language
if st.session_state.language != "English":
    questions = translations.get(st.session_state.language, questions)

# Keywords
keywords = [
    "anxiety", "stress", "mental", "therapy", "depression", "health",
    "emotion", "mood", "trauma", "wellbeing", "self-care", "counseling",
    "burnout", "grief", "isolation", "panic", "fear", "support",
    "psychologist", "psychiatrist", "diagnosis", "mental illness", "medication", "help"
]

# --- Page 0: Welcome Page ---
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

# --- Page 1: General Background Questions ---
elif st.session_state.page_number == 1:
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

# --- Page 2: Mental Health Questions ---
elif st.session_state.page_number == 2 and not st.session_state.survey_completed:
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
                "https://mental-health-chatbot-nh4y.onrender.com/generate_feedback",
                json=payload
            )
            feedback_text = response.json().get("feedback", "Sorry, something went wrong.")
            st.session_state.feedback = feedback_text.strip()
            st.session_state.survey_completed = True
            st.success("✅ Survey submitted successfully!")
            st.rerun()
        except Exception as e:
            st.error(f"❌ Failed to get feedback: {e}")

# --- Page 3: After Survey - Chat Page ---
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
            if any(word in user_input.lower() for word in keywords):
                response = requests.post(
                    "https://mental-health-chatbot-nh4y.onrender.com/chat",
                    json={"question": user_input, "language": st.session_state.language}
                )
                bot_reply = response.json().get("reply", "Sorry, something went wrong.")
            else:
                bot_reply = "⚠️ Sorry, I can only assist with mental health-related topics."

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
