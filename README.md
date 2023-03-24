### Hexlet tests and linter status:
[![Actions Status](https://github.com/FeoktistovAE/python-project-52/workflows/hexlet-check/badge.svg)](https://github.com/FeoktistovAE/python-project-52/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/4d4da041b1c6b8d9c2ba/maintainability)](https://codeclimate.com/github/FeoktistovAE/python-project-52/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/4d4da041b1c6b8d9c2ba/test_coverage)](https://codeclimate.com/github/FeoktistovAE/python-project-52/test_coverage)

## Description:

"Task Manager" is a task management system.
It allows you to set tasks, assign performers and change their statuses.
Registration and authentication are required to work with system.

#### Stack:
* Python 3
* Django
* django-bootstrap4
* Rollbar
* Pytest
* python-dotenv
* CI/CD (Github actions)
* Flake8(PEP 8)
* gunicorn
* Railway

#### Installation:
Clone repository:
```bash
git clone https://https://github.com/FeoktistovAE/python-project-52
```

Enter the root folder:
```bash
cd python-project-52
```
Install dependencies via Poetry:
```bash
make install
```
Change the name of '.env.sample' file to '.env':
```bash
mv .env.sample .env
```
Add your django secret key and rollbar token to the .env file:
```bash
SECRET_KEY = 'generated secret key'
ROLLBAR_TOKEN = 'generated Rollbar token'
```
Make migrations:
```bash
make migrations
```
```bash
make migrate
```
Run server:
```bash
make run
```
