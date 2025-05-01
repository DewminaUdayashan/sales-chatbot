
# 🚗 Auto Sales Chatbot (NLP-Powered)

This chatbot is designed to assist users in searching for vehicles using natural language. It supports queries like:

- "I'm looking for a BMW X5"
- "Show me SUVs under 5 million"
- "Do you have diesel cars?"
- "Can I lease a car?"

It uses machine learning for intent classification, NLP preprocessing for smarter matching, and MongoDB for real-time vehicle data.

---

## 🧠 Features

- 🔍 **Intent Recognition** using `TfidfVectorizer` + `Naive Bayes`
- 🧠 **NLP Preprocessing** (tokenization, stopword removal, lemmatization)
- 🔄 **Synonym-aware vehicle type matching** (e.g., "jeep" → "SUV")
- ⚡ **Real-time MongoDB integration** for vehicle listings
- 💬 **Text-based interactive console interface**
- 📚 Modular code with `chatbot.py` and `nlp_utils.py`

---

## ⚙️ Technologies Used

- Python 3.8+
- NLTK
- scikit-learn
- pymongo
- word2number

---

## 📁 Project Structure

```
auto_sales_chatbot/
├── chatbot.py         # Main application logic
├── intents.json       # Training data with tags, patterns, responses
├── nlp_utils.py       # Preprocessing pipeline (lemmatization, synonyms)
├── requirements.txt   # Python dependencies
└── README.md          # Project documentation
```

---

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/auto-sales-chatbot.git
cd auto-sales-chatbot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install nltk scikit-learn joblib pymongo word2number
python -m nltk.downloader punkt stopwords wordnet omw-1.4
```

### 3. Prepare Your MongoDB

- Make sure your MongoDB instance is running.
- Ensure your `vehicle_prices.cars` collection contains data in the format:

```json
{
  "ad_id": "123ABC",
  "vehicle_name": "BMW X5",
  "brand_name": "BMW",
  "model_name": "X5",
  "vehicle_type": "SUV",
  "fuel_type": "Diesel",
  "price": 6500000,
  ...
}
```

- Update the MongoDB URI inside `chatbot.py` if needed.

### 4. Run the Chatbot

```bash
python chatbot.py
```

Then start chatting:

```
You: Show me electric cars
Bot: These are the vehicles with Electric engines:
...
```

Type `exit` or `quit` to stop.

---

## 🧪 Sample Intents

Here’s a snippet of `intents.json`:

```json
{
  "intents": [
    {
      "tag": "greet",
      "patterns": ["Hi", "Hello", "Hey there"],
      "responses": ["Hi, how can I assist you today?"]
    },
    {
      "tag": "ask_by_fuel",
      "patterns": ["Any diesel cars?", "I want electric vehicles"],
      "responses": ["These are the vehicles with {fuel_type} engines:"]
    }
  ]
}
```

---

## 🎓 Coursework Relevance

This chatbot meets the required architectural design:

- ✅ **Natural Language Interface** (text-based)
- ✅ **Inference Engine** (intent recognition + entity extraction)
- ✅ **Knowledge Base** (MongoDB-based, live data-driven)
- ✅ **ML Component** (learning from training data via `intents.json`)
- ✅ **Preprocessing** (NLP pipeline using NLTK and WordNet)

---

## 📩 Author

- **Lahiru Prabodha**
- **Dewmina Udayashan**
- NLP & AI Coursework Submission

---

## ✅ License

This project is for educational use only.
