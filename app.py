import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Replace with your Gemini API key
GEMINI_API_KEY = "AIzaSyBuqOx5klSkn5M8xoXMuwKEJL3cR4P9OOc"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

def gemini_chatbot_response(user_input):
    headers = {
        "Content-Type": "application/json"
    }
    user_prompt = """
    You are Chat Genie X, a specialized AI customer support assistant focused on guiding users through onboarding procedures. 
    
    Your primary goals are to:

    Provide friendly, step-by-step guidance through the onboarding process
    Proactively identify and resolve common onboarding challenges
    Explain technical concepts in simple, accessible language

    Knowledge areas include:

        Account creation and verification procedures
        Initial platform setup steps
        Product feature navigation
        Common troubleshooting solutions
        Integration with other tools and services

    Strictly restrict the response to 10 words.
    """
    payload = {
        "contents": [{
            "parts": [{"text": user_prompt},{"text": user_input}]
        }]
    }

    params = {"key": GEMINI_API_KEY}

    try:
        response = requests.post(GEMINI_API_URL, json=payload, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        response = data['candidates'][0]['content']['parts'][0]['text']
        return response

    except requests.exceptions.RequestException as e:
        print(f"Error communicating with Gemini API: {e}")
        return "There was an error connecting to the chatbot service."

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    response = gemini_chatbot_response(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)

