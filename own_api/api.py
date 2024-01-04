import os
from openai import OpenAI
from flask import Flask, jsonify, request
import logging

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))

logging.basicConfig(filename='flask.log', level=logging.DEBUG)


def get_answer(question):
    prompt = "Shortly answer the question in polish"
    api_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": question}
        ]
    )
    return api_response.choices[0].message["content"]


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
                answer = get_answer(question)
                app.logger.info('Request: %s', request)
                app.logger.info('Response: %s', jsonify({'reply': answer}))
                return jsonify({'reply': answer})
            else:
                return jsonify({'error': 'No question field in the JSON data'}), 400
        else:
            return jsonify({'error': 'Invalid JSON data'}), 400


if __name__ == '__main__':
    app.run(debug=True)
