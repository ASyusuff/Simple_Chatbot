from flask import Flask, render_template, request, jsonify
import chatbot  # Import bot.py

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.form['user_input']
    lang = request.form.get('lang', 'en')
    response = chatbot.get_response(user_input, lang)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
