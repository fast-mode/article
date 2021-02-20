import os
from . import mdl
from app.models.settings.crud import settings

class Render():
    # 现在的分类id 
    category_id = 0
    db = None

    def image(self, im_name):
        return settings.value["domain_port"] + "/photo/" + im_name

    def category(self, count = 10):
        from app.models.tree.crud import get_jsondata
        data = get_jsondata()
        rt = [x["name"] for x in data["children"]]
        if len(rt) > 10:
            return rt[:10]
        else:
            return rt

    # 数据库搜索,
    def find(self, db_name, type, count):
        # 搜索同分类下文章
        if type == "same_category":
            rt = self.db.query(mdl.Article).filter(mdl.Article.category_id == self.category_id).limit(count).all()
            return rt
        else:
            return None

    def page(self, db, request, templates, link):
        try:
            article = db.query(mdl.Article).filter(mdl.Article.link == link).first()
            self.category_id = article.category_id
            self.db = db
            if article != None and os.path.exists("files/templates/article/show.html"):
                data = {}
                data['pageData'] = article.__dict__
                data['prevData'] = article.__dict__
                data['nextData'] = article.__dict__
                data['request'] = request
                data['image'] = self.image
                data['category'] = self.category
                data['find'] = self.find
                print("正常")
                return templates.TemplateResponse("article/show.html", data)
            else:
                print("检测出404" + str(article != None) + str(os.path.exists("files/templates/article/show.html")))
                return templates.TemplateResponse('404.html',{'request':request,'err':"no error"})
        except Exception as e:
            print("错误404")
            return templates.TemplateResponse('404.html',{'request':request,'err':str(e)})

