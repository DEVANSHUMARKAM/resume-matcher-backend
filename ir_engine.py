# backend/ir_engine.py

import os
import nltk
nltk.data.path.append('nltk_data')
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class SearchEngine:
    def __init__(self):
        # Initialize all the necessary components and data structures
        self.stemmer = nltk.stem.PorterStemmer()
        self.stopwords = set(nltk.corpus.stopwords.words('english'))

        self.vectorizer = TfidfVectorizer()
        self.resume_vectors = None
        self.resume_filenames = []
        self.filename_to_index = {}
        self.unstemmed_vocabulary = set()

    def _preprocess(self, text, stem=True):
        tokens = nltk.tokenize.word_tokenize(text.lower())
        filtered_tokens = [word for word in tokens if word.isalpha() and word not in self.stopwords]
        if stem:
            stemmed_tokens = [self.stemmer.stem(word) for word in filtered_tokens]
            return stemmed_tokens
        return filtered_tokens

    def load_and_index(self, resume_dir="resumes"):
        """Loads resumes from a directory and builds all necessary indexes."""
        self.resume_filenames = [f for f in os.listdir(resume_dir) if f.endswith(".txt")]
        self.filename_to_index = {name: i for i, name in enumerate(self.resume_filenames)}

        processed_resumes_for_tfidf = []
        all_unstemmed_words = []

        for filename in self.resume_filenames:
            with open(os.path.join(resume_dir, filename), 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                processed_resumes_for_tfidf.append(" ".join(self._preprocess(content, stem=True)))
                all_unstemmed_words.extend(self._preprocess(content, stem=False))

        if processed_resumes_for_tfidf:
            print(f"Indexing {len(processed_resumes_for_tfidf)} resumes for TF-IDF...")
            self.resume_vectors = self.vectorizer.fit_transform(processed_resumes_for_tfidf)
            print("TF-IDF Indexing complete!")

        self.unstemmed_vocabulary = set(all_unstemmed_words)
        print(f"Built unstemmed vocabulary with {len(self.unstemmed_vocabulary)} unique words.")

    def _get_ranked_results(self, similarities):
        top_indices = np.argsort(similarities)[-10:][::-1]
        return [{ "filename": self.resume_filenames[i], "score": round(float(similarities[i]), 4) } for i in top_indices if similarities[i] > 0]

    def search(self, query):
        if self.resume_vectors is None: return {"error": "No resumes indexed."}
        processed_query = " ".join(self._preprocess(query, stem=True))
        query_vector = self.vectorizer.transform([processed_query])
        cosine_similarities = cosine_similarity(query_vector, self.resume_vectors).flatten()
        return {"results": self._get_ranked_results(cosine_similarities)}

    def refine_search(self, original_query, relevant_docs):
        if not relevant_docs: return self.search(query=original_query)

        ALPHA, BETA = 1.0, 0.75
        processed_query_str = " ".join(self._preprocess(original_query, stem=True))
        original_query_vector = self.vectorizer.transform([processed_query_str])

        relevant_indices = [self.filename_to_index[name] for name in relevant_docs if name in self.filename_to_index]
        if not relevant_indices: return self.search(query=original_query)

        relevant_vectors = self.resume_vectors[relevant_indices]
        centroid_relevant = np.mean(relevant_vectors, axis=0)
        centroid_relevant_array = np.asarray(centroid_relevant)
        original_query_array = original_query_vector.toarray()
        new_query_array = ALPHA * original_query_array + BETA * centroid_relevant_array

        cosine_similarities = cosine_similarity(new_query_array, self.resume_vectors).flatten()
        return {"results": self._get_ranked_results(cosine_similarities)}

    def correct_spelling(self, term):
        if term in self.unstemmed_vocabulary: return term
        min_dist, corrected_term = float('inf'), term
        for vocab_word in self.unstemmed_vocabulary:
            dist = nltk.edit_distance(term, vocab_word)
            if dist < min_dist:
                min_dist, corrected_term = dist, vocab_word
        return corrected_term if min_dist <= 2 else term

    def handle_wildcard(self, term):
        prefix = term.strip('*')
        return [word for word in self.unstemmed_vocabulary if word.startswith(prefix)]

    def tolerant_search(self, query):
        if not self.unstemmed_vocabulary: return {"error": "Vocabulary not built."}

        query_terms = query.lower().split()
        corrected_terms = []
        for term in query_terms:
            if '*' in term and term.endswith('*'):
                corrected_terms.extend(self.handle_wildcard(term))
            else:
                corrected_terms.append(self.correct_spelling(term))

        rewritten_query = " ".join(corrected_terms)
        print(f"Original Query: '{query}' -> Rewritten Query: '{rewritten_query}'")

        return self.search(query=rewritten_query)