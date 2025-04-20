import os
import openai
from dotenv import load_dotenv

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_supportive_feedback(responses):
    # Try OpenAI if key is available
    if client.api_key:
        try:
            conversation = [
                {"role": "system", "content": "You are a kind and empathetic mental health assistant."},
                {"role": "user", "content": format_responses(responses)}
            ]
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=conversation
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"We tried generating a GPT-based response but encountered an error: {e}"

    # Fallback to rule-based if no API key or error
    feedback = []

    for item in responses:
        q = item.question.lower()
        a = item.answer.lower()

        if "diagnosed" in q and ("yes" in a or "i have" in a):
            feedback.append("Thank you for sharing that you've been diagnosed. You're not alone — many people manage their mental health and thrive.")

        elif "comfortable discussing" in q and "no" in a:
            feedback.append("It's completely okay to feel uncomfortable discussing mental health. Everyone opens up in their own time. You're doing great just by starting this conversation.")

        elif "stress" in q:
            if any(x in a for x in ["high", "very", "extreme"]):
                feedback.append("It sounds like you’re under a lot of stress right now. Please take a moment for yourself — even 5 minutes of breathing can help.")
            else:
                feedback.append("It’s great that your stress feels manageable. Keep doing what’s working for you!")

        elif "support" in q:
            feedback.append("You deserve support, whatever form it takes — whether that’s talking to someone, journaling, or just having quiet time.")

        elif "therapy" in q or "professional help" in q:
            if "no" in a:
                feedback.append("If you ever change your mind about therapy, it’s always there for you — and there are many free or anonymous resources too.")
            else:
                feedback.append("That’s amazing! Seeking help is a powerful and strong choice. Kudos to you!")

    if not feedback:
        feedback.append("Thank you for sharing your answers. Just starting this journey is a big step — you're doing something powerful for yourself.")

    return "\n\n".join(feedback)

def format_responses(responses):
    return "\n".join([f"{r.question} {r.answer}" for r in responses])
