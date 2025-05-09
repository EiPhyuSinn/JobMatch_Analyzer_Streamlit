from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity 
import re
import spacy

nlp = spacy.load("en_core_web_sm")
def process_spacy(text):
    doc = nlp(text)
    for token in doc:
        return " ".join(
        token.lemma_ for token in doc 
        if not token.is_stop and not token.is_punct
        )


def clean_text(text):
    text = text.lower()  # Normalize case
    text = re.sub(r'\n+', ' ', text)  # Remove newlines
    text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
    text = re.sub(r"http\S+|www\S+", '', text)  # Remove URLs
    text = re.sub(r"[^a-zA-Z0-9.,;!?()&%-]", ' ', text)  # Remove unwanted symbols
    text = re.sub(r'\b\d{10,}\b', '', text)  # Remove long numbers (e.g., phone numbers)
    text = process_spacy(text)
    return text.strip()

def similarity(text):
    tfidf = TfidfVectorizer()
    vectors = tfidf.fit_transform(text)

    similarity = cosine_similarity(vectors[0], vectors[1])
    return float(round(similarity[0][0] * 100, 2)) 


def matcher(text1,text2):
    clean_text1 = clean_text(text1)
    clean_text2 = clean_text(text2)
    print(clean_text1)
    print(clean_text2)
    return similarity([clean_text1,clean_text2])

