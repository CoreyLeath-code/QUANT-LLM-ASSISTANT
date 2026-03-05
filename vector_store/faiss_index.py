import faiss
import numpy as np

dimension = 384
index = faiss.IndexFlatL2(dimension)

def add_embeddings(vectors):
    index.add(np.array(vectors).astype("float32"))

def search(query_vector, top_k=3):
    distances, indices = index.search(
        np.array([query_vector]).astype("float32"), top_k
    )
    return indices
