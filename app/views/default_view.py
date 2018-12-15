from flask import redirect, Flask, url_for
from flask.views import MethodView
from flask_login import logout_user


def add_routes(app: Flask):
    app.add_url_rule('/', view_func=DefaultView.as_view('index'))


class DefaultView(MethodView):

    def get(self):
        return redirect(url_for('categories_view'))
