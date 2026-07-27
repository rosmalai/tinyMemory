import os
import json 
from dotenv import load_dotenv
from embedding import embed
from openai import OpenAI
from openai.resources.chat.completions.messages import Messages

from memory import save_memory

load_dotenv()

OPENROUTER_API_KEY=os.getenv("OPENROUTER_API_KEY")


client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    # for openrouter base_url
    base_url="https://openrouter.ai/api/v1"
)


MEMORY_EXTRACTOR_PROMPT = """
You are a memory extraction system.

Your job is to extract information from the user's message that could
be useful in future conversations.

Good memories include:
- personal preferences
- interests
- goals
- ongoing projects
- skills
- important personal facts
- long-term constraints

Do NOT store:
- casual conversation
- temporary information
- questions
- information that is unlikely to matter later

Return ONLY valid JSON in this format:

{
  "memories": [
    {
      "type": "preference | fact | goal | interest | project | skill | constraint",
      "key": "short descriptive key",
      "value": "the information to remember"
    }
  ]
}

If there is nothing worth remembering:

{
  "memories": []
}
"""


def memory_extract(user_message: str) -> list[dict]:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role":"system",
                "content":MEMORY_EXTRACTOR_PROMPT
            },{
                "role":"user",
                "content":user_message,
            }
        ],
        response_format={"type":"json_object"},
        max_tokens=300
    )

    content = response.choices[0].message.content

    if content is None:
        return [] # 

    data = json.loads(content)

    return data["memories"]


def add_embedding(memories: list[dict]) -> list[dict]:
    for memory in memories:
        memory["embedding"] = embed(memory["value"])

    return memories


if __name__ == "__main__":
    message="""
    I'm learning AI agents right now.
    I'm especially interested in understanding memory systems 
    and I prefer learning things by implementing them from scratch.
    """

    memories = memory_extract(message)

    memories = add_embedding(memories)

    save_memory(memories)

    print(json.dumps([
    {**memory, "embedding": memory["embedding"][-5:]}
    for memory in memories
], indent=2))
