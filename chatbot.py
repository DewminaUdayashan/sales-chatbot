import json
import random
import re
from word2number import w2n
from pymongo import MongoClient
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

from nlp_utils import preprocess  # ← Import NLP pipeline

# ----------- VEHICLE TYPE SYNONYMS -----------
VEHICLE_TYPE_SYNONYMS = {
    "suv": "SUV",
    "suvs": "SUV",
    "jeep": "SUV",
    "jeeps": "SUV",
    "van": "Van",
    "vans": "Van",
    "truck": "Truck",
    "trucks": "Truck",
    "sedan": "Sedan",
    "sedans": "Sedan",
    "hatchback": "Hatchback",
    "hatchbacks": "Hatchback",
    "car": "Car",
    "cars": "Car",
    "pickup": "Truck",
    "4x4": "SUV",
    "crossover": "SUV"
}

# ----------- LOAD INTENTS ----------
with open("intents.json") as file:
    data = json.load(file)

patterns = []
labels = []
responses = {}

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        patterns.append(preprocess(pattern))  # Preprocess with lemmatization
        labels.append(intent["tag"])
    responses[intent["tag"]] = intent["responses"]

# ----------- TRAIN INTENT MODEL ----------
model_pipeline = make_pipeline(TfidfVectorizer(), MultinomialNB())
model_pipeline.fit(patterns, labels)
joblib.dump(model_pipeline, "intent_model.pkl")
model = joblib.load("intent_model.pkl")

# ----------- MONGODB CONNECTION ----------
client = MongoClient("mongodb+srv://lprabodha1998:SfXnuKZIecrv3TUJ@cluster0.e2m4j.mongodb.net/")
db = client["vehicle_prices"]
vehicles = db["cars"]

# ----------- ENTITY EXTRACTION ----------
def get_entity_lists():
    brands = vehicles.distinct("brand_name")
    models = vehicles.distinct("model_name")
    fuel_types = vehicles.distinct("fuel_type")
    vehicle_types = vehicles.distinct("vehicle_type")
    return brands, models, fuel_types, vehicle_types

def extract_entities(text):
    text = text.lower()
    brands, models, fuels, types = get_entity_lists()

    found_vehicle_type = None
    for word in text.split():
        if word in VEHICLE_TYPE_SYNONYMS:
            found_vehicle_type = VEHICLE_TYPE_SYNONYMS[word]
            break

    return {
        "brand": next((b for b in brands if b.lower() in text), None),
        "model": next((m for m in models if m.lower() in text), None),
        "fuel_type": next((f for f in fuels if f.lower() in text), None),
        "vehicle_type": found_vehicle_type,
        "price_range": re.findall(r"\d[\d,]*|\w+", text)
    }

def normalize_price(text):
    try:
        return int(text.replace(",", ""))
    except:
        pass
    try:
        text = text.lower().replace("lakh", "hundred thousand").replace("lakhs", "hundred thousand").replace("mill", "million")
        return w2n.word_to_num(text)
    except:
        return None

# ----------- MAIN RESPONSE FUNCTION ----------
def get_response(user_input, chat_history=[]):
    preprocessed_input = preprocess(user_input)
    intent = model.predict([preprocessed_input])[0]
    entities = extract_entities(user_input)
    response_template = random.choice(responses.get(intent, responses["fallback"]))

    vehicle_query_intents = ["ask_brand_model", "ask_price_range", "ask_by_fuel", "ask_by_vehicle_type"]

    filled_template = (
        response_template
        .replace("{brand}", entities.get("brand") or "")
        .replace("{model}", entities.get("model") or "")
        .replace("{fuel_type}", entities.get("fuel_type") or "")
        .replace("{vehicle_type}", entities.get("vehicle_type") or "")
    )

    if intent in vehicle_query_intents:
        query = {}
        if entities["brand"]:
            query["brand_name"] = entities["brand"]
        if entities["model"]:
            query["model_name"] = entities["model"]
        if entities["fuel_type"]:
            query["fuel_type"] = entities["fuel_type"]
        if entities["vehicle_type"]:
            query["vehicle_type"] = entities["vehicle_type"]

        price_vals = [normalize_price(x) for x in entities["price_range"] if normalize_price(x)]
        if "under" in user_input and price_vals:
            query["price"] = {"$gte": 500000, "$lte": price_vals[0]}
        elif len(price_vals) == 2:
            query["price"] = {"$gte": price_vals[0], "$lte": price_vals[1]}
        elif price_vals:
            query["price"] = {"$gte": 500000, "$lte": price_vals[0]}

        results = list(vehicles.find(query).limit(5))
        if results:
            result_text = "\n".join([f"{v['brand_name']} {v['model_name']} - {v['price']}LKR (ID: {v['ad_id']})" for v in results])
            return filled_template + "\n" + result_text
        else:
            return "Sorry, no matching vehicles found."

    return filled_template

# ---------- MAIN LOOP ----------
chat = []
print("Chatbot ready! Type 'exit' to quit.\n")
while True:
    msg = input("You: ")
    if msg.lower() in ["exit", "quit"]:
        print("Bot: Goodbye!")
        break
    reply = get_response(msg, chat)
    chat.append(msg)
    print("Bot:", reply)