# HSE Teaching Practices repository

### Installation guide

First, you need to ensure that Python 3.X is installed on your computer/server.

Secondly, you need to install required modules for python:
```sh
# in base repository folder (/HSE_TPR)
pip install -r requirements.txt
```

Then, you need to create and apply migrations to database:
```sh
# in project folder (/HSE_TPR/hse_tpr)
python manage.py makemigrations     # create migrations
python manage.py migrate            # apply migrations
```

After that you can safely run this application with these commands:
```sh
python manage.py runserver
# or if you want to host on certain port
python manage.py runserver <port>
# or if you want to host on certain ip you can youse this command
# (you also need to add this IP in /HSE_TPR/hse_tpr/hse_tpr/settings.py ALLOWED_HOSTS list)
python manage.py runserver <ip>:<port>
```
