from langchain_openai import OpenAIEmbeddings
import faiss
import numpy as np

class VectorStore:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.index = None
        self.texts = []

    def build(self, docs):
        vectors = []

        for doc in docs:
            vec = self.embeddings.embed_query(doc["text"])
            vectors.append(vec)
            self.texts.append(doc)

        dim = len(vectors[0])
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(np.array(vectors).astype("float32"))

    def search(self, query):
        q_vec = self.embeddings.embed_query(query)
        D, I = self.index.search(np.array([q_vec]).astype("float32"), k=3)

        return [self.texts[i] for i in I[0]]