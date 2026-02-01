from random import randint, shuffle
from flask import Flask, session, redirect, url_for, render_template, request
from db import get_question_after, get_quises, check_answer
import os 

def start_quiz(quiz_id):
    session['quiz'] = quiz_id
    session['last_question'] = 0
    session['answers'] = 0
    session['total'] = 0
    
def end_quiz():
    session.clear()
    
def quiz_form():
    q_list = get_quises()
    return render_template('start.html', q_list=q_list)    

# quiz = 0
# last_question = 0
def index():
    # global quiz, last_question
    # max_quiz = 3
    # session['quiz'] = randint(1, max_quiz)
    # session['last_question'] = 0
    # return '<a href="/test">Тест</a>'
    if request.method == 'GET':
        start_quiz(-1)
        return quiz_form()
    else:
        quiz_id = request.form.get('quiz')
        start_quiz(quiz_id)
        return redirect(url_for('test'))

def save_answers():
    answer = request.form.get('ans_text')
    quest_id = request.form.get('quest_id')
    session['total'] += 1
    session['last_question'] = quest_id
    if check_answer(quest_id,answer):
        session['answers'] += 1
        
def question_form(question):
    answer_list = [question[2], question[3], question[4], question[5]]
    shuffle(answer_list)
    return render_template('test.html', question=question[1],
                           quest_id = question[0], answer_list=answer_list)
    
        

def test():
    # global last_question
    # question = get_question_after(session['last_question'], session['quiz'])
    # if question is None or len(question) == 0:
    #     return redirect(url_for('result'))
    # session['last_question'] = question[0]
    # return '<h1>' + str(session['quiz']) + '</h1><br>' + str(question) + '<br>'
    if not ('quiz' in session) or int(session['quiz'])< 0:
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            save_answers()
        
        next_question = get_question_after(session['last_question'], session['quiz'])
        if next_question is None or len(next_question) == 0:
            return redirect(url_for('result'))
        else:
            return question_form(next_question)
        
        
    
def result():
    html = render_template('result.html', 
                           answers=session['answers'], 
                           total=session['total'])
    end_quiz()
    return html

folder = os.getcwd()
print(folder)
app = Flask(__name__, template_folder='folder', static_folder=  'folder')
app.add_url_rule('/', 'index', index)
app.add_url_rule('/test', 'test', test)
app.add_url_rule('/result', 'result', result)
app.config['SECRET_KEY'] = 'secret'

if __name__ == '__main__':
    app.run()
