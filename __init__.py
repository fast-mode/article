from typing import List

from fastapi import APIRouter
from requests.sessions import Session

from app.insmodes.article.route import article_route, article_page_route
from app.models.module import ApiModule, PageModule, PageItem
from app.models.page.crud import PageRouter


class Article(ApiModule, PageModule):
    def _register_page_bp(self, bp: APIRouter, page_router: PageRouter):
        article_page_route(bp, page_router)

    def get_pages(self, db: Session) -> List[PageItem]:
        return []

    def __init__(self):
        super(Article, self).__init__()

    def _register_api_bp(self, bp: APIRouter):
        article_route(bp)

    def _get_tag(self) -> str:
        return '文章'

    def get_module_name(self) -> str:
        return 'article'


article = Article()
