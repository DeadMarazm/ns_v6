# ns_v6
pip install -r requirements/base.txt
pip freeze > requirements/base.txt

1. Библиотеки: requirements/base
2. БД старт:
flask db init
flask db migrate
flask db migrate -m "#"
flask db upgrade
3. запуск проекта run.py
4. в /app все кишки.

GitHub

