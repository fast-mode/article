import os
from . import mdl
from app.models.settings.crud import settings
from app.models.search.crud import db_search
from app.models.page.crud import Page
from app.models.assets.crud import Assets

class Render():
    # 现在的分类id 
    category_id = 0
    db = None

    def image(self, im_name):
        return ""
        # return settings.value["domain_port"] + "/photo/" + im_name

    def category(self, count = 10):
        from app.models.tree.crud import get_jsondata
        data = get_jsondata()
        rt = [x["name"] for x in data["children"]]
        if len(rt) > 10:
            return rt[:10]
        else:
            return rt

    # 数据库搜索,
    def db_search(self, db_name, type, count):
        return db_search(self.db, db_name, type, count, [self.category_id])

    def page(self, db, request, link):
        pg = Page(request)
        # try:
        article = db.query(mdl.Article).filter(mdl.Article.link == link).first()
        if article != None:
            self.category_id = article.category_id
            self.db = db
            data = {}
            data['pageData'] = article.__dict__
            data['prevData'] = article.__dict__
            data['nextData'] = article.__dict__
            data['image'] = Assets.get_link_prefix(article.image)
            data['category'] = self.category
            data['DB_Search'] = self.db_search
            return pg.show_page("article/show.html", data)
        else:
            return pg.show_404_page("找不到文章")  # templates.TemplateResponse('404.html',{'request':request,'err':"找不到文章"})
        # except Exception as e:
        #     print("发生错误")
        #     print(str(e))
        #     return templates.TemplateResponse('404.html',{'request':request,'err':str(e)})

    def list(self, db, request, category_id, page):
        pg = Page(request)
        context = db.query(mdl.Article).filter(mdl.Article.category_id == category_id).limit(10).all()
        # 判断有无
        data = {}
        data['image'] = "暂未有数据"
        data['pageData'] = context
        data['category'] = self.category
        data['DB_Search'] = self.db_search
        return pg.show_page("article/list.html", data)

    def commit_data_insert(self, context):
        rt = {}
        rt['image'] = context.image
