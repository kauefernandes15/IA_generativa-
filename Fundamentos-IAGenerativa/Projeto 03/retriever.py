from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class SimpleRetriever:
    def __init__(self, documentos):
        self.documentos = documentos
        self.vectorizer = TfidfVectorizer()
        self.doc_vectors = self.vectorizer.fit_transform(documentos)

    def retrieve(self, query, top_k=1):
        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.doc_vectors)[0]
        top_indices = similarities.argsort()[-top_k:][::-1]
        return [self.documentos[i] for i in top_indices]