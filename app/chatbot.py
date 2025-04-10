import streamlit as st
from openai import OpenAI

# ✅ 使用 st.secrets 更安全
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Persona prompt templates
persona_prompts = {
    "🧘 Calm Therapist": (
        "You are a warm, empathetic mental health assistant. "
        "When the user shares their feelings, respond with gentle validation, "
        "deep understanding, and 2-3 soft suggestions for self-care."
    ),
    "🧑‍🏫 CBT Coach": (
        "You're a cognitive behavioral therapist. When the user describes a mood, "
        "identify unhelpful thoughts or beliefs, and guide them to reframe them. "
        "Then suggest specific action steps rooted in CBT techniques."
    ),
    "🤗 Cheerful Friend": (
        "You’re a supportive, upbeat friend who knows how to cheer someone up. "
        "Use casual tone, share some positive energy, maybe a funny thought, "
        "and recommend 2-3 light actions to lift the mood."
    ),
}

def get_chatbot_response(user_input: str, persona: str, history: list = []) -> dict:
    """Return chatbot reply and 2-3 wellness suggestions based on persona tone."""

    messages = [
        {"role": "system", "content": persona_prompts.get(persona, persona_prompts["🧘 Calm Therapist"])}
    ]

    for entry in history[-3:]:  # limit memory to last 3 logs
        messages.append({"role": "user", "content": entry["text"]})
        messages.append({"role": "assistant", "content": entry["response"]})

    messages.append({"role": "user", "content": user_input})

    # ✅ 使用新版 API 调用方式
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7
    )

    full_reply = response.choices[0].message.content

    # Extract suggestions heuristically (bulleted or numbered)
    suggestions = []
    for line in full_reply.split("\n"):
        if any(kw in line.lower() for kw in ["1", "2", "•", "-"]):
            clean = line.strip("•- ").strip()
            if clean:
                suggestions.append(clean)

    return {
        "reply": full_reply,
        "suggestions": suggestions[:3]
    }
