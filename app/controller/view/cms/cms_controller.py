from flask import render_template, abort
from app.service.view.cms_service import CmsService


class CmsView:

    @staticmethod
    def index():
        pages = CmsService.get_published_pages()
        return render_template("cms/index.html", pages=pages)

    @staticmethod
    def page_detail(slug: str):
        page = CmsService.get_page_by_slug(slug)
        if not page:
            abort(404)
        return render_template("cms/detail.html", page=page)
