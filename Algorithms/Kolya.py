# Модуль Коли
from flask import session

def kraskal():
    print('Work!')
    print(f'Данные из сессии в модуля: {session.get("matrix")}') # тестовая печать данных из сессии

def prim():
    print('Work!')