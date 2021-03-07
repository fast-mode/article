import os
from . import mdl
from app.models.settings.crud import settings
from app.models.search.crud import db_search

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

    def page(self, db, request, templates, link):
        # try:
            article = db.query(mdl.Article).filter(mdl.Article.link == link).first()
            if article != None:
                self.category_id = article.category_id
                self.db = db
                if os.path.exists("files/templates/article/show.html"):
                    data = {'request':request}
                    data['pageData'] = article.__dict__
                    data['prevData'] = article.__dict__
                    data['nextData'] = article.__dict__
                    data['image'] = self.image
                    data['category'] = self.category
                    data['DB_Search'] = self.db_search
                    print("正常")
                    return templates.TemplateResponse("article/show.html", data)
                else:
                    print("检测出404" + str(article != None) + str(os.path.exists("files/templates/article/show.html")))
                    return templates.TemplateResponse('404.html',{'request':request,'err':"模版不存在"})
            else:
                return templates.TemplateResponse('404.html',{'request':request,'err':"找不到文章"})
        # except Exception as e:
        #     print("发生错误")
        #     print(str(e))
        #     return templates.TemplateResponse('404.html',{'request':request,'err':str(e)})

    def list(self, db, request, templates, category_id, page):
        # try:
            context = db_search(db, "Article", "same_category", 15, [category_id, page])
            # 判断有无
            data = {'request':request}
            data['pageData'] = context
            return templates.TemplateResponse("article/list.html", data)
            
        # except Exception as e:
        #     print(str(e))
        #     return templates.TemplateResponse('404.html',{'request':request,'err':str(e)})