# Interview Response Analysis Application

A Streamlit application that analyzes interview responses using natural language processing and sentiment analysis.

## Features

- Topic-based interview questions
- Multiple input methods (text, file upload, speech)
- Sentiment analysis
- Key phrase extraction
- Response quality assessment

## Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd <repository-name>
```

2. Install requirements:
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

3. Run the application:
```bash
streamlit run app.py
```

## Usage

1. Select an interview topic
2. Choose a specific question
3. Input your response using one of three methods:
   - Text input
   - File upload
   - Speech input
4. View the analysis results including:
   - Sentiment analysis
   - Key phrases
   - Overall response quality

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

MIT
