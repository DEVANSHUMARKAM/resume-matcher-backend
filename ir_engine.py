import os
import nltk
nltk.data.path.append('nltk_data')
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class SearchEngine:
    #empty containers aur tools generate krrega
    def __init__(self):
        self.stemmer = nltk.stem.PorterStemmer()
        self.stopwords = set(nltk.corpus.stopwords.words('english'))

        self.vectorizer = TfidfVectorizer()
        self.resume_vectors = None
        self.resume_filenames = []
        self.filename_to_index = {}
        self.unstemmed_vocabulary = set()

    #Preprocess text: tokenization, lowercasing, stopword removal, stemming
    def _preprocess(self, text, stem=True):
        tokens = nltk.tokenize.word_tokenize(text.lower())
        filtered_tokens = [word for word in tokens if word.isalpha() and word not in self.stopwords]
        if stem:
            stemmed_tokens = [self.stemmer.stem(word) for word in filtered_tokens]
            return stemmed_tokens
        return filtered_tokens

    #Vector Space Model with TF-IDF
    def load_and_index(self, resume_dir="resumes"):
        """Loads resumes from a directory and builds all necessary indexes."""
        self.resume_filenames = [f for f in os.listdir(resume_dir) if f.endswith(".txt")] #creates list of every file that ends with .txt
        self.filename_to_index = {name: i for i, name in enumerate(self.resume_filenames)} #maps filename to index in list

        # temporary containers 
        processed_resumes_for_tfidf = []
        all_unstemmed_words = []

        # loop through each resume file
        for filename in self.resume_filenames:
            with open(os.path.join(resume_dir, filename), 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                # preprocess for TF-IDF (with stemming)
                processed_resumes_for_tfidf.append(" ".join(self._preprocess(content, stem=True)))
                # preprocess for vocabulary (without stemming)
                all_unstemmed_words.extend(self._preprocess(content, stem=False))

        # build TF-IDF matrix
        if processed_resumes_for_tfidf:
            print(f"Indexing {len(processed_resumes_for_tfidf)} resumes for TF-IDF...")
            # TF-IDF vecctor calculate krrega aur matrix banaega
            self.resume_vectors = self.vectorizer.fit_transform(processed_resumes_for_tfidf)
            print("TF-IDF Indexing complete!")

        # build unstemmed vocabulary
        self.unstemmed_vocabulary = set(all_unstemmed_words)
        print(f"Built unstemmed vocabulary with {len(self.unstemmed_vocabulary)} unique words.")

    def _get_ranked_results(self, similarities):
        # Get top 10 results with similarity > 0
        top_indices = np.argsort(similarities)[-10:][::-1]
        # return list of dicts with filename and score
        return [{ "filename": self.resume_filenames[i], "score": round(float(similarities[i]), 4) } for i in top_indices if similarities[i] > 0]

    def search(self, query):
        # check krrega search model build hua ki nhi 
        if self.resume_vectors is None: return {"error": "No resumes indexed."}
        # preprocess query
        processed_query = " ".join(self._preprocess(query, stem=True))
        # clean query lega aur numerical TF-IDF vector banayega
        query_vector = self.vectorizer.transform([processed_query])
        # raking krega cosine similarity ke basis pr
        cosine_similarities = cosine_similarity(query_vector, self.resume_vectors).flatten()
        return {"results": self._get_ranked_results(cosine_similarities)}

    def refine_search(self, original_query, relevant_docs):
        if not relevant_docs: return self.search(query=original_query)

        # tuning knobs for Rocchio Algorithm
        ALPHA, BETA = 1.0, 0.75
        # preprocess original query
        processed_query_str = " ".join(self._preprocess(original_query, stem=True))
        original_query_vector = self.vectorizer.transform([processed_query_str])


        # get indices of relevant documents
        relevant_indices = [self.filename_to_index[name] for name in relevant_docs if name in self.filename_to_index]
        if not relevant_indices: return self.search(query=original_query)

        # Rocchio Algorithm to adjust query vector
        relevant_vectors = self.resume_vectors[relevant_indices]
        # Rocchio Algorithm in action
        centroid_relevant = np.mean(relevant_vectors, axis=0)
        centroid_relevant_array = np.asarray(centroid_relevant)
        original_query_array = original_query_vector.toarray()
        new_query_array = ALPHA * original_query_array + BETA * centroid_relevant_array

        # compute similarities with adjusted query
        cosine_similarities = cosine_similarity(new_query_array, self.resume_vectors).flatten()
        return {"results": self._get_ranked_results(cosine_similarities)}

    # Spelling correction 
    def correct_spelling(self, term):
        if term in self.unstemmed_vocabulary: return term
        min_dist, corrected_term = float('inf'), term
        for vocab_word in self.unstemmed_vocabulary:
            dist = nltk.edit_distance(term, vocab_word)
            if dist < min_dist:
                min_dist, corrected_term = dist, vocab_word
        return corrected_term if min_dist <= 2 else term

    # Wildcard handling
    def handle_wildcard(self, term):
        prefix = term.strip('*')
        return [word for word in self.unstemmed_vocabulary if word.startswith(prefix)]

    # Tolerant Search combining spelling correction and wildcard handling
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