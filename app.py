from flask import Flask, request, render_template, redirect, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'letsgostros'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def home_page():
    """Home Page for Survey App"""
    return render_template('index.html', survey=satisfaction_survey)

@app.route('/questions/<number>', methods=['GET'])
def get_question(number):
    """Page for survey questions"""
    number = int(number)
    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/thanks')
    else:
        if number != len(responses):
            flash(f'Uh oh. Looks like you tried to go to the wrong question. You are on question: {len(responses) +1}.')
            return redirect(f'/questions/{len(responses)}')
        else:
            return render_template('questions.html', survey=satisfaction_survey, number=int(number), len=len(satisfaction_survey.questions))

@app.route('/answers/<number>', methods=['POST'])
def save_response(number):
    """Save response and redirect to next page"""
    number = int(number)
    responses.append(request.form.get("response", None))
    print(responses)
    if number + 1 < len(satisfaction_survey.questions):
        return redirect(f'/questions/{number+1}')
    else:
        return redirect('/thanks')

@app.route('/thanks')
def thanks():
    return render_template('thanks.html')
