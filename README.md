
# codingclub-api

## POSTMAN Documentation: https://documenter.getpostman.com/view/25186829/2s93Xzy3LF

### Getting started and running locally:


Make directory
```bash
  mkdir codingclub_api
```
```bash
  cd codingclub_api
```

Initialized empty git repository
```bash
  git init
```

Set remote origin
```bash
  git remote add origin https://github.com/MustafaMunir123/codingclub-api.git
```
------------If above command does not work, then run---------------
```bash
  git pull https://github.com/MustafaMunir123/codingclub-api.git master
```
-----------------------Otherwise-----------------------

```bash
  git pull origin master
```

Install packages
```bash
  pip install -r requirements.txt
```
Make database migrations
```bash
  python manage.py makemigrations
```
```bash
  python manage.py migrate
```

Run django-backend
```bash
  python manage.py runserver
```
