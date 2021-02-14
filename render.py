import os
from . import mdl
from app.models.settings.crud import settings

def image(im_name):
    return settings.value["domain_port"] + "/photo/" + im_name

# def category

def page(db, request, templates, link):
    try:
        article = db.query(mdl.Article).filter(mdl.Article.link == link).first()
        if article != None and os.path.exists("files/templates/article/show.html"):
            data = {}
            data['pageData'] = article.__dict__
            data['prevData'] = article.__dict__
            data['nextData'] = article.__dict__
            data['request'] = request
            data['image'] = image
            print("正常")
            return templates.TemplateResponse("article/show.html", data)
        else:
            print("检测出404" + str(article != None) + str(os.path.exists("files/templates/article/show.html")))
            return templates.TemplateResponse('404.html',{'request':request,'err':"no error"})
    except Exception as e:
        print("错误404")
        return templates.TemplateResponse('404.html',{'request':request,'err':str(e)})

