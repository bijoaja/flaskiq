from app import Resource, Response


class HomeResource(Resource):

    def get(self):
        return Response().success(values=None, message="WELCOME TO API FOR GANESHA AI. VISIT API DOCS: /api/docs")
