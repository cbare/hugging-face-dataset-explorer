"""
Text search.
"""
import numpy as np
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer


nlp = spacy.load("en_core_web_sm")


def tokenizer(document):
    tokens = nlp(document)
    tokens = [
        token.lemma_
        for token in tokens if (
            token.is_stop == False and
            token.is_punct == False and
            token.lemma_.strip()!= ''
        )
    ]
    return tokens


class Index:
    """
    A text search index based on TFIDF.
    """
    def __init__(self, texts, tokenizer=tokenizer):
        self.tokenizer = tokenizer

        # See docs for scikit-learn's TfidfVectorizer:
        # https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html
        self.tfidf_vectorizer = TfidfVectorizer(input='content', tokenizer=tokenizer)

        # document-term matrix as a scipy sparse matrix
        self.M = self.tfidf_vectorizer.fit_transform(texts)

    def search(self, query, top=10):
        # query vector
        qv = self.tfidf_vectorizer.transform([query])

        # a vector of similarity scores between the query and each document
        similarities = np.asarray(self.M.dot(qv.T).todense()).ravel()

        # sort the similarities in descending order
        indices = np.argsort(similarities)[::-1]

        # return indices of top non-zero similarities
        similarities = similarities[indices][:top]
        similarities = similarities[similarities > 0]
        top = np.min([top, len(similarities)])

        return [int(i) for i in indices[:top]]
