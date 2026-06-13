import pdfplumber
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

STOPWORDS = {
    "the", "and", "for", "with", "that", "this", "are", "you", "have",
    "will", "from", "they", "been", "were", "their", "looking", "strong",
    "experience", "knowledge", "skills", "required", "plus", "problem",
    "candidates", "should", "hands", "model", "deep", "machine", "learning",
    "generative", "computer", "vision", "rest", "apis", "familiarity"
}

def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def match_score(job_description, resume_text):
    vectorizer = TfidfVectorizer(ngram_range=(1,2))
    vectors = vectorizer.fit_transform([job_description, resume_text])
    score = cosine_similarity(vectors[0], vectors[1])[0][0]
    return round(score * 100, 2)

def get_missing_keywords(job_description, resume_text):
    job_words = set(job_description.lower().replace(',', '').replace('.', '').split())
    resume_words = set(resume_text.lower().split())
    missing = job_words - resume_words - STOPWORDS
    missing = [w for w in missing if len(w) > 3]
    return sorted(missing)[:10]