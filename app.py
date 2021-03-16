from flask import Flask, flash, render_template, redirect, request, session 
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'some message'
debug = DebugToolbarExtension(app)

responses = 'responses'



@app.route('/')
def index():
    return render_template('index.html', survey=satisfaction_survey)

@app.route('/questions/<int:index>/')
def question(index):

    # redirect to initialize-responses if they don't have the responses list
    if(session.get(responses, False) == False):
        redirect('/initialize-responses')

    answers_count = len(session.get(responses))
    question_count = len(satisfaction_survey.questions)

    # redirect to thank you page if they have completed the survey
    if(answers_count == question_count):
        return redirect('/thanks')

    # redirect to the question they are currently on if they enter a url for a different question
    if(index != answers_count):
        flash('You have been redirected to this page after attempting to access an invalid url.')
        return redirect(f'/questions/{answers_count}')

    question = satisfaction_survey.questions[index]
    return render_template('question.html', question=question, question_num=index + 1)


@app.route('/answer/<int:question_num>', methods=['POST'])
def answer(question_num):

    # redirect to initialize-responses if they don't have responses list
    if(session.get(responses, False) == False):
        redirect('/initialize-responses')

    temp_responses = session[responses]
    temp_responses.append(request.form.get('answer'))
    session[responses] = temp_responses

    # send to thank you page if they have answered all questions
    if(question_num == len(satisfaction_survey.questions)): 
        return redirect('/thanks')

    return redirect(f'/questions/{question_num}')


@app.route('/thanks')
def thank_you():
    return render_template('thanks.html')

@app.route('/initialize-responses', methods=['POST'])
def initialize_responses():
    session[responses] = []

    return redirect('/questions/0')