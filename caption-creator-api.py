from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv("OPENAI_API_KEY", "your_api_key_here")

@app.route('/')
def home():
    return "🪄 Caption Creator API is running!"

@app.route('/api/caption', methods=['GET'])
def generate_caption():
    prompt = request.args.get('prompt', '')
    if not prompt:
        return jsonify({"error": "Please provide a prompt, e.g. /api/caption?prompt=sunset over lake"}), 400

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }

    OR_ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
    
    tones = {
        "simple": "Write a simple, straightforward caption",
        "poetic": "Write a poetic, artistic caption with beautiful imagery",
        "funny": "Write a funny, humorous caption with a joke or pun",
        "aesthetic": "Write an aesthetic, trendy caption with emojis"
    }
    
    captions = {}
    
    for tone_name, tone_instruction in tones.items():
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a creative social media caption generator."},
                {"role": "user", "content": f"{tone_instruction} for: {prompt}. Keep it short and catchy."}
            ],
            "max_tokens": 60
        }
        
        response = requests.post(OR_ENDPOINT, headers=headers, json=data)
        
        if response.status_code != 200:
            captions[tone_name] = "Error generating caption"
        else:
            captions[tone_name] = response.json()['choices'][0]['message']['content'].strip()
    
    return jsonify({"prompt": prompt, "captions": captions})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
