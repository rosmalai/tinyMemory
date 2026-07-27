import math
from sentence_transformers import SentenceTransformer

#model = SentenceTransformer("all-MiniLM-L6-v2")
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def embed(text:str) -> list[float]:
    '''
    text to vector
    '''
    vector = model.encode(text)

    return vector.tolist()


def cosine_similarity(a:list[float], b:list[float]) -> float:
    '''
    compare 2 vector 1.in memory 2.user prompt 
    '''
    
    dot_product = sum(
        x*y 
        for x, y in zip(a, b)
    )
    
    magnitude_a = math.sqrt(
        sum(x*x for x in a)
    )

    magnitude_b = math.sqrt(
        sum(y*y for y in b)
    )

    return dot_product/ (magnitude_a*magnitude_b)


#  --------- test ---------

# test embeding
vector = embed("User prefers Python")

print(len(vector))
print(vector[:5])

# test cosine cosine_similarity




'''
"User prefers Python"
          │
          ▼
┌──────────────────────┐
│ Embedding Model      │
│ all-MiniLM-L6-v2     │
└──────────┬───────────┘
           │
           ▼
[0.021, -0.071, 0.033, ...]
        384 numbers
'''
