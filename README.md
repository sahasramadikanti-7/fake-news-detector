# 📰 Fake News Detection System

## 📌 Project Overview

Fake news and misleading information can spread rapidly through social media,
messaging applications, and online platforms.

This project is an AI-based Fake News Detection System developed using
Python, Streamlit, and Google Gemini API.

The system allows a user to enter a news paragraph and uses a few-shot
prompting approach to classify the news as **Likely Fake News** or
**Likely Real News**.

It also provides an AI-estimated confidence percentage and an explanation
for the prediction.

---

## 🎯 Objectives

The main objectives of this project are:

- To develop a simple AI-based fake news detection application.
- To classify a given news paragraph as likely fake or real.
- To use few-shot prompting with 10 example cases.
- To provide fake and real confidence percentages.
- To provide an understandable explanation for the prediction.
- To create an easy-to-use web interface using Streamlit.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | Web application interface |
| Google Gemini API | AI-based news analysis |
| Google GenAI SDK | Connects Python application with Gemini |
| JSON | Structured AI response |
| VS Code | Development environment |

---

## ⚙️ How the System Works

The system follows these steps:

1. The user enters a news paragraph.
2. The application prepares a prompt containing 10 example cases.
3. The examples demonstrate the expected FAKE and REAL classification.
4. The news paragraph is added to the prompt.
5. Google Gemini analyzes the submitted news.
6. Gemini returns:
   - Prediction
   - Fake confidence
   - Real confidence
   - Explanation
7. Streamlit displays the result to the user.

### System Flow

```text
User enters news
       ↓
Streamlit Interface
       ↓
Few-Shot Prompt
(10 Examples)
       ↓
Google Gemini API
       ↓
AI Analysis
       ↓
Prediction + Confidence + Explanation
       ↓
Result displayed in Streamlit