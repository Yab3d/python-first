import os

CONTACTS_FILE = "contacts.txt"

def load_contacts():
    contacts = []
    if not os.path.exists(CONTACTS_FILE):
        return contacts

    with open(CONTACTS_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split(",")
                if len(parts) == 2:
                    contacts.append({"name": parts[0], "phone": parts[1]})
    return contacts


def save_contacts(contacts):
    with open(CONTACTS_FILE, "w") as f:
        for contact in contacts:
            f.write(f"{contact['name']},{contact['phone']}\n")


def add_contact(name, phone):
    contacts = load_contacts()
    for c in contacts:
        if c["name"].lower() == name.lower():
            print(f"Contact '{name}' already exists.")
            return
    contacts.append({"name": name, "phone": phone})
    save_contacts(contacts)
    print(f"Contact '{name}' added.")
    print(contacts)


def search_contact(query):
    contacts = load_contacts()
    results = [c for c in contacts if query.lower() in c["name"].lower()]
    if results:
        for c in results:
            print(f"  {c['name']} — {c['phone']}")
    else:
        print(f"No contacts found for '{query}'.")


def delete_contact(name):
    contacts = load_contacts()
    original_count = len(contacts)
    contacts = [c for c in contacts if c["name"].lower() != name.lower()]

    if len(contacts) == original_count:
        print(f"Contact '{name}' not found.")
    else:
        save_contacts(contacts)
        print(f"Contact '{name}' deleted.")


def list_all():
    contacts = load_contacts()
    if not contacts:
        print("No contacts saved yet.")
    else:
        print(f"\n--- {len(contacts)} Contact(s) ---")
        for c in contacts:
            print(f"  {c['name']} — {c['phone']}")


def run():
    print("=== Contact Book ===")
    while True:
        print("\nOptions: add | search | delete | list | quit")
        choice = input("> ").strip().lower()

        if choice == "add":
            name = input("Name: ").strip()
            phone = input("Phone: ").strip()
            add_contact(name, phone)

        elif choice == "search":
            query = input("Search name: ").strip()
            search_contact(query)

        elif choice == "delete":
            name = input("Delete name: ").strip()
            delete_contact(name)

        elif choice == "list":
            list_all()

        elif choice == "quit":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Try: add, search, delete, list, quit")


if __name__ == "__main__":
    run()