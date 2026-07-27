# Stupid memory
'''
memory = {} 

def save_memory(key, value):
    memory[key] = value

def get_memory(key):
    return memory.get(key)


save_memory("name", "nirmalya")
save_memory("favourite language", "c")

print(get_memory("name"))
'''

# Persistent memory
import os
import json
from pathlib import Path

MEMORY_FILE = "memory.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}
    try:
        with open(MEMORY_FILE, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
            return {}

def save_memory(memory):
    with open(MEMORY_FILE, "w") as file:
        json.dump(memory, file, indent=4)

def add_memory(key, value):
    memory = load_memory()

    memory[key] = value 
    
    save_memory(memory)

def get_memory(key):
    memory = load_memory()

    return memory.get(key)

def delete_memory(key):
    memory = load_memory()

    if key in memory:
        del memory[key]

        save_memory(memory)

        return True

    return False

def get_all_memories():
    return load_memory()

# =========================

def process_message(message):
    print(f"\nUser said: {message}")

    should_remember = input("Should this be remembered? (y/n): ")

    if should_remember.lower() != "y":
        print("Discarded.")
        return

    key = input("Key: ")
    value = input("Value: ")

    add_memory(key, value)

    print("Memory stored.")
