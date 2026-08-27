# My PhD University Atlas

An interactive world map for tracking universities. Click a pin to see the professors/collaborators, papers, and
conferences.

It's a static site (HTML/CSS/JS + a JSON data file), hosted for free on
GitHub Pages. Add new universities with a small Python script.


---

## Part 1 — One-time setup

### 1. Create a GitHub account 
Go to https://github.com and sign up.

### 2. Install Git on your computer
- **Windows:** download from https://git-scm.com/download/win and install with default options.
- **Mac:** open Terminal and type `git --version` — it will prompt you to install if missing.
- **Linux:** `sudo apt install git`

Check it worked by opening a terminal (Command Prompt / Terminal) and typing:
```
git --version
```
You should see a version number.

### 3. Install Python packages
This project uses one small library, `geopy`, to automatically find the
latitude/longitude of a university from its name. In a terminal:
```
pip install geopy
```
(or `pip3 install geopy`, depending on system)

### 4. Create the GitHub repository
1. Go to https://github.com/new
2. Repository name: `phd-university-map` (or anything you like)
3. Set it to **Public** (required for free GitHub Pages)
4. Do NOT check "Add a README" — leave everything else default
5. Click **Create repository**
6. GitHub will show you a page with a URL like:
   `https://github.com/YOUR-USERNAME/phd-university-map.git`
   Keep this tab open, you'll need that URL in step 6.

### 5. Get this project onto your computer
Unzip the project folder you downloaded, and note where it is
(e.g. `Desktop/phd-university-map`).

### 6. Push it to GitHub
Open a terminal, navigate into the folder, then run these commands one
at a time:

```
cd path/to/phd-university-map
git init
git add .
git commit -m "first version of my PhD university map"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/phd-university-map.git
git push -u origin main
```
Replace the URL with the one from step 4. GitHub may ask you to log in
(it may open a browser window — just follow the prompts).

### 7. Turn on GitHub Pages
1. On your repository's GitHub page, click **Settings**
2. In the left sidebar, click **Pages**
3. Under "Build and deployment" → "Source", choose **Deploy from a branch**
4. Branch: `main`, folder: `/ (root)` → click **Save**
5. Wait about a minute, then refresh the page. GitHub will show you a
   URL like:
   `https://YOUR-USERNAME.github.io/phd-university-map/`

Open that URL — you should see your map with Kent State University
already on it as an example pin. **This is now a live website anyone
with the link can view** (but only you can edit it, from your computer).

---

## Part 2 — Adding new information

Every time you learn about a new university, a new professor, a paper,
or a conference, do this:

### Adding a brand-new university
```
cd path/to/phd-university-map
python scripts/add_university.py
```
It will ask you for the name, look up coordinates automatically, and
ask about professors/papers/conferences. Answer the prompts (press
Enter on a blank line to skip a section).

### Adding info to a university you already have
```
python scripts/update_university.py
```
Pick the university from the list, then add a professor, paper,
conference, or update its status/notes.

### Publish your changes
After either script, run:
```
git add .
git commit -m "add new info"
git push
```
Within a minute or two, your live map at
`https://YOUR-USERNAME.github.io/phd-university-map/` will update
automatically.

### Editing by hand (optional)
All your data lives in one plain text file: `data/universities.json`.
You can also open it directly in any text editor and edit it, as long
as you keep the format (each university is `{ ... }`, separated by
commas, inside `[ ]`). If you're not confident editing JSON by hand,
just stick to the two Python scripts above — they can't break the format.

---

## How the pins work

Each university has a **status**, shown as a colored dot and in the
sidebar:

| Status | Color |
|---|---|
| interested | blue |
| shortlisted | amber |
| applied | purple |
| accepted | green |
| rejected | red |

Change a university's status any time with `update_university.py`
(option 4).

---

## Project structure
```
phd-university-map/
├── index.html              the page itself
├── css/style.css           styling
├── js/script.js            map + sidebar logic
├── data/universities.json  YOUR DATA — one entry per university
├── scripts/
│   ├── add_university.py     add a new university
│   └── update_university.py  add info to an existing one
└── requirements.txt
```

## Ideas for later
- A search box to jump to a university by name
- Filter buttons to show only "shortlisted" pins
- A "distance from home" or "cost of living" note per pin
- Export your list to a spreadsheet for application tracking

Feel free to ask for help adding any of these once the basic map is
working for you.



https://nafeesath-k-a.github.io/phd-university-map/
