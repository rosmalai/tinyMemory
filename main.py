from memory import(
    add_memory,
    get_memory,
    delete_memory,
    get_all_memories,
    process_message
)

def main():
    while True:
        print("\n--- MEMORY SYSTEM ---")
        print("1. Add memory")
        print("2. Get memory")
        print("3. Show all memories")
        print("4. Delete memory")
        print("5. Exit")

        choice = input("\nChoose: ")

        if choice == "1":

            key = input("Key: ")
            value = input("Value: ")

            add_memory(key, value)

            print("Memory stored.")

        elif choice == "2":

            key = input("What do you want to remember? ")

            value = get_memory(key)

            if value:
                print(f"{key}: {value}")
            else:
                print("Memory not found.")

        elif choice == "3":

            memories = get_all_memories()

            if not memories:
                print("No memories stored.")
            else:
                for key, value in memories.items():
                    print(f"{key}: {value}")

        elif choice == "4":

            key = input("Memory key to delete: ")

            deleted = delete_memory(key)

            if deleted:
                print("Memory deleted.")
            else:
                print("Memory not found.")

        elif choice == "5":
            break

        else:
            print("Invalid option.")

'''
messages = [
    "My name is Nirmalya",
    "I'm learning AI agents",
    "I had pizza today",
    "I mostly use Python"
]


for message in messages:
    process_message(message)
'''

if __name__ == "__main__":
    main()

