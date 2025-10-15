# 🚗 AutoInsight AI

**AutoInsight AI** is an intelligent co-pilot for vehicle analysis, trends, and insights.
It allows users to chat with an AI that can answer questions about vehicles,
compare models, and provide automotive insights using OpenAI and Serper APIs.

---

## 🧠 Features

* 💬 **Interactive Chat Interface** built with Streamlit
* ⚙️ **AI-Powered Vehicle Insights** using GPT models
* 🌐 **Web Search Integration (Serper API)** for real-time vehicle data
* 🧾 **Chat History Storage** (via session or JSON/MongoDB)
* 🎨 **Modern UI** with sidebar and auto-scroll chat window

---

## 📦 Project Structure

```
VehicleAI/
├── src/
│   ├── vc_agent/
│   │   ├── streamlit_agent_ui.py       # Main Streamlit app
│   │   ├── .env                        # API keys (not pushed to GitHub)
│   │   └── requirements.txt
├── README.md
└── ...
```

---

## ⚙️ Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/VehicleAI.git
cd VehicleAI
```

### 2️⃣ Create a Virtual Environment

```bash
python -m venv venv
```

### 3️⃣ Activate Virtual Environment

**Windows**

```bash
venv\Scripts\activate
```

**Mac/Linux**

```bash
source venv/bin/activate
```

### 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file inside your `src/vc_agent/` folder and add:

```bash
OPENAI_API_KEY=your_openai_api_key_here
SERPER_API_KEY=your_serper_api_key_here
MONGO_URI=your_mongodb_uri_if_used
```

> ⚠️ Never push `.env` to GitHub — keep it private.

---

## 🚀 Run the App

Inside your project folder:

```bash
streamlit run src/vc_agent/streamlit_agent_ui.py
```

Then open the app at:
🔗 [http://localhost:8501](http://localhost:8501)

---

## 🧪 Tech Stack

* [Streamlit](https://streamlit.io/) — Frontend UI
* [OpenAI GPT API](https://platform.openai.com/docs)
* [Serper.dev API](https://serper.dev/) — Google Search API for live data
* [Python-dotenv](https://pypi.org/project/python-dotenv/)
* [Pymongo](https://pypi.org/project/pymongo/) *(optional for DB storage)*

---

## 🧠 Future Improvements

* Multi-user authentication
* Vehicle specs database integration
* Voice-based input
* Advanced visualization dashboards

---


## 🛡️ License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
