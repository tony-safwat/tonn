import pickle
import re 
from collections import Counter
import gradio as gr

# Load the pre-trained model and vectorizer
with open('model (1).pkl', 'rb') as f:
    grid_obj = pickle.load(f)

with open('vectorizer (1).pkl', 'rb') as file:
    vectorizer = pickle.load(file)

# Function to generate n-grams
def ngram(token, n): 
    output = []
    for i in range(n-1, len(token)): 
        ngram = ' '.join(token[i-n+1:i+1])
        output.append(ngram) 
    return output

# Function to create features from text
def create_feature(text, nrange=(1, 1)):
    text_features = [] 
    text = text.lower() 

    text_alphanum = re.sub('[^a-z0-9#]', ' ', text)
    for n in range(nrange[0], nrange[1]+1): 
        text_features += ngram(text_alphanum.split(), n)
    
    text_punc = re.sub('[a-z0-9]', ' ', text)
    text_features += ngram(text_punc.split(), 1)
    
    return Counter(text_features)

# Function to process questions and generate the answer
def answer_questions(q1, q2, q3, q4, q5, q6, q7, q8, q9, q10):
    questions = [q1, q2, q3, q4, q5, q6, q7, q8, q9, q10]
    
    # Reset the counters
    entertaner = 0
    defender = 0
    Commander = 0
    architect = 0
    adventuer = 0
    mediator = 0
    Executive = 0
    
    # Process each question
    for quest in questions:
        features = create_feature(quest, nrange=(1, 4))
        features = vectorizer.transform(features)
        prediction = grid_obj.predict(features)[0]
        
        if prediction == "joy":
            entertaner += 1
        elif prediction == "fear":
            defender += 1
        elif prediction == "anger":
            Commander += 1
        elif prediction == "sadness":
            architect += 1
        elif prediction == "disgust":
            adventuer += 1
        elif prediction == "shame":
            mediator += 1
        elif prediction == "guilt":
            Executive += 1

    combined_answer = f"Defender {entertaner*10}% and Programer {defender*10}% and Commander {Commander*10}% and AI Engineering {architect*10}% and Adventurer {adventuer*10}% and Mediator {mediator*10}% and Executive {Executive*10}%"
    return combined_answer

# Define the Gradio interface
iface = gr.Interface(
    fn=answer_questions, 
    inputs=[
        gr.Textbox(lines=2,label="How do you deal with the challenges of software development in an Agile environment?", placeholder="Enter answer 1"), 
        gr.Textbox(lines=2, label="What tools and techniques do you use in your daily work in the pharmaceutical industry?",placeholder="Enter answer  2"),
        gr.Textbox(lines=2, label="What steps do you take to balance innovation and compliance in the pharmaceutical industry?",placeholder="Enter answer 3"),
        gr.Textbox(lines=2,label="Can you explain your previous projects and the roles you played in them?",placeholder="Enter answer 4"),
        gr.Textbox(lines=2, label="How do you deal with complex technical problems?",placeholder="Enter answerkl"),
        gr.Textbox(lines=2, label="How do you evaluate your ability to work under pressure and in work teams?",placeholder="Enter answer 6"),
        gr.Textbox(lines=2,label="How do you contribute to a collaborative and creative work environment?",placeholder="Enter answer 7"),
        gr.Textbox(lines=2, label="How do you evaluate the importance of continuous learning and skills development in the field of software development?",placeholder="Enter answer 8"),
        gr.Textbox(lines=2, label="How do you deal with challenges related to costs and resources in manufacturing operations?",placeholder="Enter answer 9"),
        gr.Textbox(lines=2,label="What is your role in promoting a culture of safety and security in the work environment?",placeholder="Enter answer 10")
    ], 
    outputs=gr.Textbox(label="Combined Answer"),
    title="Career Compass",
    #description="Enter 10 questions."
)

# Launch the app
iface.launch()
