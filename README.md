# tinyMemory

## ***Architecture***
```
User message
     │
     ▼
┌──────────────┐
│ Memory       │
│ Retrieval    │
└──────┬───────┘
       │ relevant memories
       ▼
┌──────────────┐
│     LLM      │
└──────┬───────┘
       │ response
       ▼
┌──────────────┐
│ Memory       │
│ Extraction   │
└──────┬───────┘
       │ useful facts
       ▼
┌──────────────┐
│ Memory Store │
└──────────────┘
```
### ***Step 1: Stupid memory***

***Fundamental memory operation***
- *WRITE memory*
- *READ memory*

***Every sophisticated agent-memory system eventually has to do these two things***

### ***Step 2: Make memory persistent***

***Memory disappears when the program stops, so replace that with `memory.json`***

***Now agent has long term memory across program execution***

***At this point don't even connect an LLM***

### ***Step 3: Final real memory problem*** 

***Suppose the conversation is*** 

```
User: My name is Nirmalya.

User: I'm learning AI agents.

User: I mostly use Python.

User: Actually I've started using TypeScript more.
```

***You don't want to***

```
memory = [
   every single message ever sent
]
```
***this would just be conversation history not memory***

***Instead want something like this***

```
[
    {
        "type": "identity",
        "key": "name",
        "value": "Nirmalya"
    },
    {
        "type": "interest",
        "key": "learning",
        "value": "AI agents"
    },
    {
        "type": "preference",
        "key": "programming_language",
        "value": "TypeScript"
    }
]
```

***So the component become***
```
Conversation
     ↓
Memory Extractor
     ↓
Structured Memory
```

### ***Let an LLM extract memory*** 

***Manually extracting memory***

```
Raw conversation
       ↓
┌──────────────────────┐
│ Should I remember it?│  ← Step 3
└──────────┬───────────┘
       yes │      │ no
           ↓      └──→ discard
   Extract information
           ↓
    Structured memory
           ↓
       Storage
```

***LLM work as a memory extractor*** 

```
Raw conversation
      │
      ▼
┌───────────────┐
│      LLM      │
│               │
│ "What here is │
│ worth keeping?"│
└───────┬───────┘
        │
        ▼
Structured memories

[
  {
    type: "interest",
    key: "...",
    value: "..."
  }
]
```

***Memory still stored in `memory.json`***

```
User message
     ↓
LLM extractor       ← what we just built
     ↓
Structured memories
     ↓
Memory store        ← build this next
     ↓
memory.json
```

### ***Solve retrieval; Keyword search***

*Eventually we'll have 1000s memories*

*Suppose the user ask ~ "What project should I build?"*

*Obs I won't want `Prompt = all_1000_memories + user_message`*

*Instead*

```
1000 memories
     │
     ▼
Memory Retrieval
     │
     ▼
~5 relevant memories
     │
     ▼
    LLM
```

### ***Add Embedding***

***Each memory become***

```
{
    "id": 17,

    "text": "User is learning AI agents",

    "embedding": [
        0.234,
        -0.712,
        0.083,
        ...
    ],

    "created_at": "...",

    "importance": 0.7
}
```

***When the user says***
`"What should I study for agent development?"`

***Embade that query***
```
query
 ↓
embedding
 ↓
cosine similarity
 ↓
memory embeddings
 ↓
top-k
```

***So even thought `"learning AI agents"` & `"study for agent development"` doesn't share many exact word, semantic retrieval can connect them***

#### 1. Pick embeded model
local `sentence-transformer` model (don't need embedding API)

#### 2. Add embedding during memory creation
- ***Suppose LLM extrction gives*** 
    ```
    memory = {
        "type": "preference",
        "key": "programming_language",
        "value": "User prefers Python"
    }
    ```
- ***Before storing it*** 
    ```
    memory["embedding"] = embed(memory["value"])
    ```
- ***Then save***
    ```
    {
        "type": "preference",
        "key": "programming_language",
        "value": "User prefers Python",
        "embedding": [
            0.021,
            -0.071,
            0.033,
            ...
        ]
    }
    ```
#### 3. Implement cosine similarity

$$cos(\theta) = \frac{A \cdot B}{\|A\| \|B\|}$$
- ***Close to 1 ~ very similar***
- ***Close to 0 ~ not very similar***

```
                USER
                 │
                 ▼
        ┌────────────────┐
        │ extraction.py  │
        │      LLM       │
        └───────┬────────┘
                │
              memory
                │
                ▼
        ┌────────────────┐
        │ embedding.py   │
        │     embed()    │
        └───────┬────────┘
                │
         memory + vector
                │
                ▼
        ┌────────────────┐
        │   storage.py   │
        └────────────────┘


             Later...


              USER QUERY
                  │
                  ▼
        ┌─────────────────┐
        │  embedding.py   │
        │     embed()     │
        └────────┬────────┘
                 │
           query vector
                 │
                 ▼
        ┌─────────────────┐
        │  retrieval.py   │
        │ cosine similarity│
        └────────┬────────┘
                 │
               Top K
                 │
                 ▼
               LLM
```



### ***Deal with memory update***

- ***Let's say***
    ```
    Day 1:
    "I prefer Python."
    
    Day 20:
    "I've switched to TypeScript lately."
    ```
- ***Naively I got***
    ```
    Memory #1: prefers Python
    Memory #2: prefers TypeScript
    ```
- ***Now retrieval might return both***

- ***System need to reason***
    ```
     new memory
        ↓
     search related existing all_1000_memories
        ↓
    ┌─────────────────────────┐
    │ Is this:                │
    │                         │
    │ NEW information?        │
    │ UPDATE?                 │
    │ DUPLICATE?              │
    │ CONTRADICTION?          │
    └───────────┬─────────────┘
                ↓
      modify memory
    ```

#### ***Implementation order***
- V0 Python dictionary ~> Understand READ / WRITE

- V1 JSON persistence ~> Understand long-term storage

- V2 LLM memory extraction ~> Understand WHAT to remember

- V3 Structured memories + metadata ~> Understand memory representation

- V4 Keyword retrieval ~> Understand retrieval

- V5 Embedding retrieval ~> Understand semantic memory

- V6 Memory update / delete / conflict ~> Understand memory lifecycle

- V7 Importance + recency scoring ~> Understand ranking

- V8 Short-term + long-term memory ~> Understand memory architecture

- V9 Memory consolidation ~> Merge many experiences into knowledge

#### ***Final sctructure***
```
                  USER
                    │
                    ▼
             ┌─────────────┐
             │   Query     │
             └──────┬──────┘
                    │
           ┌────────▼────────┐
           │ Memory Retrieval│
           └────────┬────────┘
                    │
              relevant memories
                    │
                    ▼
             ┌─────────────┐
             │     LLM     │
             └──────┬──────┘
                    │
          ┌─────────▼─────────┐
          │ Memory Extraction │
          └─────────┬─────────┘
                    │
          ┌─────────▼─────────┐
          │ Memory Manager    │
          │                   │
          │ add               │
          │ update            │
          │ delete            │
          │ merge             │
          └─────────┬─────────┘
                    │
                    ▼
             ┌────────────┐
             │Memory Store│
             └────────────┘
```
