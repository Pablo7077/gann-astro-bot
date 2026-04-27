# Mac Setup Guide for a Complete Beginner

This guide assumes you have never coded before.

## Part 1 — Install the tools

### 1. Install Python
- Go to https://www.python.org/downloads/macos/
- Download the latest Python 3 release.
- Open the installer and keep clicking Continue.
- Finish the install.

### 2. Install GitHub Desktop
- Go to https://desktop.github.com/
- Download GitHub Desktop for Mac.
- Drag it into Applications.
- Open it and sign in with your GitHub account.

### 3. Install Visual Studio Code
- Go to https://code.visualstudio.com/
- Download VS Code for Mac.
- Install it.

## Part 2 — Create or replace your GitHub project locally

### If you already have the old repo on GitHub
1. Open your repo page on GitHub.
2. Click the green **Code** button.
3. Click **Open with GitHub Desktop**.
4. In GitHub Desktop, choose a folder like Documents/GitHub.
5. Click **Clone**.

GitHub says you can clone a repository from GitHub to GitHub Desktop by choosing the repository and a local path, then clicking Clone. [web:67][web:68]

## Part 3 — Put the new files into the repo
1. Download the project zip shared with you.
2. Double-click the zip in Finder.
3. Open the extracted folder.
4. Open your cloned GitHub repo folder in Finder.
5. Drag all new project files into your repo folder.
6. If Finder asks whether to replace files, click **Replace**.

## Part 4 — Open Terminal in the project folder
1. Open Finder.
2. Open your project folder.
3. Right-click inside the folder and choose **New Terminal at Folder** if available, or open Terminal manually.
4. In Terminal, type `cd ` and drag the project folder into Terminal, then press Enter.

## Part 5 — Create the Python environment
Python virtual environments isolate project packages so they do not interfere with other Python projects. [web:72][web:75]

Run these commands one by one:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

The built-in `venv` module is the standard way to create a Python virtual environment, and on macOS you activate it with `source my_env/bin/activate`. [web:72]

## Part 6 — Test the project from Terminal
Run these commands one at a time:

```bash
python3 main.py --quick
python3 main.py --symbols
python3 main.py --backtest nifty 2022-01-01
```

## Part 7 — Run the dashboard
Run:

```bash
streamlit run app.py
```

Streamlit starts a local development server and opens your app in a browser tab when you run `streamlit run app.py`. [web:79][web:76]

## Part 8 — Save your changes to GitHub using GitHub Desktop
1. Go back to GitHub Desktop.
2. You will see a list of changed files on the left.
3. Write a commit message like: `Replace Vedic foundation with Gann project scaffold`
4. Click **Commit to main**.
5. Click **Push origin**.

GitHub Desktop lets you clone, pull, commit, and push repositories visually without needing the command line for Git itself. [web:80]

## Part 9 — Beginner rules
- Always activate the environment first with `source .venv/bin/activate`
- Always run commands from the project folder
- If something fails, read the first red error line carefully
- Never edit `requirements.txt` unless you know why
- Test `python3 main.py --quick` before opening Streamlit

## Part 10 — What this project already includes
- Daily market signal engine
- Gann-style time cycle module
- Gann-style square-of-nine style level calculator
- Backtester with strategy-vs-buy-and-hold comparison
- Streamlit dashboard
- Report generator

## Part 11 — Important honesty note
This scaffold gives you a complete working local foundation and backtester, but it is still a research model, not a guaranteed predictive engine. Market performance should be validated carefully before any real use.
