from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

class SurveyPayload(BaseModel):
    responses: list
    language: str

class ChatPayload(BaseModel):
    question: str
    language: str

# Mental health keywords
MENTAL_HEALTH_KEYWORDS = [
    "anxiety", "stress", "mental", "therapy", "depression", "health",
    "emotion", "mood", "trauma", "wellbeing", "self-care", "counseling",
    "burnout", "grief", "isolation", "panic", "fear", "support",
    "psychologist", "psychiatrist", "diagnosis", "mental illness", "medication", "help"
]

def is_mental_health_related(text: str) -> bool:
    return any(word in text.lower() for word in MENTAL_HEALTH_KEYWORDS)

# -----------------
# API 1: Survey Summary
@app.post("/generate_feedback")
async def generate_feedback(payload: SurveyPayload):
    input_text = "\n".join([f"Q: {item['question']}\nA: {item['answer']}" for item in payload.responses])

    if not any(is_mental_health_related(item["question"]) or is_mental_health_related(item["answer"]) for item in payload.responses):
        return {
            "feedback": "⚠️ I'm sorry, I can only generate feedback for mental health-related questions."
        }

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a compassionate mental health assistant who provides a warm summary based on user's answers."},
                {"role": "user", "content": input_text}
            ]
        )
        summary = response.choices[0].message.content.strip()
        return {"feedback": summary}

    except Exception as e:
        return {"feedback": f"⚠️ An error occurred while generating feedback: {str(e)}"}

# -----------------
# API 2: Chat Follow-up
@app.post("/chat")
async def chat(payload: ChatPayload):
    if not is_mental_health_related(payload.question):
        return {"reply": "⚠️ I'm sorry, I can only answer mental health related topics."}

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a friendly mental health chatbot. Answer clearly and only respond to the specific user's question."},
                {"role": "user", "content": payload.question}
            ]
        )
        reply = response.choices[0].message.content.strip()
        return {"reply": reply}

    except Exception as e:
        return {"reply": f"⚠️ An error occurred while answering: {str(e)}"}
import os

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))  # default to 10000 locally
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
