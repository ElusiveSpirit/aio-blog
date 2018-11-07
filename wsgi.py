"""wsgi.py entry point"""
from aiohttp.web import run_app

from app.app import create_app

app = create_app()

if __name__ == '__main__':
    run_app(app)
