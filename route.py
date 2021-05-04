from HtmlCreator import Html
from HtmlCreator.Body.Image import Image

from app.models.page.crud import Page
from fastapi import APIRouter, HTTPException, Depends, Header, Request
from enum import Enum
from sqlalchemy.orm import Session
from app.models.mdl import database
from . import orm, crud, mdl
from app.models.system import token
from app.models.user.mdl import User
from ...models.assets.crud import Assets
from ...models.template.Template import Template

bp = APIRouter()


# bp.route('/view')

# 文章状态枚举


class ArticleStatus(str, Enum):
    trash = 'trash'
    outline = 'outline'
    online = 'online'
    noseacrh = 'noseacrh'
    all = 'all'

    def toInt(self):
        if self == self.trash:
            return 0
        elif self == self.outline:
            return 1
        elif self == self.online:
            return 2
        elif self == self.noseacrh:
            return 3
        else:
            return 10


# create


@bp.post('/create', description='创建文章')
def create(
        article: orm.ArticleCreate,
        now_user: User = Depends(token.get_token_func()),
        db: Session = Depends(database.get_db)):
    #
    now_user.into_auth("arti_edit_self")
    return crud.create(db, article, now_user.id)


# update


@bp.put('/update', description='更更更更更更新')
def update(
        article: orm.ArticleUpdate,
        now_user: User = Depends(token.get_token_func()),
        db: Session = Depends(database.get_db)):
    # 如果有编辑所有权限
    # if now_user.check_auth(9):
    # TODO
    now_user.into_auth("arti_edit_self")
    return crud.update(db, article)
    # else:
    #     owner_id = crud.get_owner_id(db,article.id)
    #     if owner_id == now_user.id:
    #         return crud.update(db,article)
    #     else:
    #         raise HTTPException(status_code=403,detail='权限不足')


# release


@bp.put('/release', description='发布,true为可检索false为不可检索')
def release(
        article: orm.ArticleRelease,
        now_user: User = Depends(token.get_token_func()),
        db: Session = Depends(database.get_db)):
    #
    owner_id = crud.get_owner_id(db, article.id)
    if owner_id == now_user.id:
        return crud.release(db, article)
    else:
        raise HTTPException(status_code=403, detail='权限不足')


# release


@bp.put('/to_outline', description='将文章变回草稿,不论它在哪')
def to_outline(
        article_id: int,
        now_user: User = Depends(token.get_token_func()),
        db: Session = Depends(database.get_db)):
    #
    owner_id = crud.get_owner_id(db, article_id)
    if owner_id == now_user.id:
        return crud.return_to_outline(db, article_id)
    else:
        raise HTTPException(status_code=403, detail='权限不足')


# read


@bp.get('/self/articles/{status}',
        description='读取自己的文章,注意在url中加入状态,trash垃圾箱 outline草稿箱 online已发布 noseacrh已发布不索引 all全部,索引分别为0,1,2,3,10')
def read_self_all(
        status: ArticleStatus,
        now_user: User = Depends(token.get_token_func()),
        db: Session = Depends(database.get_db),
):
    # print(status.toInt())
    return crud.get_user_articles(db, now_user, status.toInt())


# read_all


@bp.get('/all/articles', description='读取所有的文章,admin的权限')
def read_all_of_the_server(
        now_user: User = Depends(token.get_token_func()),
        db: Session = Depends(database.get_db),
):
    #
    now_user.into_auth("arti_edit_all")
    return crud.get_all_articles(db)


@bp.get('/self/readone/{id}', description='读取一篇文章')
def read_one(
        id,
        now_user: User = Depends(token.get_token_func()),
        db: Session = Depends(database.get_db), ):
    #
    if crud.get_owner_id(db, id) == now_user.id:
        return crud.read_one_page(db, id)
    else:
        raise HTTPException(status_code=403, detail='权限不足')


@bp.delete('/delete/{id}', description='假的删除,假的!')
def delete(
        id: int,
        now_user: User = Depends(token.get_token_func()),
        db: Session = Depends(database.get_db)):
    # 如果拥有编辑全部文章的权限
    if now_user.check_auth(9):
        return crud.delete(db, id)
    else:
        # 否则按正常套路来
        article_owner_id = crud.get_owner_id(db, id)
        if article_owner_id == now_user.id:
            return crud.delete(db, id)
        else:
            raise HTTPException(status_code=403, detail='权限不足')


@bp.delete('/real_delete/{id}', description='真正删除,,(真的吗?)')
def real_delete(
        id: int,
        now_user: User = Depends(token.get_token_func()),
        db: Session = Depends(database.get_db)):
    # 如果拥有编辑全部文章的权限
    if now_user.check_auth(9):
        return crud.real_delete(db, id)
    else:
        # 否则按正常套路来
        article_owner_id = crud.get_owner_id(db, id)
        if article_owner_id == now_user.id:
            return crud.real_delete(db, id)
        else:
            raise HTTPException(status_code=403, detail='权限不足')


# 下面是关于页面渲染的代码
pg_bp = APIRouter()
p = Page()


def get_show_creator():
    rt = Html('默认文章页面')
    rt.body.addElement('成功进入{{ pageData.link }}页面 图片:')\
        .addElement(Image('{{ image }}'))
    return rt


@pg_bp.get('/show/{params:path}', description='参数只有一个:link(暂时为id)')
@p.wrap()
def show(db, link: str):
    article: mdl.Article = db.query(mdl.Article).filter(mdl.Article.link == link).first()
    if article is not None:
        data = {'pageData': article.__dict__,
                'prevData': article.__dict__,
                'nextData': article.__dict__,
                'image': Assets.path_to_link(article.image),
                'category': article.category_id,
                # 'DB_Search': self.db_search,
                }
        return 'article/show.html', data, get_show_creator


def get_category_list_creator():
    rt = Html('分类列表页面')
    rt.body.addElement('成功进入分类列表页面')
    return rt


@pg_bp.get('/list/{params:path}', description='参数有一个:category_id')
@p.wrap()
def list_in_category(db, category_id: str):
    context = db.query(mdl.Article).filter(mdl.Article.category_id == category_id).limit(10).all()
    data = {
        'image': "暂未有数据",
        'pageData': context,
        # 'category': self.category,
        # 'DB_Search': self.db_search
    }
    return 'article/list.html', data, get_category_list_creator
