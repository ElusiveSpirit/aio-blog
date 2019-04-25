Async REST blog API
==========
[![Build Status](https://travis-ci.org/ElusiveSpirit/aio-blog.svg?branch=master)](https://travis-ci.org/ElusiveSpirit/aio-blog)

Using the AioHTTP python framework

## Requeirement

- Python 3.6
- MongoDB

## Setup

Run in terminal

```bash
pipenv install
```

## Basic usage

There is a commands.py file close enough to Django manage.py. Usage is to run `pipenv run ./commands.py <command>`:

- runserver - Starts server with AioHTTP run_app. Not so cool like aiohttp-devtools runserver. 
- shell - Python or IPython interactive shell with set up app.
- test - Run tests.
- clear_collection - Clear Mongo collection. Mostly used for testing.
