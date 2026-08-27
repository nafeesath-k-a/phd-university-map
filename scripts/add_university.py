"""
add_university.py

Run this whenever you learn about a new university (or new info about one
you already have) and want to add it to your map.

Usage:
    python scripts/add_university.py

It will ask you questions in the terminal, look up the university's
coordinates automatically (using OpenStreetMap), and save everything into
data/universities.json — the file the map reads from.

Requires: geopy   ->   pip install geopy
"""

import json
import os
import sys

try:
    from geopy.geocoders import Nominatim
except ImportError:
    print("The 'geopy' package is not installed.")
    print("Install it first with:  pip install geopy")
    sys.exit(1)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, "..", "data", "universities.json")


def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def geocode(place_name):
    geolocator = Nominatim(user_agent="phd-university-map")
    location = geolocator.geocode(place_name)
    if location is None:
        return None
    return location.latitude, location.longitude


def prompt_list(label):
    print(f"\nAdd {label}(s) — leave the name blank and press Enter when done.")
    items = []
    while True:
        name = input(f"  {label} name: ").strip()
        if not name:
            break
        note = input(f"  Note about {name} (optional): ").strip()
        items.append({"name": name, "note": note})
    return items


def prompt_scholarships():
    """Prompt for scholarships with name, link, and note."""
    print("\nAdd scholarship(s) — leave the name blank and press Enter when done.")
    items = []
    while True:
        name = input("  scholarship name: ").strip()
        if not name:
            break
        link = input(f"  Website/Link for {name} (optional): ").strip()
        note = input(f"  Note about {name} (optional): ").strip()
        items.append({
            "name": name,
            "link": link,
            "note": note
        })
    return items


def main():
    data = load_data()
    existing_ids = {u.get("id") for u in data}

    print("=== Add a new university ===\n")
    name = input("University name (e.g. Kent State University): ").strip()
    if not name:
        print("A name is required. Aborting.")
        return

    uni_id = name.lower().replace(" ", "-").replace(",", "")
    if uni_id in existing_ids:
        print(f"\nNote: '{name}' already seems to be on the map (id: {uni_id}).")
        proceed = input("Add it again as a duplicate entry anyway? (y/n): ").strip().lower()
        if proceed != "y":
            print("Cancelled. Tip: you can edit the existing entry directly in "
                  "data/universities.json instead.")
            return

    print("\nLooking up coordinates on OpenStreetMap...")
    coords = geocode(name)
    if coords is None:
        print("Could not find it automatically.")
        lat = float(input("Enter latitude manually: ").strip())
        lng = float(input("Enter longitude manually: ").strip())
    else:
        lat, lng = coords
        print(f"Found: {lat:.4f}, {lng:.4f}")
        confirm = input("Use these coordinates? (y/n): ").strip().lower()
        if confirm != "y":
            lat = float(input("Enter latitude manually: ").strip())
            lng = float(input("Enter longitude manually: ").strip())

    country = input("Country: ").strip()
    print("\nStatus options: interested / shortlisted / applied / accepted / rejected")
    status = input("Status [interested]: ").strip() or "interested"
    website = input("Website (optional): ").strip()
    general_notes = input("General notes (optional): ").strip()

    professors = prompt_list("professor/collaborator")
    papers = prompt_list("paper")
    conferences = prompt_list("conference")
    scholarships = prompt_scholarships()

    entry = {
        "id": uni_id,
        "name": name,
        "country": country,
        "lat": lat,
        "lng": lng,
        "status": status,
        "website": website,
        "notes": general_notes,
        "professors": professors,
        "papers": papers,
        "conferences": conferences,
        "scholarships": scholarships,
    }

    data.append(entry)
    save_data(data)
    print(f"\nAdded '{name}' to data/universities.json")
    print("Next: git add . && git commit -m \"add {}\" && git push".format(name))


if __name__ == "__main__":
    main()