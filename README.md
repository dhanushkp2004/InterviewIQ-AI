<!-- ======================== BANNER ======================== -->

<p align="center"> <img src="interview.png" width="100%" alt="PulseConnect Banner"/> </p>
# 🧠 InterviewIQ AI

<p align="center">

<p align="center">
<img src="https://readme-typing-svg.demolab.com?font=Poppins&weight=700&size=30&pause=1000&color=7B68EE&center=true&vCenter=true&width=1000&lines=Master+Your+Next+Interview+with+AI;AI-Powered+Interview+Preparation;Resume+Matching+and+ATS+Analysis;Real-Time+AI+Feedback;FastAPI+%7C+Python+%7C+OpenAI" />
</p>

</p>

<p align="center">

<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi"/>
<img src="https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai"/>
<img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite"/>
<img src="https://img.shields.io/badge/HTML-E34F26?style=for-the-badge&logo=html5"/>
<img src="https://img.shields.io/badge/CSS-1572B6?style=for-the-badge&logo=css3"/>
<img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript"/>
<img src="https://img.shields.io/github/license/YOUR_USERNAME/InterviewIQ-AI?style=for-the-badge"/>

</p>

<p align="center">

### 🎯 *Practice Smarter • Learn Faster • Get Hired*

</p>

---

# 🚀 Overview

**InterviewIQ AI** is a modern AI-powered interview preparation platform designed to help job seekers practice technical interviews, evaluate responses, improve resumes, and boost interview confidence.

Powered by **FastAPI**, **Python**, and the **OpenAI Responses API**, InterviewIQ AI simulates real interview experiences with intelligent feedback, resume-job matching, and personalized recommendations.

When no API key is available, the platform seamlessly switches to **Demo Mode**, ensuring every feature remains fully functional.

---

# ✨ Key Features

* 🤖 AI Interview Question Generator
* 💬 Intelligent Answer Evaluation
* 📄 Resume vs Job Description Matching
* 📊 ATS Compatibility Score
* 🧠 Skill Gap Analysis
* 📈 User Dashboard & Progress Tracking
* 🔐 Secure Authentication
* 💾 SQLite Database
* ⚡ Demo Mode (No API Key Required)
* 🌙 Clean & Responsive UI

---

# 🏗 System Architecture

```mermaid
flowchart LR

Candidate([👨 Candidate])

Frontend["🌐 Frontend<br/>HTML • CSS • JavaScript"]

Backend["⚡ FastAPI Backend"]

AI["🤖 OpenAI API<br/>or Demo AI Engine"]

Database[(🗄 SQLite)]

Candidate --> Frontend
Frontend --> Backend
Backend --> AI
Backend --> Database
AI --> Backend
Database --> Backend
Backend --> Frontend
Frontend --> Candidate
```

---

# 🎯 Interview Workflow

```mermaid
flowchart TD

Start([🚀 Start])

Start --> Login

Login --> Dashboard

Dashboard --> SelectRole

SelectRole --> GenerateQuestion

GenerateQuestion --> CandidateAnswer

CandidateAnswer --> AIReview

AIReview --> Feedback

Feedback --> Score

Score --> Dashboard

Dashboard --> InterviewHistory
```

---

# 📄 Resume Match Workflow

```mermaid
flowchart LR

Resume["📄 Resume"]

Job["💼 Job Description"]

Parser["📑 Resume Parser"]

AI["🤖 AI Analyzer"]

Resume --> Parser

Job --> Parser

Parser --> AI

AI --> ATS["📊 ATS Score"]

AI --> Skills["🧠 Skill Gap"]

AI --> Suggestions["✍ Improvement Suggestions"]

AI --> Interview["🎯 Interview Questions"]
```

---

# 💻 Tech Stack

### Frontend

* HTML5
* CSS3
* JavaScript

### Backend

* FastAPI
* Python

### AI

* OpenAI Responses API
* Prompt Engineering
* AI Feedback Engine

### Database

* SQLite

---

# 📂 Project Structure

```text
InterviewIQ-AI/

├── backend/
│   ├── app/
│   │   ├── services/
│   │   ├── static/
│   │   ├── models.py
│   │   ├── main.py
│   │
│   ├── requirements.txt
│   ├── .env.example
│
├── README.md
```

---

# 🌟 Why InterviewIQ AI?

✅ Simulates real interview scenarios

✅ AI-powered resume evaluation

✅ Generates personalized interview questions

✅ ATS-style resume scoring

✅ Works with or without an OpenAI API key

✅ Built using production-ready FastAPI architecture

---

# 🚀 Future Roadmap

* 🎙 Voice-Based Interviews
* 🎥 Webcam Mock Interviews
* 📈 Performance Analytics
* 📄 AI Resume Builder
* 🌍 Multi-Language Support
* 📱 Mobile Application
* 🤖 AI Career Coach

---

<p align="center">

## ⭐ If you like this project, consider giving it a Star!

**Practice • Improve • Succeed 🚀**

</p>
