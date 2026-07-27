import os 
import json 
from memory import (
    load_memory,save_memory, get_memory, get_all_memories
)
from embedding import embed, cosine_similarity


# Keyword Search retrieval
def retrieve(query:str, memories:list[str]) -> list[str]:
    query_words = set(query.lower().split())

    scored = []

    for memory in memories:
        memory_words=set(memory.lower().split())

        score = len(query_words & memory_words)

        scored.append((score, memory))

    scored.sort(reverse=True)
    
    return [memory for score, memory in scored if score > 0][:3]


# Semantic search 
def  retrieve_memories(query, memories, k=3):
    query_embedding = embed(query)

    results = []

    for memory in memories:

        score = cosine_similarity(
            query_embedding, 
            memory["embedding"]
        )

        results.append({
            "score":score,
            "memory":memory
        })
    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:k]



# --------- test -----------
memories = load_memory()

results = retrieve_memories(
    "What programming language should I use?",
    memories
)

for result in results:
    print(result["score"])
    print(result["memory"]["value"])
