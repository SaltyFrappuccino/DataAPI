import json
from sanic.views import HTTPMethodView
from sanic.response import json as response_json

from backend.app.sanic_app.ml_modules import ML_AbstractModel
from backend.app.sanic_app.ml_modules.ml_factory import ML_Factory
from backend.app.sanic_app.ml_modules.schemas import ML_ModelSchema


class ML_View(HTTPMethodView):

    def __init__(self):
        super(ML_View, self).__init__()
        self.ml_factory: ML_Factory = ML_Factory()

    async def get(self, request):
        return response_json({"success": False, "message": "method not available"})

    async def post(self, request):
        data = request.json
        ml_model_schema: ML_ModelSchema = self.ml_factory.create(data['model_id'])
        ml_model: ML_AbstractModel = ml_model_schema.ml_model(
            ml_model_schema.ml_model_path,
            ml_model_schema.preprocessor_path
        )
        ml_result = ml_model.make_predictions(data)
        result = json.dumps(ml_result, default=str)
        return response_json({"success": True, 'data': result})

    async def put(self, request):
        return response_json({"success": False, "message": "method not available"})

    async def delete(self, request):
        return response_json({"success": False, "message": "method not available"})
