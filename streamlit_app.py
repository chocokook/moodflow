import streamlit as st
from datetime import datetime
import pandas as pd
import plotly.express as px
import os
import json

from app.chatbot import get_chatbot_response
from app.sentiment_analysis import analyze_sentiment, map_score_to_emoji

LOG_PATH = "app/data/user_logs.json"

st.set_page_config(page_title="MoodFlow", layout="centered")

# initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# persona selection
st.title("🧘 MoodFlow - Your Emotion Companion")
persona = st.selectbox("Choose MoodFlow's tone today:", [
    "🧘 Calm Therapist",
    "🧑‍🏫 CBT Coach",
    "🤗 Cheerful Friend"
])

# load logs
if not os.path.exists(LOG_PATH):
    os.makedirs("app/data", exist_ok=True)
    with open(LOG_PATH, "w") as f:
        json.dump([], f)

with open(LOG_PATH, "r") as f:
    logs = json.load(f)

# display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


user_input = st.chat_input("How are you feeling today?")
if user_input:
    # display user input in chat
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # analyze sentiment and map to emoji
    ai_mood_score = analyze_sentiment(user_input)
    emoji = map_score_to_emoji(ai_mood_score)

    # get chatbot response
    with st.spinner("MoodFlow is thinking..."):
        reply_data = get_chatbot_response(user_input, persona)

    # show AI response in chat
    st.chat_message("assistant").markdown(reply_data["reply"])
    st.session_state.messages.append({"role": "assistant", "content": reply_data["reply"]})

    # collect feedback
    with st.form("feedback_form"):
        st.markdown("### 🧩 Did you try any of the suggestions?")
        tried = st.radio("Tried?", ["Yes", "No"], horizontal=True)
        helpfulness = st.slider("Helpfulness Score (1-5)", 1, 5, 3)
        comment = st.text_area("Optional comment (e.g., what worked, what didn’t)")
        submitted = st.form_submit_button("Save Log")

    if submitted:
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "text": user_input,
            "response": reply_data["reply"],
            "ai_mood_score": ai_mood_score,
            "emoji": emoji,
            "suggestions": reply_data["suggestions"],
            "feedback": {
                "tried": tried == "Yes",
                "helpfulness_score": helpfulness,
                "comment": comment
            },
            "user_rating": helpfulness
        }
        logs.append(log_entry)
        with open(LOG_PATH, "w") as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)
        st.success("Your entry has been saved! 💾")

# visualize mood trend
if logs:
    st.markdown("## 📈 Your Mood Trend")
    df = pd.DataFrame([
        {
            "Day": i + 1,
            "AI Score": log["ai_mood_score"],
            "User Rating": log.get("user_rating", None),
            "Emoji": log["emoji"]
        }
        for i, log in enumerate(logs)
    ])

    fig = px.line(df, x="Day", y=["AI Score", "User Rating"], markers=True,
                  title="Mood over Time", labels={"value": "Score"})

    fig.add_scatter(x=df["Day"], y=df["AI Score"], mode="text",
                    text=df["Emoji"], textposition="top center",
                    showlegend=False)

    st.plotly_chart(fig, use_container_width=True)
