import streamlit as st
from textblob import TextBlob
import spacy
import speech_recognition as sr
# import ollama

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

# Dictionary of topics and their associated questions
interview_questions = {
    "Python": [
        "What are the key features of Python?",
        "Explain the difference between lists and tuples in Python.",
        "How does memory management work in Python?",
        "What is the GIL in Python?",
        "Explain the use of decorators in Python."
    ],
    "Data Structures": [
        "What is the difference between a stack and a queue?",
        "Explain the concept of a binary search tree.",
        "What is a hash table and how does it work?",
        "Describe the time complexity of common sorting algorithms.",
        "What is the difference between a linked list and an array?"
    ],
    "Machine Learning": [
        "What is the difference between supervised and unsupervised learning?",
        "Explain the concept of overfitting and how to prevent it.",
        "What is the difference between classification and regression?",
        "Describe the k-means clustering algorithm.",
        "What is the purpose of cross-validation in machine learning?"
    ],
    "Web Development": [
        "What is the difference between GET and POST HTTP methods?",
        "Explain the concept of RESTful APIs.",
        "What is CORS and why is it important?",
        "Describe the differences between SQL and NoSQL databases.",
        "What are the key principles of responsive web design?"
    ]
}

def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    if sentiment > 0.1:
        return 'positive'
    elif sentiment < -0.1:
        return 'negative'
    else:
        return 'neutral'

def extract_key_phrases(text):
    doc = nlp(text)
    key_phrases = [chunk.text for chunk in doc.noun_chunks if len(chunk.text.split()) > 1]
    return key_phrases[:5]

def assess_quality(sentiment, key_phrases, text_length):
    if sentiment == 'positive' and len(key_phrases) >= 3 and text_length > 100:
        return 'high'
    elif sentiment == 'negative' and len(key_phrases) < 2 and text_length < 50:
        return 'low'
    else:
        return 'medium'

def speech_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Speak now...")
        audio = r.listen(source)
        st.write("Processing speech...")
    
    try:
        text = r.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        st.error("Sorry, I couldn't understand the audio.")
        return None
    except sr.RequestError:
        st.error("Sorry, there was an error connecting to the speech recognition service.")
        return None

st.title("Interview Responses Analysis")
st.write("This app analyzes the sentiment, key phrases, and overall quality of interview responses.")

# Topic input and question selection
selected_topic = st.selectbox("Select a topic:", list(interview_questions.keys()))
st.session_state.questions = interview_questions[selected_topic]

# Question selection
if 'questions' in st.session_state:
    selected_question = st.selectbox("Select a question:", st.session_state.questions)
    st.write("Selected question:", selected_question)

# Input method selection
input_method = st.radio("Choose input method:", ("Upload File", "Enter Text", "Speech Input"))

responses = []

if input_method == "Upload File":
    uploaded_file = st.file_uploader("Upload a text file with interview responses", type="txt")
    if uploaded_file:
        responses = uploaded_file.read().decode("utf-8").strip().split('\n\n')
elif input_method == "Enter Text":
    input_text = st.text_area("Enter your response here:")
    if input_text:
        responses = [input_text]
else:  # Speech Input
    if st.button("Start Speech Recognition"):
        speech_text = speech_to_text()
        if speech_text:
            st.write("Recognized text:", speech_text)
            responses = [speech_text]

if responses:
    analysis_results = []
    for response in responses:
        sentiment = analyze_sentiment(response)
        key_phrases = extract_key_phrases(response)
        quality = assess_quality(sentiment, key_phrases, len(response))
        analysis_results.append({
            'response': response,
            'sentiment': sentiment,
            'key_phrases': key_phrases,
            'quality': quality
        })
    
    for i, result in enumerate(analysis_results, 1):
        st.header(f"Response {i}")
        st.write(result['response'])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader("Sentiment")
            st.write(result['sentiment'])
        with col2:
            st.subheader("Key Phrases")
            st.write(", ".join(result['key_phrases']))
        with col3:
            st.subheader("Overall Quality")
            st.write(result['quality'])
        
        st.markdown("---")
else:
    st.write("Please provide a response to analyze.")