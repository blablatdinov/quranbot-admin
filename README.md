# Как пользоваться?

```
python3.9 -m venv venv
pip install -r requirements.txt
```

Можно удалить директорию blog, и стереть из INSTALLED_APPS

Запуск тестов:

```
task test
# или
pytest
```

Запуск сортировки импортов и линтера

```
task lint
# или
isort . && flake8 .
```

Создать файл переводов:

```bash
./manage.py makemessages -l ru
./manage.py compilemessages
```
