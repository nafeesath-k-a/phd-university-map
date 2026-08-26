"""
update_university.py

Run this when you get NEW information about a university you already added
(e.g. you find a new professor, a paper, or a conference), instead of
adding it as a duplicate.

Usage:
    python scripts/update_university.py
"""

import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, "..", "data", "universities.json")


def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def choose_university(data):
    print("\nWhich university do you want to update?\n")
    for i, uni in enumerate(data):
        print(f"  [{i}] {uni['name']} ({uni.get('country', '')})")
    choice = input("\nEnter number: ").strip()
    try:
        return data[int(choice)]
    except (ValueError, IndexError):
        print("Invalid choice.")
        return None


def main():
    data = load_data()
    if not data:
        print("No universities found yet. Run add_university.py first.")
        return

    uni = choose_university(data)
    if uni is None:
        return

    print(f"\nUpdating: {uni['name']}")
    print("What would you like to add?")
    print("  1) Professor / collaborator")
    print("  2) Paper")
    print("  3) Conference")
    print("  4) Update status")
    print("  5) Update general notes")
    choice = input("Choose 1-5: ").strip()

    if choice == "1":
        name = input("Professor/collaborator name: ").strip()
        note = input("Note: ").strip()
        uni.setdefault("professors", []).append({"name": name, "note": note})
    elif choice == "2":
        name = input("Paper title: ").strip()
        note = input("Note (authors, link, relevance...): ").strip()
        uni.setdefault("papers", []).append({"name": name, "note": note})
    elif choice == "3":
        name = input("Conference name: ").strip()
        note = input("Note (date, location, relevance...): ").strip()
        uni.setdefault("conferences", []).append({"name": name, "note": note})
    elif choice == "4":
        print("Options: interested / shortlisted / applied / accepted / rejected")
        uni["status"] = input("New status: ").strip() or uni.get("status", "interested")
    elif choice == "5":
        uni["notes"] = input("New general notes: ").strip()
    else:
        print("Invalid choice, nothing changed.")
        return

    save_data(data)
    print(f"\nUpdated '{uni['name']}'.")
    print("Next: git add . && git commit -m \"update {}\" && git push".format(uni["name"]))


if __name__ == "__main__":
    main()
