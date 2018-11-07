"""Application roots
"""
from app.apps.base.views import IndexView

routes = [
    ('*', '/', IndexView, 'index')
]
