# Модуль Кирилла

from flask import request, session, render_template

def demukron():
    matrix = request.get_data(as_text=True)  # получаем матрицу из запроса

    print(matrix) # тестовый вывод

    session['matrix'] = matrix # сохранение матрицы в словаре "Session"

    return 'Данные успешно получены на сервере' # требуется возврат текстового значения


def demukron_result():
    print('Work!')