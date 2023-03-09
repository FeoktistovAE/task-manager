### Hexlet tests and linter status:
[![Actions Status](https://github.com/FeoktistovAE/python-project-52/workflows/hexlet-check/badge.svg)](https://github.com/FeoktistovAE/python-project-52/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/4d4da041b1c6b8d9c2ba/maintainability)](https://codeclimate.com/github/FeoktistovAE/python-project-52/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/4d4da041b1c6b8d9c2ba/test_coverage)](https://codeclimate.com/github/FeoktistovAE/python-project-52/test_coverage)

## Description:

["Task Manager"](python-project-52-production-20b1.up.railway.app) is a task management system.
It allows you to set tasks, assign performers and change their statuses.
Registration and authentication are required to work with system.

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
Create '.env' file in the root directory:
```bash
touch .env
```
Add SECRET_KEY variable to the newly created file:
```bash
SECRET_KEY = 'generated secret key'
```
Make migrations:
```bash
make migrations
```
```bash
make migrate
```
Run project:
```bash
make run
```
