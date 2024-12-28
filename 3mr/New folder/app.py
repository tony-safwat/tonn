
from flask import Flask, render_template, request, jsonify
import random
import pickle
import re
from sklearn.feature_extraction.text import CountVectorizer

app = Flask(__name__)

# Load the pre-trained model and vectorizer
with open('model (1).pkl', 'rb') as f:
    model = pickle.load(f)

with open('vectorizer (1).pkl', 'rb') as f:
    vectorizer = pickle.load(f)

questions = [
    "Can you describe a time when your attention to detail helped you identify and correct a mistake before it became a significant issue?",
    "How do you ensure accuracy and precision in your work, especially when dealing with complex tasks or large amounts of data?",
    "Can you give an example of a project where paying attention to small details made a significant difference in the outcome?",
    "Describe your process for double-checking your work to ensure there are no errors or oversights.",
    "How do you handle situations where you notice inconsistencies or discrepancies in information or data?",
    "Tell me about a time when your attention to detail helped you catch a potential problem that others had overlooked.",
    "Can you tell me about a situation where you analyzed a complex problem and arrived at an innovative solution? How did you do that?",
    "How do you assess the credibility of the information you rely on when making decisions?",
    "How do you deal with conflicting or incomplete information when trying to solve a problem?",
    "What steps do you take to evaluate the quality of your work or project results?",
]

def create_feature(text, nrange=(1, 1)):
    text_features = []
    text = text.lower()
    text_alphanum = re.sub('[^a-z0-9#]', ' ', text)
    for n in range(nrange[0], nrange[1]+1):
        text_features += ngram(text_alphanum.split(), n)
    text_punc = re.sub('[a-z0-9]', ' ', text)
    text_features += ngram(text_punc.split(), 1)
    return ' '.join(text_features)

def ngram(token, n):
    output = []
    for i in range(n-1, len(token)):
        ngram = ' '.join(token[i-n+1:i+1])
        output.append(ngram)
    return output

@app.route('/')
def index():
    selected_questions = random.sample(questions, 10)
    return render_template('index.html', questions=selected_questions)

@app.route('/submit', methods=['POST'])
def submit():
    user_answers = request.form.to_dict()
    answers_text = " ".join(user_answers.values())
    features = create_feature(answers_text, nrange=(1, 4))
    vectorized_features = vectorizer.transform([features])
    prediction = model.predict(vectorized_features)[0]
    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    app.run(debug=True)