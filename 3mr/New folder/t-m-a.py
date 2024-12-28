import pickle
import re
import time
import gradio as gr
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC

# Load the pre-trained model and vectorizer
with open('model (2).pkl', 'rb') as f:
    best_clf = pickle.load(f)

with open('vectorizer (2).pkl', 'rb') as file:
    vectorizer = pickle.load(file)

# Function to generate n-grams
def ngram(token, n):
    output = []
    for i in range(n - 1, len(token)):
        ngram = ' '.join(token[i - n + 1:i + 1])
        output.append(ngram)
    return output

# Function to create features from text
def create_feature(text, nrange=(1, 4)):
    text_features = []
    text = text.lower()

    # Treat alphanumeric characters as word tokens
    text_alphanum = re.sub('[^a-z0-9#]', ' ', text)
    for n in range(nrange[0], nrange[1] + 1):
        text_features += ngram(text_alphanum.split(), n)

    # Treat punctuations as word tokens
    text_punc = re.sub('[a-z0-9]', ' ', text)
    text_features += ngram(text_punc.split(), 1)

    return ' '.join(text_features)

# Function to process questions and generate the answer
def answer_questions(q1, q2, q3, q4, q5, q6, q7, q8, q9, q10):
    start_time = time.time()
    questions = [q1, q2, q3, q4, q5, q6, q7, q8, q9, q10]
    question_times = []

    # Check if any question is left unanswered
    if any(not q.strip() for q in questions):
        return "All questions marked with * are required. Please fill in all the fields."

    # Reset the counters
    categories = {
        "Attention to detail": 0,
        "Neglect of detail": 0,
        "Logical thinking": 0,
        "Illogical thinking": 0,
        "Adaptability": 0,
        "Inflexibility": 0,
        "Problem-solving": 0,
        "Problem-avoidance": 0
    }

    # Process each question
    for idx, quest in enumerate(questions, 1):
        features = create_feature(quest, nrange=(1, 4))
        features = vectorizer.transform([features])
        prediction = best_clf.predict(features)[0]
        question_time = time.time() - start_time
        question_times.append(f"Question {idx}: {question_time:.2f} seconds")
        
        if prediction in categories:
            categories[prediction] += 1

    # Convert counts to percentages
    total_questions = len(questions)
    percentages = {key: (value / total_questions) * 100 for key, value in categories.items()}
    
    combined_answer = (
        f"*Attention to detail {percentages['Attention to detail']:.1f}% and "
        f"*Neglect of detail {percentages['Neglect of detail']:.1f}% and "
        f"*Logical thinking {percentages['Logical thinking']:.1f}% and "
        f"*Illogical thinking {percentages['Illogical thinking']:.1f}% and "
        f"*Adaptability {percentages['Adaptability']:.1f}% and "
        f"*Inflexibility {percentages['Inflexibility']:.1f}% and "
        f"*Problem-solving {percentages['Problem-solving']:.1f}% and "
        f"*Problem-avoidance {percentages['Problem-avoidance']:.1f}%"
    )
    
    end_time = time.time()
    overall_time = end_time - start_time
    time_taken = "\n".join([f"Overall time taken to complete all questions: {overall_time:.2f} seconds"] + question_times)

    detailed_report = (
        "Detailed Report:\n"
        f"Attention to detail: {percentages['Attention to detail']:.1f}%\n"
        f"Neglect of detail: {percentages['Neglect of detail']:.1f}%\n"
        f"Logical thinking: {percentages['Logical thinking']:.1f}%\n"
        f"Illogical thinking: {percentages['Illogical thinking']:.1f}%\n"
        f"nAdaptability: {percentages['Adaptability']:.1f}%\n"
        f"Inflexibility: {percentages['Inflexibility']:.1f}%\n"
        f"Problem-solving: {percentages['Problem-solving']:.1f}%\n"
        f"Problem-avoidance: {percentages['Problem-avoidance']:.1f}%"
    )

    highest_skill = max(percentages, key=percentages.get)
    job_suggestions = []

    if highest_skill == 'Attention to detail':
        job_suggestions.append("Quality Manager (مدير الجودة): Suitable due to high attention to detail, adaptability, and problem-solving skills. [Job Description](link_to_job_description)")
        job_suggestions.append("Data Entry Specialist (أخصائي إدخال بيانات): Suitable due to meticulous attention to detail and accuracy. [Job Description](link_to_job_description)")
    elif highest_skill == 'Logical thinking':
        job_suggestions.append("Systems Analyst (محلل نظم): Suitable due to high logical thinking, problem-solving, and adaptability skills. [Job Description](link_to_job_description)")
        job_suggestions.append("Scientific Researcher (باحث علمي): Suitable due to")
        job_suggestions.append("Medical Representative (ممثل طبي): Suitable due to high logical thinking, problem-solving, and adaptability skills. [Job Description](link_to_job_description)")
        job_suggestions.append("Statistician (عالم إحصاءات): Suitable due to strong logical thinking and analytical skills. [Job Description](link_to_job_description)")
    elif highest_skill == 'Problem-solving':
        job_suggestions.append("IT Project Manager (مدير مشروعات تكنولوجيا المعلومات): Suitable due to high problem-solving, adaptability, and attention to detail skills. [Job Description](link_to_job_description)")
        job_suggestions.append("Clinical Data Analyst (محلل بيانات سريرية): Suitable due to high problem-solving, logical thinking, and attention to detail skills. [Job Description](link_to_job_description)")
        job_suggestions.append("Quality Manager (مدير الجودة): Suitable due to high problem-solving, adaptability, and attention to detail skills. [Job Description](link_to_job_description)")
        job_suggestions.append("Operations Research Analyst (محلل بحوث العمليات): Suitable due to strong problem-solving and analytical skills. [Job Description](link_to_job_description)")
    elif highest_skill == 'Adaptability':
        job_suggestions.append("Project Coordinator (منسق مشروع): Suitable due to high adaptability, communication, and problem-solving skills. [Job Description](link_to_job_description)")
        job_suggestions.append("Customer Success Manager (مدير نجاح العملاء): Suitable due to high adaptability, communication, and problem-solving skills. [Job Description](link_to_job_description)")
        job_suggestions.append("Sales Representative (ممثل مبيعات): Suitable due to high adaptability, communication, and problem-solving skills. [Job Description](link_to_job_description)")
    elif highest_skill == 'Illogical thinking':
        job_suggestions.append("Creative Director (مدير إبداعي): Suitable due to high creativity, innovative thinking, and problem-solving skills. [Job Description](link_to_job_description)")
        job_suggestions.append("UX/UI Designer (مصمم تجربة المستخدم/واجهة المستخدم): Suitable due to high creativity, design thinking, and problem-solving skills. [Job Description](link_to_job_description)")
        job_suggestions.append("Content Writer (كاتب محتوى): Suitable due to high creativity, writing skills, and problem-solving abilities. [Job Description](link_to_job_description)")
    elif highest_skill == 'Problem-avoidance':
        job_suggestions.append("Risk Manager (مدير المخاطر): Suitable due to strong risk assessment, problem-solving, and analytical skills. [Job Description](link_to_job_description)")
        job_suggestions.append("Compliance Officer (مسؤول الامتثال): Suitable due to strong regulatory knowledge, problem-solving, and analytical skills. [Job Description](link_to_job_description)")
        job_suggestions.append("Quality Assurance Specialist (متخصص ضمان الجودة): Suitable due to strong attention to detail, problem-solving, and analytical skills. [Job Description](link_to_job_description)")

    job_suggestions_text = "\n".join(job_suggestions)

    suitability_report = (
        f"Based on the analysis, you are suitable for the following jobs:\n"
        f"{job_suggestions_text}"
    )

    return combined_answer + "\n\n" + time_taken + "\n\n" + detailed_report + "\n\n" + suitability_report

# Define the Gradio interface
iface = gr.Interface(
    fn=answer_questions, 
    inputs=[
        gr.Textbox(lines=2, label="*Can you describe a time when your attention to detail helped you identify and correct a mistake before it became a significant issue?", placeholder="Enter answer 1"), 
        gr.Textbox(lines=2, label="*How do you ensure accuracy and precision in your work, especially when dealing with complex tasks or large amounts of data?", placeholder="Enter answer 2"),
        gr.Textbox(lines=2, label="*Can you give an example of a project where paying attention to small details made a significant difference in the outcome?", placeholder="Enter answer 3"),
        gr.Textbox(lines=2, label="*Describe your process for double-checking your work to ensure there are no errors or oversights?", placeholder="Enter answer 4"),
        gr.Textbox(lines=2, label="*How do you handle situations where you notice inconsistencies or discrepancies in information or data?", placeholder="Enter answer 5"),
        gr.Textbox(lines=2, label="*Tell me about a time when your attention to detail helped you catch a potential problem that others had overlooked.", placeholder="Enter answer 6"),
        gr.Textbox(lines=2, label="*Can you tell me about a situation where you analyzed a complex problem and arrived at an innovative solution? How did you do that?", placeholder="Enter answer 7"),
        gr.Textbox(lines=2, label="*How do you assess the credibility of the information you rely on when making decisions?", placeholder="Enter answer 8"),
        gr.Textbox(lines=2, label="*How do you deal with conflicting or incomplete information when trying to solve a problem?", placeholder="Enter answer 9"),
        gr.Textbox(lines=2, label="*What steps do you take to evaluate the quality of your work or project results?", placeholder="Enter answer 10")
    ],
    outputs=gr.Textbox(label="*Combined Answer"),
    title="Career Compass"
)

# Launch the app
iface.launch()