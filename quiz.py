from random import randint
from flask import Flask, sessions, redirect, url_for
from db import get_question_after

quiz = 0
last_question = 0
def index():
    global quiz, last_question
    max_quiz = 3
    quiz = randint(1, max_quiz)
    last_question = 0
    return '<a href="/test">Тест</a>'

def test():
    global last_question
    question = get_question_after(last_question, quiz)
    if question is None or len(question) == 0:
        return redirect(url_for('result'))
    last_question = question[0]
    return '<h1>' + str(quiz) + '</h1><br>' + str(question) + '<br>'

def result():
    return '<h1>Результат</h1>'

    
app = Flask(__name__)
app.add_url_rule('/', 'index', index)
app.add_url_rule('/test', 'test', test)
app.add_url_rule('/result', 'result', result)

if __name__ == '__main__':
    app.run()
