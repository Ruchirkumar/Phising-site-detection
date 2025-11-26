from flask import Flask, render_template, request, redirect, url_for, flash
import pickle
import os

BASE_DIR = os.path.dirname(__file__)
VECT_PATH = os.path.join(BASE_DIR, 'vectorizer.pkl')
LR_MODEL_PATH = os.path.join(BASE_DIR, 'Phishing.pkl')
MNB_MODEL_PATH = os.path.join(BASE_DIR, 'phishing_mnb.pkl')

app = Flask(__name__)
app.secret_key = 'dev-secret-for-local-testing'


def load_artifacts():
    vect = None
    lmodel = None
    mnb = None
    if os.path.exists(VECT_PATH):
        with open(VECT_PATH, 'rb') as f:
            vect = pickle.load(f)
    if os.path.exists(LR_MODEL_PATH):
        with open(LR_MODEL_PATH, 'rb') as f:
            lmodel = pickle.load(f)
    if os.path.exists(MNB_MODEL_PATH):
        with open(MNB_MODEL_PATH, 'rb') as f:
            mnb = pickle.load(f)
    return vect, lmodel, mnb


def preprocess_url(url: str) -> str:
    """Normalize URL to match notebook preprocessing: remove protocol (http/https), leading 'www.' and trailing slashes."""
    if not isinstance(url, str):
        return url
    url = url.strip()
    # remove protocol
    if url.startswith('http://'):
        url = url[len('http://'):]
    elif url.startswith('https://'):
        url = url[len('https://'):]
    # remove leading www.
    if url.startswith('www.'):
        url = url[len('www.'):]
    # remove trailing /
    url = url.rstrip('/')
    return url


@app.route('/', methods=['GET', 'POST'])
def index():
    vect, lmodel, mnb = load_artifacts()
    models_available = {
        'LogisticRegression': lmodel is not None,
        'MultinomialNB': mnb is not None
    }

    if request.method == 'POST':
        url_text = request.form.get('url', '').strip()
        model_choice = request.form.get('model')

        if not url_text:
            flash('Please enter a URL to analyze.', 'error')
            return redirect(url_for('index'))

        if vect is None:
            flash('Vectorizer (vectorizer.pkl) not found. Place it in the project root.', 'error')
            return redirect(url_for('index'))

        # preprocess and transform URL using vectorizer
        try:
            url_processed = preprocess_url(url_text)
            X = vect.transform([url_processed])
        except Exception as e:
            flash(f'Error transforming input with vectorizer: {e}', 'error')
            return redirect(url_for('index'))

        if model_choice == 'LogisticRegression':
            if lmodel is None:
                flash('Logistic Regression model not found (Phishing.pkl).', 'error')
                return redirect(url_for('index'))
            pred = lmodel.predict(X)[0]
        else:
            # default to MultinomialNB
            if mnb is None:
                flash('MultinomialNB model not found (phishing_mnb.pkl).', 'error')
                return redirect(url_for('index'))
            pred = mnb.predict(X)[0]

        # normalize prediction to readable label
        label = str(pred)
        if label.lower() in ['bad', 'phishing', '1', 'true']:
            human = 'Phishing / Malicious'
        elif label.lower() in ['good', 'legit', '0', 'false']:
            human = 'Legitimate / Safe'
        else:
            human = label

        return render_template('result.html', url=url_text, model=model_choice, prediction=human, raw=label)

    return render_template('index.html', models=models_available)


if __name__ == '__main__':
    app.run(debug=True)

