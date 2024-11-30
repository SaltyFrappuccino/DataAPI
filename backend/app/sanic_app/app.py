from sanic import Sanic

from backend.app.sanic_app.views import ML_View


application = Sanic("SanicService")
application.add_route(ML_View.as_view(), "/api/ml")
