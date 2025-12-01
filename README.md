Music Career - progetto Django

Processo di esecuzione:
. python -m venv venv
2. .\venv\Scripts\activate (Windows) | source venv/bin/activate (Linux)
3. pip install -r requirements.txt
4. python manage.py makemigrations
5. python manage.py migrate
6. python setup_sample.py   # crea account manager1/artist1 e dati di esempio
7. python manage.py runserver

credenziali generate di default con l'esecuzione di setup_sample.py:
- manager1 / managerpass
- artist1 / artistpass

