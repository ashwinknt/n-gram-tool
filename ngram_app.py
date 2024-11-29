from flask import Flask, render_template, request
import nltk
from nltk.util import ngrams
from nltk.corpus import stopwords

# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Initialize Flask app
app = Flask(__name__)

# Function to generate filtered n-grams
def get_ngrams(text, n, keywords):
    # Tokenize the text
    words = nltk.word_tokenize(text.lower())
    # Generate n-grams
    n_grams = list(ngrams(words, n))
    # Get stop words
    stop_words = set(stopwords.words('english'))
    # Join n-grams to make them easily searchable
    n_grams_joined = [' '.join(gram) for gram in n_grams]
    # Filter out n-grams that contain stop words
    filtered_ngrams = [
        n_gram for n_gram in n_grams_joined
        if not any(word in stop_words for word in n_gram.split())
        and any(keyword.lower() in n_gram for keyword in keywords)
    ]
    return filtered_ngrams

# Home route for the web form
@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        # Get form data
        text = request.form.get('text')
        n = int(request.form.get('n'))
        keywords = request.form.get('keywords').split(',')
        
        # Generate n-grams
        result = get_ngrams(text, n, keywords)

    return render_template('index.html', result=result)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)