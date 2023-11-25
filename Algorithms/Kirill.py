# Модуль Кирилла

from flask import request, session, render_template

def demukron():

    data = request.get_json() # получаем данные
    matrix = data.get('matrix')
    size = data.get('size')
    
    print(f'Размер: {size}', f'Матрица: {matrix}', sep="\n") # тестовый вывод

    session['matrix'] = matrix # сохранение матрицы в словаре "Session"
    session['size'] = size # сохранение матрицы в словаре "Session"

    return 'Данные успешно получены на сервере' # требуется возврат текстового значения


def demukron_result():
    print('Work!')