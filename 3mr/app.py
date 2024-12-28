from flask import Flask, render_template, request, jsonify
import random
import pickle
import re
from sklearn.feature_extraction.text import CountVectorizer

app = Flask(__name__)

# Load the pre-trained model and vectorizer
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

# List of interview questions
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
    "Describe a time when you had to adapt to a significant change in your work environment. How did you handle it?",
    "Can you provide an example of a situation where you quickly adjusted your approach or priorities in response to unexpected circumstances?",
    "How do you stay calm and composed when faced with sudden changes or challenges in your work?",
    "Tell me about a time when you successfully learned a new skill or adapted to a new technology or software.",
    "Describe a project where you had to work with a new team or in a different department.",
    "Can you describe a time when you identified a major problem in your work and how you approached solving it?",
    "What steps do you take to understand and analyze a complex problem before developing a solution?",
    "How do you prioritize problems when you have multiple issues to address at the same time?",
    "Can you give an example of a creative solution you developed for a challenging problem?",
    "Describe a situation where you had to solve a problem under a tight deadline. How did you manage it?"
]

# Function to create features from text using n-grams
def create_feature(text, nrange=(1, 1)):
    text_features = []
    text = text.lower()
    text_alphanum = re.sub('[^a-z0-9#]', ' ', text)
    for n in range(nrange[0], nrange[1] + 1):
        text_features += ngram(text_alphanum.split(), n)
    text_punc = re.sub('[a-z0-9]', ' ', text)
    text_features += ngram(text_punc.split(), 1)
    return ' '.join(text_features)

# Function to create n-grams
def ngram(token, n):
    output = []
    for i in range(n - 1, len(token)):
        ngram = ' '.join(token[i - n + 1:i + 1])
        output.append(ngram)
    return output

# Route for the homepage, renders a random set of questions
@app.route('/')
def index():
    selected_questions = random.sample(questions, 10)  # Select 10 random questions
    return render_template('index.html', questions=selected_questions)

# Route for submitting answers
@app.route('/submit', methods=['POST'])
def submit():
    user_answers = request.form.to_dict()  # Get form data as dictionary
    answers_text = " ".join(user_answers.values())  # Combine answers into a single text
    features = create_feature(answers_text, nrange=(1, 4))  # Create features from the answers
    vectorized_features = vectorizer.transform([features])  # Vectorize the features
    prediction = model.predict(vectorized_features)[0]  # Get the prediction
    return jsonify({'prediction': prediction})  # Return the prediction as JSON

if __name__ == '__main__':
    app.run(debug=True, port=7860)
