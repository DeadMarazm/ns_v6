# ns_v6
1. Библиотеки: requirements/base
pip install -r requirements/base.txt
pip freeze > requirements/base.txt

2. БД старт:
flask db init
flask db migrate
flask db migrate -m "#"
flask db upgrade

3. запуск проекта run.py

Баг в админской части и логика:
1. Открытие http://127.0.0.1:5000/admin/ Работают кнопки "Админка" и "Войти" одинаково
2. Переход  на http://127.0.0.1:5000/admin/login
3. Авторизация как admin в __init__.py функция def create_db_and_admin
4. Переадресация на http://127.0.0.1:5000/admin/
5. Окткрывает шаблон /templates/admin/index.html Должен админ панель

