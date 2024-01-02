from flask import Flask, jsonify, request

app = Flask(__name__)


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
                return jsonify({'reply': f"this is the answer to our question: {question}"})
            else:
                return jsonify({'error': 'No question field in the JSON data'}), 400
        else:
            return jsonify({'error': 'Invalid JSON data'}), 400


def get_answer(question):
    return f"this is the answer to our question: {question}"


if __name__ == '__main__':
    app.run(debug=True)
