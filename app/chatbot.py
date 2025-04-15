import os
import streamlit as st
from openai import OpenAI

# set OpenAI API key
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_chatbot_response(user_input, persona="🧘 Calm Therapist"):
    """
    Generate a chatbot response using OpenAI Chat API with memory (chat history).
    """

    
    system_prompt = f"You are MoodFlow, an AI emotional support assistant with the tone of '{persona}'. \
Respond empathetically and offer helpful but gentle reflections. Use friendly tone and emojis where appropriate."

    # build the messages list for the API call
    messages = [{"role": "system", "content": system_prompt}]

    # add history messages to the API call
    for msg in st.session_state.get("messages", []):
        if msg["role"] in ["user", "assistant"]:
            messages.append({"role": msg["role"], "content": msg["content"]})

    # add the current user input to the messages
    messages.append({"role": "user", "content": user_input})

    # make the API call to OpenAI
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  
        messages=messages
    )

    reply = response.choices[0].message.content.strip()

    return {
        "reply": reply,
        "suggestions": [] 
    }

