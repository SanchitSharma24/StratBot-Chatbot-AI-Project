from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
print("Loaded API Key:", GEMINI_API_KEY)
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("models/gemini-1.5-pro")

# Flask app
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    print("User input:", user_input)

    if not user_input:
        return jsonify({"error": "No input provided."}), 400

    try:
        response = model.generate_content(user_input)
        clean_text = response.text.replace("**", "") 
        return jsonify({"response": clean_text})
    except Exception as e:
        print("Gemini Error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)




