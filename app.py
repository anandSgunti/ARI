from flask import Flask, request, Response
from openai import OpenAI
from flask_cors import CORS  # Import CORS
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app) 

# Set up OpenAI API key (Ensure to set your API key in the environment variables)
client = OpenAI(api_key=os.getenv("OPEN_AI_KEY"))

# Chatbot logic using OpenAI GPT-4o-mini with streaming
def chatbot_response_stream(message: str):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Using GPT-4o-mini
            messages=[{"role": "system", "content": "text": "Provide concise and relevant answers to user queries within an AR application, ensuring that your responses maintain the immersive experience. Include clickable links if they are applicable and enhance the user's experience or understanding.\n\n# Guidelines\n\n- Keep responses brief and pertinent to the user's current context or query.\n- Wherever applicable, include clickable links that direct users to additional resources, ensuring they enhance the user's experience within the AR context.\n- Maintain a tone that is neutral and supportive, avoiding any disruption to the user's immersive experience.\n\n# Output Format\n\n- Responses should be concise, ideally limited to one or two sentences.\n- If including links, ensure they are formatted as clickable links.\n\n# Examples\n\n**Input:** \"What is the capital of France?\"\n\n**Output:** \"The capital of France is Paris. [Learn more here](https://en.wikipedia.org/wiki/Paris).\""},
                      {"role": "user", "content": message}],
            stream=True,  # Enable streaming
            
  temperature=1,
  max_completion_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
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
