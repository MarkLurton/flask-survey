from flask import Flask, request, render_template, redirect, flash, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = 'letsgostros'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


@app.route('/')
def home_page():
    """Home Page for Survey App"""
    return render_template('index.html', surveys=surveys)

@app.route('/survey-select', methods=["POST"])
def save_survey_selection():
    """Save survey selection to session"""
    survey = request.form['survey']
    session['survey'] = survey
    return redirect('/survey')

@app.route('/survey')
def survey_start_page():
    """Survey Start Page for Survey App"""
    return render_template('survey.html', survey=surveys[f"{session['survey']}"])

@app.route('/questions/<number>', methods=['POST', 'GET'])
def get_question(number):
    """Page for survey questions"""
    responses = session.get("responses", [])
    number = int(number)
    if len(responses) == len(surveys[f"{session['survey']}"].questions):
        return redirect('/thanks')
    else:
        if number != len(responses):
            flash(f'Uh oh. Looks like you tried to go to the wrong question. You are on question: {len(responses) +1}.')
            return redirect(f'/questions/{len(responses)}')
        else:
            return render_template('questions.html', survey=surveys[f"{session['survey']}"], number=int(number), len=len(surveys[f"{session['survey']}"].questions))

@app.route('/answers/<number>', methods=['POST'])
def save_response(number):
    """Save response and redirect to next page"""
    responses = session.get("responses", [])
    number = int(number)
    text = request.form.get("text", False)
    if text:
        responses.append([request.form.get("response", None), text])
    else:
        responses.append([request.form.get("response", None)])
    session["responses"] = responses
    print(session["responses"])
    if number + 1 < len(surveys[f"{session['survey']}"].questions):
        return redirect(f'/questions/{number+1}')
    else:
        return redirect('/thanks')

@app.route('/thanks')
def thanks():
    print(session["responses"])
    return render_template('thanks.html', responses=session["responses"], questions = enumerate(surveys[f"{session['survey']}"].questions))
