from sanic.views import HTTPMethodView
from sanic.response import json


class ML_View(HTTPMethodView):
    async def get(self, request):
        return json({"success": False, "message": "method not available"})

    async def post(self, request):
        """Обработка POST-запросов"""
        data = request.json
        return json({"success": True, data: data})

    async def put(self, request):
        return json({"success": False, "message": "method not available"})

    async def delete(self, request):
        return json({"success": False, "message": "method not available"})
