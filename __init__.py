from fastapi import APIRouter
from requests.sessions import Session
from app.insmodes.article.route import article_route, article_page_route
from app.models.module import ApiModule, PageModule, PageItem, TableModule
from app.models.page.crud import PageRouter
from .mdl import Article as MdlArticle


class Article(PageModule, ApiModule, TableModule):
    def get_table(self):
        return [MdlArticle]

    def _register_page_bp(self, bp: APIRouter, page_router: PageRouter):
        article_page_route(bp, page_router)

    def _get_pages(self, db: Session) -> list:
        return []

    def __init__(self):
        super().__init__()

    def _register_api_bp(self, bp: APIRouter):
        article_route(bp)

    def _get_tag(self) -> str:
        return '文章'

    def get_module_name(self) -> str:
        return 'article'


article = Article()
