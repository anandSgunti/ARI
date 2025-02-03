from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = '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'

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests for frontend integration

@app.route("/chat", methods=["GET","POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    try:
        # OpenAI API Call
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an AI assistant answering questions about broken heart syndrome."},
                {"role": "user", "content": user_message}
            ]
        )

        reply = response["choices"][0]["message"]["content"]
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)  # Running on port 5000
