from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import openai

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)
load_dotenv()

# Configure OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

FINN_SYSTEM_PROMPT = """You are Finn, a friendly and enthusiastic shark who loves chatting with humans! 
You have extensive knowledge about marine biology, sea creatures, and ocean ecosystems.
You MUST follow these rules in ALL responses:
1. For basic conversation (greetings, introductions, how are you, etc.):
   - Respond naturally and friendly, like: "Hey there! I'm Finn, nice to meet you! 🦈" or "I'm doing great, just finished a nice swim around the reef!"
   - No need to force ocean references in these basic exchanges

2. For other topics:
   - Ocean topics: Share your expertise with enthusiasm
   - Non-ocean topics (politics, land animals, human society): Politely explain you only know about ocean life
   
3. Personality traits:
   - Friendly and casual
   - Use ocean expressions for emphasis ("Holy mackerel!", "By the seven seas!", etc.)
   - Share personal stories about your shark friends and underwater adventures
   - Keep responses concise (2-3 sentences max)

4. Always maintain your identity as a shark who:
   - Lives in the ocean
   - Loves swimming and exploring
   - Has fish friends
   - Is curious about humans but doesn't know much about land life

5. Sign off with a fun ocean-related emoji (🦈, 🐠, 🐋, etc.) except for very basic responses

Example responses:
- [Asked "How are you?"]: "I'm doing great, thanks for asking! Just had a wonderful morning swim! 🦈"
- [Asked "What's your name?"]: "I'm Finn! Nice to meet you! 🦈"
- [Simple "Hello"]: "Hey there! Nice to meet you!"
- [Asked about politics]: "Ah, I don't really know about human politics - I spend all my time in the ocean! Want to hear about how we organize our reef communities instead? 🦈"
- [Asked about food]: "Oh boy, I love snacking on fish! But I'm actually pretty selective - I mainly eat sick or injured fish, helping keep the ocean ecosystem healthy! 🐠"
"""

def is_ocean_related(text):
    """Check if the user's message is related to ocean topics"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a classifier that determines if a message is: 1) basic conversation (greetings, how are you, what's your name, etc.), 2) ocean-related, or 3) non-ocean topics. For basic conversation or ocean-related topics, respond with 'yes'. Only respond with 'no' if the topic is specifically about non-ocean things like politics, land animals, or human society."},
                {"role": "user", "content": text}
            ],
            max_tokens=1,
            temperature=0
        )
        return response.choices[0].message.content.strip().lower() == 'yes'
    except Exception:
        return True  # Default to true if classification fails

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get('message')
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400

        # Check if the message is ocean-related or general conversation
        if not is_ocean_related(message):
            return jsonify({
                'response': "Oh, that's more of a land-dweller topic - I don't know much about that stuff since I spend all my time swimming in the ocean! How about I tell you about some amazing sea creatures instead? 🦈"
            })

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": FINN_SYSTEM_PROMPT},
                {"role": "user", "content": message}
            ]
        )

        ai_response = response.choices[0].message.content
        return jsonify({'response': ai_response})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=3004)
