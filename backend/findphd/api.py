from typing import List
from ninja import NinjaAPI
from findphd.schemas import Position_schemas, Position_detail_schemas, Message, Post_schemas, Detail_post_schemas, Create_post, Create_user
from findphd.schemas import Auth, Update_post, Delete_post, Add_like_position
from findphd.models import Position, Post, User
from ninja.pagination import paginate
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
import random
from django.core.mail import send_mail

api = NinjaAPI()

@api.get('/latest', response=List[Position_schemas])
@paginate
def latest(request):
    return Position.objects.all()[:100]

@api.get('/detail/{id}', response={200: Position_detail_schemas, 404: Message})
def detail(request, id: int):
    try:
        return 200, Position.objects.get(id=id)
    except Position.DoesNotExist as e:
        return 404, {'message': "not found item"}

@api.get('/latest_post', response=List[Post_schemas])
@paginate
def latest_post(request):
    return Post.objects.all()[:100]

@api.get('/post_detail/{id}', response={200: Detail_post_schemas})
def detail_post(request, id: int):
    return Post.objects.get(id=id)

def create_random_code():
    return str(int(random.random()*1000000))

@api.post('/create_user', response={200: Message, 404: Message})
def create_user(request, payload : Create_user):
    try:
        if User.objects.filter(email=payload.email):
            send_mail(
                    f'[findphd] 是您吗？',
                    f'您的邮箱 {payload.email} 正在我们的网站findphd重复创建用户，系统已经拦截，请确保这是您。\n 如果这是您，且您登录遇到问题，请重置code。',
                    'geekboxclub@126.com',
                    [payload.email],
                    fail_silently=False,
                )
            return 200, {'message': "already"}
        new_user = User.objects.create(**payload.dict())
        new_user.code = create_random_code()
        new_user.save()
        try:
            send_mail(
                    f'[findphd] 注册成功',
                    f'您正在findphd网站创建账号，本网站不要求您设置任何密码和个人信息。\n code:{new_user.code} \n将作为您暂时的使用权限凭证，您可以之后随时更新该code。',
                    'geekboxclub@126.com',
                    [payload.email],
                    fail_silently=False,
                )
        except Exception as e:
            return 404, {"message": '邮箱配置错误，但您的用户的已经创建成功，请重置code获取您的登录凭证。'}
        return 200, {'message': "success:"+str(new_user.id)}
    except Exception as e:
        return 404, {"message": str(e)}

@api.post('/update_code', response={200: Message, 404: Message})
def update_code(request, email:str):
    try:
        user = get_object_or_404(User, email=email)
        if user:
            user.code = create_random_code()
            try:
                send_mail(
                        f'[findphd] Your Code : {user.code}',
                        f'您的code重置成功，新code如下：\n code:{user.code} \n您可以之后随时更新该code。',
                        'geekboxclub@126.com',
                        [email],
                        fail_silently=False,
                    )
            except Exception as e:
                return 404, {"message": '邮箱配置错误，这可能是我们的问题，您可以稍后再试。'}
            user.save()
            return 200, {'message': "update code success:"+str(user.id)}
    except Exception as e:
        return 404, {"message": str(e)}

def auth_user(auth : Auth):
    user = User.objects.filter(email=auth.email)
    if len(user)>0 and auth.code == user[0].code:
        return True
    else:
        return False

@api.post('/create_post', response={200: Message, 404: Message})
def create_post(request, auth:Auth, payload : Create_post):
    try:
        if auth_user(auth):
            new_post = Post.objects.create(detail=payload.detail)
            new_post.creator = get_object_or_404(User, pk=payload.creator_id)
            if new_post.creator.email == auth.email:
                if payload.to_id is not None:
                    new_post.to = get_object_or_404(Post, pk=payload.to_id)
                new_post.save()
                return 200, {'message': "success:"+str(new_post.id)}
            else:
                return 404, {"message": "creator must is you"}
        else:
            return 404, {"message": "auth failed"}
    except Exception as e:
        return 404, {"message": "Error"}

@api.post('/update_post', response={200: Message, 404: Message})
def update_post(request, auth:Auth, payload:Update_post):
    try:
        if auth_user(auth):
            user = get_object_or_404(User, email=auth.email)
            creator = get_object_or_404(User, pk=payload.creator_id)
            if user == creator:
                new_post = get_object_or_404(Post, pk=payload.id)
                new_post.detail = payload.detail
                new_post.save()
                return 200, {'message': "update success:"+str(new_post.id)}
            else:
                return 404, {"message": "you are not the creator"}
        else:
            return 404, {"message": "auth failed"}
    except Exception as e:
        return 404, {"message": "Error"}

@api.post('/delete_post', response={200: Message, 404: Message})
def delete_post(request, auth:Auth, payload:Delete_post):
    try:
        if auth_user(auth):
            user = get_object_or_404(User, email=auth.email)
            creator = get_object_or_404(User, pk=payload.creator_id)
            if user == creator:
                new_post = get_object_or_404(Post, pk=payload.id)
                new_post.delete()
                return 200, {'message': "delete success"}
            else:
                return 404, {"message": "you are not the creator"}
        else:
            return 404, {"message": "auth failed"}
    except Exception as e:
        return 404, {"message": "Error"}

@api.post('/add_like', response={200: Message, 404: Message})
def add_like_position(request, auth:Auth, payload:Add_like_position):
    try:
        if auth_user(auth):
            user = get_object_or_404(User, email=auth.email)
            position = get_object_or_404(Position, pk=payload.position_id)
            user.like.add(position)
            user.save()
            return 200, {'message': "add success"}
        else:
            return 404, {"message": "auth failed"}
    except Exception as e:
        return 404, {"message": "Error"}

@api.post('/delete_like', response={200: Message, 404: Message})
def delete_like_position(request, auth:Auth, payload:Add_like_position):
    try:
        if auth_user(auth):
            user = get_object_or_404(User, email=auth.email)
            position = get_object_or_404(Position, pk=payload.position_id)
            user.like.remove(position)
            user.save()
            return 200, {'message': "delete success"}
        else:
            return 404, {"message": "auth failed"}
    except Exception as e:
        return 404, {"message": "Error"}

@api.post('/my', response=List[Position_schemas])
@paginate
def my_like(request, auth:Auth):
    if auth_user(auth):
        user = get_object_or_404(User, email=auth.email)
        return user.like.all()
    else:
        return []
