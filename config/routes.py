"""Application roots
"""
from app.apps.auth.views import UserView
from app.apps.base.views import IndexView

routes = [
    ('*', '/user', UserView, 'user'),
    ('*', '/', IndexView, 'index'),
]
