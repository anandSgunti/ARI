from flask import Flask, request, Response
from openai import OpenAI
import os

# Initialize Flask app
app = Flask(__name__)

# Set up OpenAI API key (Ensure to set your API key in the environment variables)
client = OpenAI(api_key=os.getenv("OPEN_AI_KEY"))

# Chatbot logic using OpenAI GPT-4o-mini with streaming
def chatbot_response_stream(message: str):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Using GPT-4o-mini
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": message}],
            stream=True  # Enable streaming
        )
        for chunk in response:
            if chunk.choices:
                yield chunk.choices[0].delta.content
    except Exception as e:
        yield f"Error: {str(e)}"

# Chatbot API endpoint with streaming
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        message = data.get("message", "")
        return Response(chatbot_response_stream(message), content_type='text/plain')
    except Exception as e:
        return Response(f"Error: {str(e)}", status=500, content_type='text/plain')

# Run using: python filename.py


# Run using: python filename.py
if __name__ == "__main__":
    app.run(debug=True, port=5000)  # Running on port 5000
