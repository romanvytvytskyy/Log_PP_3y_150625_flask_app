
#* file db.py

import sqlite3
db_name = 'quiz.sqlite'
conn = None
cursor = None


def open():
    global conn, cursor
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()


def close():
    cursor.close()
    conn.close()


def do(query):
    cursor.execute(query)
    conn.commit()


def clear_db():
    ''' видаляє всі таблиці '''
    open()
    query = '''DROP TABLE IF EXISTS quiz_content'''
    do(query)
    query = '''DROP TABLE IF EXISTS question'''
    do(query)
    query = '''DROP TABLE IF EXISTS quiz'''
    do(query)
    close()

def create():
    open()
    cursor.execute('''PRAGMA foreign_keys=On''')
    
    do('''CREATE TABLE IF NOT EXISTS quiz( 
                   id INTEGER PRIMARY KEY, 
                   name VARCHAR)''')
                   
    do('''CREATE TABLE IF NOT EXISTS question(
    id INTEGER PRIMARY KEY,
    question VARCHAR,
    answer VARCHAR,
    wrong1 VARCHAR,
    wrong2 VARCHAR,
    wrong3 VARCHAR)''')
    
    do('''CREATE TABLE IF NOT EXISTS quiz_content (
       id INTEGER PRIMARY KEY,
       quiz_id INTEGER,
       question_id INTEGER,
       FOREIGN KEY (quiz_id) REFERENCES quiz(id),
       FOREIGN KEY (question_id) REFERENCES question(id))''')
       
    close()


def add_questions():
    questions = [
        # --- ЛОГІКА ТА ЖАРТИ (6-10 років) ---
        ('Скільки місяців у році мають 28 днів?', 'Всі', 'Один', 'Жодного', 'Два'),
        ('Якою рукою краще розмішувати чай?', 'Ложкою', 'Правою', 'Лівою', 'Будь-якою'),
        ('Що стає більшим, якщо його поставити догори ногами?', 'Число 6', 'Повітряна кулька', 'Дерево', 'Камінь'),
        ('Що належить вам, але інші користуються цим частіше?', 'Ваше ім’я', 'Ваш телефон', 'Ваш велосипед', 'Ваші кросівки'),
        ('На яке питання ніколи не можна відповісти "так", якщо ви спите?', 'Ви вже спите?', 'Ви чуєте мене?', 'Ви хочете їсти?', 'Зараз день?'),
        ('Що можна побачити із заплющеними очима?', 'Сон', 'Темряву', 'Майбутнє', 'Нічого'),
        
        # --- ПРИРОДА ТА ТВАРИНИ (6-12 років) ---
        ('Скільки ніг у павука?', 'Вісім', 'Шість', 'Десять', 'Чотири'),
        ('Який птах є символом мудрості?', 'Сова', 'Орел', 'Папуга', 'Горобець'),
        ('Яка найбільша тварина на планеті?', 'Синій кит', 'Слон', 'Жираф', 'Білий ведмідь'),
        ('Яка планета Сонячної системи є найбільшою?', 'Юпітер', 'Сатурн', 'Марс', 'Земля'),
        ('Звідки сходить сонце?', 'Зі сходу', 'Із заходу', 'З півдня', 'З півночі'),
        ('Яка рослина завжди "стежить" за сонцем?', 'Соняшник', 'Троянда', 'Кактус', 'Ромашка'),
        ('Який метал рідкий за кімнатної температури?', 'Ртуть', 'Залізо', 'Золото', 'Алюміній'),

        # --- ЗАГАЛЬНА ЕРУДИЦІЯ (10-14 років) ---
        ('Хто написав "Кобзар"?', 'Тарас Шевченко', 'Іван Франко', 'Леся Українка', 'Григорій Сковорода'),
        ('Яка столиця Франції?', 'Париж', 'Лондон', 'Берлін', 'Рим'),
        ('Скільки континентів на Землі?', '7', '5', '6', '8'),
        ('Як називається найглибша точка океану?', 'Маріанська западина', 'Бермудський трикутник', 'Чорна діра', 'Керченська протока'),
        ('Який газ ми вдихаємо для життя?', 'Кисень', 'Азот', 'Вуглекислий газ', 'Водень'),
        ('Хто винайшов електричну лампочку?', 'Томас Едісон', 'Нікола Тесла', 'Ісаак Ньютон', 'Альберт Ейнштейн'),
        ('В якій країні винайшли папір?', 'Китай', 'Єгипет', 'Греція', 'Індія'),

        # --- ТЕХНОЛОГІЇ ТА ІТ (10-18 років) ---
        ('Яка мова програмування названа на честь змії?', 'Python', 'Java', 'C++', 'Ruby'),
        ('Що таке "баг" у програмуванні?', 'Помилка в коді', 'Вірус', 'Спеціальна функція', 'Захист даних'),
        ('Який пристрій використовується для введення тексту в комп’ютер?', 'Клавіатура', 'Монітор', 'Миша', 'Принтер'),
        ('Як називається головний мозок комп’ютера?', 'Процесор', 'Оперативна пам’ять', 'Відеокарта', 'Блок живлення'),
        ('Яка компанія створила операційну систему Windows?', 'Microsoft', 'Apple', 'Google', 'Linux'),
        ('Що означає скорочення WWW?', 'World Wide Web', 'World West Web', 'Wide World Work', 'Work Win World'),
        ('Який символ використовується в Python для коментарів?', '#', '//', '/*', '--'),
        ('Яке розширення зазвичай мають файли Python?', '.py', '.txt', '.exe', '.js'),

        # --- МАТЕМАТИКА ТА НАУКА (12-18 років) ---
        ('Чому дорівнює корінь квадратний з 81?', '9', '7', '8', '10'),
        ('Яке число вважається "дюжиною"?', '12', '10', '13', '24'),
        ('Скільки градусів у розгорнутому куті?', '180', '90', '360', '45'),
        ('Яка найближча до Землі зірка?', 'Сонце', 'Полярна зірка', 'Сіріус', 'Проксіма Центавра'),
        ('Яка формула води?', 'H2O', 'CO2', 'NaCl', 'O2'),
        ('Скільки секунд у одній годині?', '3600', '60', '600', '1200'),
        ('Хто сформулював закон всесвітнього тяжіння?', 'Ісаак Ньютон', 'Галілео Галілей', 'Чарльз Дарвін', 'Стівен Гокінг'),

        # --- ГЕОГРАФІЯ ТА КУЛЬТУРА (14-18 років) ---
        ('Яка найдовша річка у світі?', 'Амазонка', 'Ніл', 'Дніпро', 'Дунай'),
        ('Яка країна має найбільшу площу у світі?', 'Канада', 'Китай', 'США', 'Бразилія'),
        ('На якому континенті розташована пустеля Сахара?', 'Африка', 'Азія', 'Австралія', 'Південна Америка'),
        ('В якому році Україна проголосила незалежність?', '1991', '1990', '1996', '2001'),
        ('Як називається валюта Японії?', 'Єна', 'Юань', 'Долар', 'Вон'),
        ('Яка найвища гора світу?', 'Еверест', 'Говерла', 'Кіліманджаро', 'Монблан'),
        ('Хто намалював "Мона Лізу"?', 'Леонардо да Вінчі', 'Пабло Пікассо', 'Вінсент ван Гог', 'Сальвадор Далі'),

        # --- СКЛАДНІ ТА ЦІКАВІ ПИТАННЯ (16-18 років) ---
        ('Скільки кісток у тілі дорослої людини?', '206', '300', '150', '250'),
        ('Який елемент є найпоширенішим у всесвіті?', 'Водень', 'Кисень', 'Гелій', 'Залізо'),
        ('Яка швидкість світла у вакуумі (приблизно)?', '300 000 км/с', '150 000 км/с', '1 000 000 км/с', '340 м/с'),
        ('Що вивчає наука ентомологія?', 'Комах', 'Птахів', 'Гриби', 'Зірки'),
        ('Яка мова є офіційною у Бразилії?', 'Португальська', 'Іспанська', 'Бразильська', 'Англійська'),
        ('Який вітамін виробляється в організмі людини під дією сонця?', 'D', 'C', 'A', 'B12'),
        ('Як називається найменша частинка хімічного елемента?', 'Атом', 'Молекула', 'Клітина', 'Електрон'),
        ('В якому місті відбулися перші сучасні Олімпійські ігри?', 'Афіни', 'Рим', 'Париж', 'Лондон')
    ]
    open()
    cursor.executemany(
             '''INSERT INTO question (question, answer, wrong1, wrong2, wrong3) 
             VALUES(?, ?, ?, ?, ?)''', questions)
    conn.commit()
    close()
    
def add_quiz():
    quizes = [
        ('Логіка та жарти (6-10 років)',),
        ('Природа та тварини (6-12 років)',),
        ('Загальна ерудиція (10-14 років)',),
        ('Технології та ІТ (10-18 років)',),
        ('Математика та наука (12-18 років)',),
        ('Географія та культура (14-18 років)',),
        ('Складні та цікаві питання (16-18 років)',)
    ]
    open()
    cursor.executemany(
             '''INSERT INTO quiz (name) 
             VALUES(?)''', quizes)
    conn.commit()
    close()
    
def add_links():
    open()
    cursor.execute('''PRAGMA foreign_keys=On''')
    query = '''INSERT INTO quiz_content (quiz_id, question_id) VALUES(?, ?)'''
    answer = input("Додати зв'язок (y/n)? ")
    while answer != 'n':
        quiz_id = int(input('Введіть id вікторини: '))
        question_id = int(input('Введіть id питання: '))
        cursor.execute(query, (quiz_id, question_id))
        conn.commit()
        answer = input("Додати зв'язок (y/n)? ")
    close()
    
    
def auto_add_links():
    open()
    cursor.execute('''PRAGMA foreign_keys=On''')
    query = '''INSERT INTO quiz_content (quiz_id, question_id) VALUES(?, ?)'''
    links_map = [
        (1, 1, 6),   
        (2, 7, 13),  
        (3, 14, 20), 
        (4, 21, 28), 
        (5, 29, 35), 
        (6, 36, 42), 
        (7, 43, 50)  
    ]
    links_to_insert = []
    
    for quiz_id, start_id, end_id in links_map:
        for q_id in range(start_id, end_id + 1):
            links_to_insert.append((quiz_id, q_id))
            
    cursor.executemany(query, links_to_insert)
    
    conn.commit()
    print(f"Автоматично додано {len(links_to_insert)} зв'язків між питаннями та вікторинами.")
    close()

    
def show(table):
    query = f'''SELECT * FROM {table}'''
    open()
    cursor.execute(query)
    print(cursor.fetchall())
    close()
    

def show_tables():
    show('question')
    show('quiz')
    show('quiz_content')    
    
def get_question_after(question_id = 0, quiz_id = 1):
    open()
    query = '''SELECT quiz_content.id, question.question, question.answer, question.wrong1, 
                question.wrong2, question.wrong3 FROM question, quiz_content 
                WHERE quiz_content.question_id = question.id AND quiz_content.id > ? 
                AND quiz_content.quiz_id = ? ORDER BY quiz_content.id'''
    print(question_id, quiz_id)
    cursor.execute(query, (question_id, quiz_id))
    result = cursor.fetchone()
    close()
    return result

def get_quises():
    query = 'SELECT * FROM quiz ORDER BY id'
    open()
    cursor.execute(query)
    result = cursor.fetchall()
    close()
    return result 

def check_answer(q_id, ans_text):
    query = '''
            SELECT question.answer 
            FROM quiz_content, question 
            WHERE quiz_content.id = ? 
            AND quiz_content.question_id = question.id
        '''
    open()
    cursor.execute(query, str(q_id))
    result = cursor.fetchone()
    close()    
    if result is None:
        return False 
    else:
        if result[0] == ans_text:
            return True 
        else:
            return False 


def main():
    clear_db()
    create()
    add_questions()
    add_quiz()
    # add_links()
    auto_add_links()
    show_tables()
    print(get_question_after(1,3))
    
if __name__ == '__main__':
    main()