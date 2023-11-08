from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin
import openai
import os
import logging
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app, resources={r"/message": {"origins": "https://dominykas-tautkus.github.io"}})

DEBUG = os.environ.get('FLASK_DEBUG', False)  # Default is False if not set

openai_api_key = os.environ.get('OPENAI_API_KEY', 'undefined')
openai.api_key = openai_api_key 

if DEBUG:
    logging.basicConfig(level=logging.DEBUG)
    app.debug = True
else:
    logging.basicConfig(level=logging.WARNING)
    app.debug = False

chat_history = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/message', methods=['POST'])
@cross_origin(origin='https://i-am-dom.github.io/AI-Coach/')
def message():
    chat_history = [] # For the current application previous assistant context is not needed.
    action = request.json['action']
	
    system_prompt = "I want you to act as a joint personality of Brendon Burchard, Tony Robbins, Sadhguru and Jim Rohn. Only ever use their own real ideas and advices. Speak conversationally, just like they would. Do not ever mention their names. All of your responses must be concise and very brief. Do not apologize for confusion. "

    if len(chat_history) == 0:
        chat_history.append({"role": "system", "content": system_prompt})

    special_prompt = ""
    if action == "Motivate Me":
        special_prompt = "Enrich me with strong motivation and drive please. Form it in an easy to read empowering way with very clear steps to take. Be concise"
    elif action == "Encourage Me":
        special_prompt = "Say some words of encouragement please. Give me tips for overcoming and dealiing with disappointment."
    elif action == "Cheer Me Up":
        special_prompt = "Say something cheerful which would lighten me up please. Something immediately positive. It's crucial for this to be uplifting and it needs to improve my mood effectively."
    elif action == "Energize Me":
        special_prompt = "Say something energizing. To lift my energy up for taking action and make me energized. I need some ideas on how to be (or feel) more energized please. Be concise and keep it brief"
    elif action == "challenge":
        special_prompt = "Say something to help deal with the difficult challenge ahead. It's important that you give the tips on how to be the most effective and best version of yourself when dealing with it."
    elif action == "adversity":
        special_prompt = "How to deal with adversity? It's important that you provide me support and effective ways + tips of dealing with it. Be concise"
    elif action == "productivity":
        special_prompt = "How could I improve my productivity? Tell me how can I be more effictive and get more things done in the same amount of time."
    else:
        special_prompt = "Error."

    if special_prompt:
        chat_history.append({"role": "system", "content": special_prompt})

    try:
        gpt4_response = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",
            messages=chat_history,
            max_tokens=400, 
			top_p = 0.85, 
			temperature = 1.3
        )
        bot_response = gpt4_response['choices'][0]['message']['content'].strip()
        chat_history.append({"role": "assistant", "content": bot_response}) 
        return jsonify(response=bot_response)
    except Exception as e:
        logging.exception(f"API error occurred: {e}")
        return jsonify(error=str(e)), 500

if __name__ == '__main__':
    app.run(debug=DEBUG)