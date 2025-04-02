# 🌿 MoodFlow: GenAI-Powered Mental Health Journal Assistant

**MoodFlow** is a GenAI-powered emotional journaling assistant.  
It lets you express your feelings, receive personalized support from AI with different personas, track mood trends, and reflect with feedback. Built with LLM prompting + Streamlit + sentiment analysis + visualization.

---

## ✨ Features

- 🤖 GPT-powered conversations with customizable tone/persona
- 🎭 Choose your assistant's tone:
  - 🧘 Calm Therapist
  - 🧑‍🏫 CBT Coach
  - 🤗 Cheerful Friend
- 🧠 Sentiment analysis with emoji interpretation
- 📈 Mood trend visualization (AI score vs your rating)
- 📝 Logs your emotional entries, suggestions, and your feedback
- 💬 Optional feedback form to track what helped you

---

## 🛠 Technologies Used

- `streamlit` – front-end interaction
- `openai` – GPT-3.5-turbo LLM for suggestion generation
- `textblob` – for sentiment scoring
- `plotly` – for emotion visualization
- `dotenv` – for secure API key loading

---

## 🚀 How to Run

### 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/moodflow.git cd moodflow


### 2. Install dependencies

### 3. Set up your OpenAI API key

Copy the `.env.example` file:


Then open `.env` and add your API key:


---

## 📸 Demo Preview

| Input | Response |
|-------|----------|
| “I feel anxious about tomorrow.” | “It’s okay to feel anxious. Let’s try some breathing, journaling, or taking a walk.” |

📊 Mood trend chart with emoji annotations is generated automatically!

---

## 📁 Project Structure


---

## 💡 Future Ideas

- 🧾 Weekly summary PDF export
- 🎤 Voice input with Whisper API
- 🧑‍💻 Multi-user login & personalization
- 📊 Emotion category classification (beyond score)

---

## 🪄 Why this project?

This project explores how GenAI and LLM prompting can be used in emotionally intelligent tools.  
It demonstrates skills in:
- Prompt engineering (persona-based tone control)
- NLP sentiment processing
- UI design with Streamlit
- Emotional data visualization
- Feedback loop design

> Made with 💙 by [@chocokook](https://github.com/chocokook)




