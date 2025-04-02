import streamlit as st
import json
import os
import pandas as pd
import plotly.express as px
from datetime import datetime
from app.sentiment_analysis import analyze_sentiment, map_score_to_emoji
from app.chatbot import get_chatbot_response

LOG_PATH = "app/data/user_logs.json"

st.set_page_config(page_title="MoodFlow", layout="centered")
st.title("🧘 MoodFlow - Your Emotion Companion")

# Persona selector
persona = st.selectbox("Choose MoodFlow's tone today:", [
    "🧘 Calm Therapist",
    "🧑‍🏫 CBT Coach",
    "🤗 Cheerful Friend"
])

# Load logs
if not os.path.exists(LOG_PATH):
    os.makedirs("app/data", exist_ok=True)
    with open(LOG_PATH, "w") as f:
        json.dump([], f)

with open(LOG_PATH, "r") as f:
    logs = json.load(f)

# Chat input
user_input = st.text_area("How are you feeling today?", height=120)

if st.button("Talk to MoodFlow"):
    if user_input.strip():
        ai_mood_score = analyze_sentiment(user_input)
        emoji = map_score_to_emoji(ai_mood_score)

        with st.spinner("MoodFlow is thinking..."):
            reply_data = get_chatbot_response(user_input, persona, history=logs)

        st.markdown("### 🤖 MoodFlow's Response")
        st.write(reply_data["reply"])

        st.markdown("### 📝 Suggested Actions")
        for i, suggestion in enumerate(reply_data["suggestions"]):
            st.write(f"{i+1}. {suggestion}")

        # Feedback form
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

# Visualize mood trend
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
