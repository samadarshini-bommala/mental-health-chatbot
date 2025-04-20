import streamlit as st
import json
import requests

st.set_page_config(page_title="Mental Health Support Bot")
st.title("🧠 Mental Health Support Chatbot")

# Load questions from local JSON
with open("questions.json", "r") as f:

    questions = json.load(f)

# Initialize session state
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
    st.session_state.answers = []

# Display current question
if st.session_state.current_question < len(questions):
    question = questions[st.session_state.current_question]
    answer = st.text_input(question, key=st.session_state.current_question)

    if st.button("Next") and answer:
        st.session_state.answers.append({
            "question": question,
            "answer": answer
        })
        st.session_state.current_question += 1
        st.rerun()


else:
    st.success("Thank you for completing the survey. Here's your personalized support summary:")

    # Send answers to backend API
    try:
        response = requests.post(
            "http://127.0.0.1:8000/generate_feedback",
            json={"responses": st.session_state.answers}
        )
        feedback = response.json().get("feedback", "Sorry, something went wrong.")
    except Exception as e:
        feedback = f"Error: {e}"

    st.markdown(f"**Your Support Summary:**\n\n{feedback}")

    # Reset session
    if st.button("Start Over"):
        st.session_state.current_question = 0
        st.session_state.answers = []
        st.rerun()
