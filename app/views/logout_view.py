from flask import redirect, Flask
from flask.views import MethodView
from flask_login import logout_user

def add_routes(app: Flask):
    app.add_url_rule('/logout', view_func = LogoutView.as_view('logout_view'))

class LogoutView(MethodView):

    def get(self):
        logout_user()
        return redirect('/')
