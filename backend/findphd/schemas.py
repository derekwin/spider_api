from ninja.orm import create_schema
from datetime import datetime
from ninja import Schema
from typing import List
from findphd.models import Position, Post, User

Position_schemas = create_schema(Position, exclude=['detail', 'detail_zh'])
Position_detail_schemas = create_schema(Position, exclude=['id'])
Post_schemas = create_schema(Post, exclude=['to'])
User_schemas = create_schema(User, exclude=['code', 'like'])

class Detail_post_schemas(Schema):
    id : int
    detail : str
    to : Post_schemas = None
    post : List[Post_schemas] = None
    creator : User_schemas = None
    timestamp : datetime
    best : str = None

class Create_post(Schema):
    detail : str
    to_id : int
    creator_id : int

class Update_post(Schema):
    id : int
    detail : str
    creator_id : int

class Delete_post(Schema):
    id : int
    creator_id : int

class Add_like_position(Schema):
    position_id : int   # position id

class Create_user(Schema):
    email : str

class Message(Schema):
    message : str 

class Auth(Schema):
    email : str
    code : str