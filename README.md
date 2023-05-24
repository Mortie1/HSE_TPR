# HSE Teaching Practices repository

## Installation guide


### Way 1: Django

1.    Ensure that Python 3.X is installed on your computer/server. You can check that by running in terminal:
      ```sh
      # windows
      python --version

      #linux
      python3 --version
      ```
      If python is not installed, follow the [official guide](https://wiki.python.org/moin/BeginnersGuide/Download) 

2.    Install required modules for python:
      ```sh
      # in base repository folder (/HSE_TPR)
      pip install -r requirements.txt
      ```

3.    Create and apply migrations to database:
      ```sh
      # in project folder (/HSE_TPR/hse_tpr)
      python manage.py makemigrations     # create migrations
      python manage.py migrate            # apply migrations
      ```

5.    Create .env file in project folder (/HSE_TPR/hse_tpr) with following contents:
      ```sh
      SECRET_KEY='your-secret-key'    # if you don't have one, you can obtain it
                                      # by creating your own django project and
                                      # getting it from settings.py
      ```

4.    Now you can safely run this application with these commands:
      ```sh
      python manage.py runserver

      # or if you want to host on certain port
      python manage.py runserver <port>

      # or if you want to host on certain ip you can youse this command
      # (you also need to add this IP in /HSE_TPR/hse_tpr/hse_tpr/settings.py ALLOWED_HOSTS list)
      python manage.py runserver <ip>:<port>
      ```
      You will get output like this:
      ```sh
      Watching for file changes with StatReloader
      Performing system checks...

      System check identified no issues (0 silenced).
      May 24, 2023 - 13:10:44
      Django version 4.2.1, using settings 'hse_tpr.settings'
      Starting development server at http://<ip>:<port>/
      Quit the server with CONTROL-C.
      ```
      Now you can view website by following the link http://\<ip\>:\<port\>/ in your web-browser

### Way 2: Docker

1.    Check if Docker and docker-compose are installed on your device by running in terminal: 
      ```sh
      docker --version
      docker-compose --version
      ```
      If Docker or docker-compose are not installed - follow the [official guides](https://docs.docker.com/)
2.    Create .env.dev, .env.prod and .env.prod.db files in base repository folder (/HSE_TPR) with following contents:
      ```sh
      # .env.dev:
      DEBUG=1
      SECRET_KEY='your-secret-key'
      DJANGO_ALLOWED_HOSTS='127.0.0.1 localhost your.ip'
      SQL_ENGINE=django.db.backends.postgresql
      SQL_DATABASE=hse_tpr_dev
      SQL_USER=hse_tpr
      SQL_PASSWORD=hse_tpr
      SQL_HOST=db
      SQL_PORT=5432
      DATABASE=postgres
      
      # .env.prod:
      DEBUG=0
      SECRET_KEY='your-secret-key'
      DJANGO_ALLOWED_HOSTS='127.0.0.1 localhost your.ip'
      SQL_ENGINE=django.db.backends.postgresql
      SQL_DATABASE=hse_tpr_prod
      SQL_USER=hse_tpr
      SQL_PASSWORD=hse_tpr
      SQL_HOST=db
      SQL_PORT=5432
      DATABASE=postgres
      
      # .env.prod.db
      POSTGRES_USER=hse_tpr
      POSTGRES_PASSWORD=hse_tpr
      POSTGRES_DB=hse_tpr_prod
      ```
3.    Now you can run docker-compose images by running following command:
      ```sh
      docker-compose -f docker-compose.yml up -d --build        # dev version
      # or
      docker-compose -f docker-compose.prod.yml up -d --build   # prod version (with gunicorn and nginx)
      ```
4.    Access the website via [localhost:7777](http://localhost:7777/) or \<your-ip\>:7777 in web browser

## Usage guide
