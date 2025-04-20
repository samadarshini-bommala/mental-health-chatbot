# mental-health-chatbot
# 🧠 Mental Health Support Chatbot

A full-stack chatbot app that walks users through a short mental health self-assessment, collects their answers, and generates supportive feedback.

---

## 📌 Features
- Step-by-step chatbot flow using real U.S.-based mental health survey questions
- Streamlit frontend for easy interaction
- FastAPI backend to handle supportive reflection logic
- Empathetic feedback generated using rule-based logic (can be extended to OpenAI)

---

## 🧩 Technologies Used
- **Frontend:** Streamlit
- **Backend:** FastAPI, Python 3.9+
- **API Logic:** Pydantic + rule-based logic in Python
- **Extras:** SQLite data (U.S. survey), optional OpenAI integration

---

## 📁 Folder Structure
```plaintext
mental-health-chatbot/
├── backend/
│   ├── main.py
│   ├── response_logic.py
│   └── requirements.txt
├── frontend/
│   ├── app.py
│   └── questions.json
├── data/
│   └── mental_health.sqlite
├── .gitignore
└── README.md
```

---

## 🚀 How to Run

### 1. Clone the Repo
```bash
git clone https://github.com/your-username/mental-health-chatbot.git
cd mental-health-chatbot
```

### 2. Create & Activate Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate    # Windows
```

### 3. Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### 4. Run FastAPI Backend
```bash
cd backend
uvicorn main:app --reload
```

### 5. Run Streamlit Frontend
In a new terminal:
```bash
cd frontend
streamlit run app.py
```

---

## 🌐 API Contract
**Endpoint:** `/generate_feedback`
- **Method:** POST
- **Payload:**
```json
{
  "responses": [
    {"question": "Have you been diagnosed...", "answer": "Yes"},
    {"question": "How do you manage stress?", "answer": "Breathing exercises"}
  ]
}
```
- **Response:**
```json
{
  "feedback": "Thank you for sharing..."
}
```

---

## ✅ Grading Alignment
- ✅ Frontend: Streamlit chatbot
- ✅ Backend: Python + API logic
- ✅ API: FastAPI with Pydantic models
- ✅ System Design: Smart feedback generator
- 🔄 Bonus: Ready for AWS API Gateway deployment

---

## 💙 Acknowledgement
This chatbot aims to provide **supportive and reflective guidance**, not medical advice. For any crisis, please contact a licensed professional or emergency service.

---

Feel free to extend this project to add:
- Mood tracking
- GPT-powered feedback
- Resource links or maps

---
