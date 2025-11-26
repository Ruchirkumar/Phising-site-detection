# Phishing Website Detection - Frontend

This adds a minimal Flask frontend so you can test the trained models interactively.

Files added
- `app.py` - small Flask app that loads `vectorizer.pkl` and either `Phishing.pkl` (Logistic Regression) or `phishing_mnb.pkl` (MultinomialNB) if present in the project root.
- `templates/index.html` - form to enter a URL and choose a model.
- `templates/result.html` - shows prediction result.
- `static/style.css` - minimal styling.
- `requirements.txt` - Python dependencies.

Setup

1. Make sure the pickles produced by the notebook are in the project root:

   - `vectorizer.pkl`
   - `Phishing.pkl` (Logistic Regression) and/or `phishing_mnb.pkl` (MultinomialNB)

2. Create and activate a virtual environment, install deps:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Run the app:

```bash
python app.py
```

4. Open http://127.0.0.1:5000 in a browser and enter a URL to test.

Notes and security

- Pickle files can execute arbitrary code. Only use models you trust.
- If the vectorizer or models are missing the UI will flash helpful messages telling you which files are absent.
