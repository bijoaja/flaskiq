from flask import request
from flask_restful import Resource

from utils import Response
from utils.middleware import Middleware
from app.service.view.cms_service import CmsService


class CmsListResource(Resource):

    def get(self):
        pages = CmsService.list_pages()
        return Response().success(is_success=True, values=pages, message="Pages retrieved.")

    @Middleware.token_required
    def post(self, current_user):
        data = request.get_json() or {}
        if not data.get("title") or not data.get("slug"):
            return Response().invalid(
                is_success=False, values=None,
                message="Fields 'title' and 'slug' are required.",
                code=400,
            )
        page = CmsService.create_page(data)
        return Response().success(is_success=True, values=page, message="Page created.", code=201)


class CmsDetailResource(Resource):

    def get(self, page_id: int):
        page = CmsService.get_page(page_id)
        if not page:
            return Response().invalid(is_success=False, values=None, message="Page not found.", code=404)
        return Response().success(is_success=True, values=page, message="Page retrieved.")

    @Middleware.token_required
    def put(self, current_user, page_id: int):
        data = request.get_json() or {}
        page = CmsService.update_page(page_id, data)
        if not page:
            return Response().invalid(is_success=False, values=None, message="Page not found.", code=404)
        return Response().success(is_success=True, values=page, message="Page updated.")

    @Middleware.token_required
    def delete(self, current_user, page_id: int):
        deleted = CmsService.delete_page(page_id)
        if not deleted:
            return Response().invalid(is_success=False, values=None, message="Page not found.", code=404)
        return Response().success(is_success=True, values=None, message="Page deleted.")
