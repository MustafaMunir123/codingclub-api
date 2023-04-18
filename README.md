
# codingclub-api

## POSTMAN Documentation: https://web.postman.co/workspace/My-Workspace~50cdc6dd-a2ee-4ed7-8db9-3dbe49a15964/documentation/25186829-cff6057f-5afd-42ad-9d84-1e96be9c4110

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

Take latest pull of master branch
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
