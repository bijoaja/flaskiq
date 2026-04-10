from flask_restful import Resource
from flask import request
from utils import Response
from app.service.api.v1 import CmsApiService


class CmsListResource(Resource):
    def get(self):
        pages = CmsApiService.list_pages(published_only=False)
        return Response().success(values=pages, message="CMS pages")

    def post(self):
        data = request.get_json() or {}
        if not {"title", "slug"}.issubset(data.keys()):
            return Response().invalid(
                is_success=False, values=None,
                message="Fields 'title' and 'slug' are required"
            )
        try:
            page = CmsApiService.create_page(data)
            return Response().success(values=page, message="Page created", code=201)
        except Exception as e:
            return Response().invalid(is_success=False, values=None, message=str(e))


class CmsDetailResource(Resource):
    def get(self, page_id: int):
        page = CmsApiService.get_page(page_id)
        if not page:
            return Response().invalid(
                is_success=False, values=None, message="Page not found", code=404
            )
        return Response().success(values=page, message="Page detail")

    def put(self, page_id: int):
        data = request.get_json() or {}
        page = CmsApiService.update_page(page_id, data)
        if not page:
            return Response().invalid(
                is_success=False, values=None, message="Page not found", code=404
            )
        return Response().success(values=page, message="Page updated")

    def delete(self, page_id: int):
        success = CmsApiService.delete_page(page_id)
        if not success:
            return Response().invalid(
                is_success=False, values=None, message="Page not found", code=404
            )
        return Response().success(values=None, message="Page deleted")
