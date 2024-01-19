import os
import json
from openai import OpenAI
from flask import Flask, jsonify, request
import logging
from serpapi import GoogleSearch  # type: ignore
from typing import List, Dict, Any

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "")

logging.basicConfig(filename='flask.log', level=logging.DEBUG)

app.logger.debug('Starting application')

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))
serpapi_key = os.getenv("SERPAPI_KEY", "")


def get_answer(question):
    if os.path.getsize('knowledge_list.json') > 0:
        with open('knowledge_list.json', 'r') as f:
            knowledge_list = json.load(f)
    else:
        knowledge_list = []
    prompt = f"Shortly answer the question in polish. Use following info: {str(knowledge_list)}"
    api_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": question}
        ]
    )
    return api_response.choices[0].message.content or ""


def save_info(info):
    try:
        with open('knowledge_list.json', 'r') as f:
            file_content = f.read()
            if file_content:
                knowledge_list = json.loads(file_content)
            else:
                knowledge_list = []
    except FileNotFoundError:
        knowledge_list = []

    knowledge_list.append(info)

    with open('knowledge_list.json', 'w') as f:
        json.dump(knowledge_list, f)


def handle_conversation(query: str) -> Dict[str, Any]:
    function_descriptions: List[Dict[str, Any]] = [
                {
                    "name": "get_answer",
                    "description": "If it is a question",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "question": {
                                "type": "string",
                                "description": "question",
                            }
                        },
                        "required": ["question"]
                    },
                },
                {
                    "name": "save_info",
                    "description": "If it is any information",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "info": {
                                "type": "string",
                                "description": "info to save",
                            }
                        }
                    },
                    "required": ["info"]
                }
    ]

    response = client.chat.completions.create(
        model="gpt-4-0613",
        messages=[{"role": "user", "content": query}],
        functions=function_descriptions  # type: ignore
    )
    response_message = response.choices[0].message

    if response_message.function_call:
        return response_message.function_call  # type: ignore
    else:
        return response_message  # type: ignore


@app.route('/', methods=['GET', 'POST'])
def home():
    if (request.method == 'GET'):
        data = "hello world"
        return jsonify({'data': data})


@app.route('/answer', methods=['POST'])
def answer():
    if request.method == 'POST':
        data = request.get_json()
        if data is not None:
            question = data.get('question')
            if question is not None:
                fcall = handle_conversation(question)
                if fcall.name == "get_answer":
                    arguments = json.loads(fcall.arguments)
                    answer = get_answer(arguments["question"])
                    app.logger.info('Request: %s', request)
                    app.logger.info('Response: %s', jsonify({'reply': answer}))
                    with open('knowledge_list.json', 'w') as file:  # noqa
                        pass
                    return jsonify({'reply': answer})
                elif fcall.name == "save_info":
                    arguments = json.loads(fcall.arguments)
                    info = arguments["info"]
                    save_info(info)
                    app.logger.info('Request: %s', request)
                    app.logger.info('Response: %s', jsonify({'reply': 'OK, I get it'}))
                    return jsonify({'reply': 'OK, I get it'})
            else:
                return jsonify({'error': 'No question field in the JSON data'}), 400
        else:
            return jsonify({'error': 'Invalid JSON data'}), 400


def question_to_keywords(question):
    prompt = """Create a list of keywords that describes the question.
             It will be used for google search. Answer in polish"""
    api_response = client.chat.completions.create(
        model="gpt-4-0613",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": question}
        ]
    )
    keywords_message = api_response.choices[0].message.content or ""
    return keywords_message


@app.route('/google-answer', methods=['POST'])
def google_answer():
    if request.method == 'POST':
        data = request.get_json()
        if data is not None:
            question = data.get('question')
            if question is not None:
                keywords = question_to_keywords(question)
                params = {
                    "api_key": serpapi_key,
                    "engine": "google",
                    "q": keywords,
                    "google_domain": "google.pl",
                    "gl": "pl",
                    "hl": "pl"
                }
                search = GoogleSearch(params)
                result = search.get_dict()["organic_results"][0]["link"]
                json_result = json.dumps(result)
                app.logger.info('Request: %s', request)
                app.logger.info('Response: %s', json_result)
                return jsonify({'reply': result})


def md2html(input):
    prompt = "md2html"
    model_response = client.chat.completions.create(
        model="ft:gpt-3.5-turbo-1106:personal::8iqli9zY",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": input}
        ]
    )
    html = model_response.choices[0].message.content or ""
    return html


@app.route('/md2html', methods=['POST'])
def md2html_answer():
    if request.method == 'POST':
        data = request.get_json()
        if data is not None:
            question = data.get('question')
            if question is not None:
                html = md2html(question)
                app.logger.info('Request: %s', request)
                app.logger.info('Response: %s', html)
                return jsonify({'reply': html})


if __name__ == '__main__':
    app.run(debug=True)
