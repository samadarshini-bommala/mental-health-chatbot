import streamlit as st
import json
import requests

st.set_page_config(page_title="🧠 Mental Health Chatbot")
st.title("🧠 Mental Health Support - Interactive Mode")

# Load questions
with open("questions.json", "r") as f:
    questions = json.load(f)

# Session state setup
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
    st.session_state.chat_history = []
    st.session_state.answers = []
    st.session_state.feedback = ""
    st.session_state.in_followup = False
    st.session_state.temp_input = None
    st.session_state.last_button_clicked = None

# Show previous chat history
for entry in st.session_state.chat_history:
    with st.chat_message(entry["role"]):
        st.markdown(entry["message"])

# If questions left, show next one
if st.session_state.current_question < len(questions):
    q = questions[st.session_state.current_question]

    # Display the question on screen
    if st.session_state.current_question > 0:
        if st.button("⬅️ Back to Previous Question"):
            st.session_state.current_question -= 1
            st.session_state.chat_history = st.session_state.chat_history[:-2]
            st.session_state.answers = st.session_state.answers[:-1]
            st.rerun()
    st.markdown(f"**{q}**")

    user_input = None
    yes_no_question = any(kw in q.lower() for kw in ["diagnosed", "comfortable", "believe your productivity", "sought professional help", "open to trying"])

    if yes_no_question:
        user_input = st.radio("Choose your answer:", ["", "Yes", "No"], index=0, key=f"radio_{st.session_state.current_question}")
        if user_input in ["Yes", "No"]:
            st.session_state.chat_history.append({"role": "assistant", "message": q})
            st.session_state.chat_history.append({"role": "user", "message": user_input})
            st.session_state.answers.append({"question": q, "answer": user_input})
            st.session_state.current_question += 1
            st.rerun()
    elif "support do you feel would help you right now" in q.lower():
        user_input = st.chat_input("Type your answer and press Enter")
        if user_input:
            st.session_state.chat_history.append({"role": "assistant", "message": q})
            st.session_state.chat_history.append({"role": "user", "message": user_input})
            st.session_state.answers.append({"question": q, "answer": user_input})

            # Immediately generate and show feedback
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/generate_feedback",
                    json={"responses": st.session_state.answers}
                )
                st.session_state.feedback = response.json().get("feedback", "Sorry, something went wrong.")
            except Exception as e:
                st.session_state.feedback = f"Error: {e}"

            st.session_state.chat_history.append({
    "role": "assistant",
    "message": f"**Your Support Summary:**\\n\\n{st.session_state.feedback}"
})


            st.session_state.current_question += 1
            st.rerun()
    else:
        user_input = st.chat_input("Type your answer and press Enter")
        if user_input:
            st.session_state.chat_history.append({"role": "assistant", "message": q})
            st.session_state.chat_history.append({"role": "user", "message": user_input})
            st.session_state.answers.append({"question": q, "answer": user_input})
            st.session_state.current_question += 1
            st.rerun()

else:
    # All questions answered
    if not st.session_state.feedback:
        with st.chat_message("assistant"):
            st.markdown("Thanks for completing the survey. Generating your supportive summary... 💙")

            try:
                response = requests.post(
                    "http://127.0.0.1:8000/generate_feedback",
                    json={"responses": st.session_state.answers}
                )
                st.session_state.feedback = response.json().get("feedback", "Sorry, something went wrong.")
            except Exception as e:
                st.session_state.feedback = f"Error: {e}"

    with st.chat_message("assistant"):
        st.markdown(f"**Your Support Summary:**\n\n{st.session_state.feedback}")

    # Let user continue asking questions after survey
    followup = st.chat_input("You can ask more questions here...")
    if followup:
        st.session_state.chat_history.append({"role": "user", "message": followup})

        # Simple mental health keyword check
        keywords = [
    "anxiety", "stress", "mental", "therapy", "depression", "health",
    "emotion", "mood", "trauma", "wellbeing", "self-care", "counseling",
    "burnout", "grief", "isolation", "panic", "fear", "support",
    "psychologist", "psychiatrist", "diagnosis", "mental illness" , "feel" , "talk"
]
        if any(word in followup.lower() for word in keywords):
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/generate_feedback",
                    json={"responses": st.session_state.answers + [{"question": followup, "answer": followup}]}
                )
                followup_reply = response.json().get("feedback", "Sorry, something went wrong.")
            except Exception as e:
                followup_reply = f"Error: {e}"
        else:
            followup_reply = "I'm sorry, I can only answer questions related to mental health. 💬"

        st.session_state.chat_history.append({"role": "assistant", "message": followup_reply})
        st.rerun()
