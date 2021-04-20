import os
from flask import Blueprint, url_for
from flask_restful import Resource, marshal_with, fields, reqparse, inputs, marshal
from werkzeug.datastructures import FileStorage
from apps.user.model import User,Friend
from exts import api, db
from settings import Config

# 创建蓝图
user_bp = Blueprint('user', __name__, url_prefix='/api')
# http://127.0.0.1:5000/api/
# <Rule '/api/' (HEAD, OPTIONS, GET) -> user.user_center>
@user_bp.route('/')
def user_center():
    return 'hello'

# 定义返回数据的格式 键为model里面的name 也为返回前端的name
# user_fields = {
#     'id': fields.Integer,
#     'username': fields.String,
#     'password': fields.String,
#     'udatetime': fields.DateTime
# }

# 定制显示fields方法 继承Raw 重写format方法
class IsDelete(fields.Raw):
    def format(self, value):
        # print('------------------>', value)  # False/True
        return '删除' if value else '未删除'


# get "http://127.0.0.1:5000/user/1" 返回详情
# 定义返回数据的格式 键为model里面的name
user_fields = {
    'id': fields.Integer,
    # 取数据库username的值 若无 默认为匿名 返回前端为name
    'name': fields.String(attribute='username',default='匿名'),
    'pwd': fields.String(attribute='password'),
    'isDelete': fields.Boolean(attribute='isdelete'),
    # 定制fields方法
    '是否删除': IsDelete(attribute='isdelete'),
    'udatetime': fields.DateTime(dt_format='rfc822')
}

# get "http://127.0.0.1:5000/user" 返回 userlist ----->点击具体的一个获取详情 ------> 详情
user_fields_1 = {
    'id': fields.Integer,
    'username': fields.String(default='匿名'),
    'uri': fields.Url('single_user', absolute=True) # "http://127.0.0.1:5000/user/1"
    # 若无absolute=True 返回 /user/1
}

# 参数解析 后端确认设置的字段前端是否提交 不可多加也不可少写
# bundle_errors=True 所有的错都报错，默认为False 只报第一个错误
parser = reqparse.RequestParser(bundle_errors=True)  # 解析对象
# request.form.get()  | request.args.get() | request.cookies.get() | request.headers.get() 对应于
# location=['form']   | location=['args']  |location=['cookies']   |location=['headers'] |location=['files']

# name type required 提示信息 参数取值方式
parser.add_argument('username', type=str, required=True, help='必须输入用户名', location=['form'])
# 正则inputs.regex 验证字符串
parser.add_argument('password',type=inputs.regex(r'^\d{6,12}$'), required=True, help='必须输入6~12位数字密码',location=['form'])
parser.add_argument('phone',type=inputs.regex(r'^1[356789]\d{9}$'),location=['form'], help='手机号码格式错误')
# 允许此字段有多个值存在
parser.add_argument('hobby', action='append')  # 在postman中添加的多个以hobby为key的值以列表形式返回
# 文件上传 必须设置type=FileStorage, location=['files']
parser.add_argument('icon', type=FileStorage,location=['files'])


# 定义类视图继承Resource  postman携带数据读取
class UserResource(Resource):
    # 定义get请求的处理
    @marshal_with(user_fields_1) # 也适用于列表 定制返回值格式
    def get(self):
        # 浏览器 访问 http://127.0.0.1:5000/user 出现msg	"------>get" 因为浏览器是get请求
        # 模拟post put delete操作需要进入postman
        # return {'msg': '------>get'}
        users = User.query.all()

        # 对自定义的类无法直接序列化，使用marshal_with自定义返回数据格式
        # userList = []
        # for user in users:
        #     # userList.append(user) # Object of type User is not JSON serializabl
        #     userList.append(user.__dict__) # 对象有__dict__属性  Object of type InstanceState is not JSON serializable
        # return userList

        return users

    # 定义post请求的处理
    @marshal_with(user_fields)
    def post(self):
        # 获取数据
        args = parser.parse_args( )
        username = args.get('username')
        password = args.get('password')
        phone = args.get('phone')
        hobby = args.get('hobby') # ['篮球', '皮球']
        icon = args.get('icon') # <FileStorage: 'gjjxj.jpg' ('image/jpeg')>
        # 创建user对象
        user = User( )
        user.username = username
        user.password = password
        if icon:
            upload_path = os.path.join(Config.UPLOAD_ICON_DIR, icon.filename)
            icon.save(upload_path)
            # 保存路径
            user.icon = os.path.join('upload','icon', icon.filename)
        if phone:
            user.phone = phone
        db.session.add(user)
        db.session.commit( )
        return user

    # 定义put请求的处理
    def put(self):
        return {'msg': '------>put'}

    # 定义delete请求的处理
    def delete(self):
        return {'msg': '------>delete'}


# 定义传参测试类 http://127.0.0.1:5000/user/1
class UserSimpleResource(Resource):
    @marshal_with(user_fields)  # 将user转成一个序列化的对象，
    def get(self, id):
        user = User.query.get(id)
        return user

    def put(self, id):
        print('endpoint的使用：', url_for('all_user')) # endpoint的使用： /user
        return {'msg': 'ok'}

    def delete(self, id):
        pass


user_friend_fields = {
    'username': fields.String,
    'nums': fields.Integer,
    # Allows you to nest one set of fields inside another
    # 声明这条记录放列表 列表里面为user_fields格式
    'friends': fields.List(fields.Nested(user_fields))
}

class UserFriendResource(Resource):
    @marshal_with(user_friend_fields)
    def get(self, id):
        friends = Friend.query.filter(Friend.uid == id).all()
        user = User.query.get(id)

        friend_list = []
        for friend in friends:
            u = User.query.get(friend.fid)
            friend_list.append(u)

        data = {
            'username': user.username,
            'nums': len(friends),
            'friends': friend_list  # 套叠结构 [user,user,user] not JSON serializable 需要结合marshal_with(user_friend_fields)使用
            # 'friends': marshal(friend_list,user_fields) # 用user_fields格式化friend_list后返回
        }
        return data


# 将类加入到api中 会出现路由[<Rule '/user' (POST, HEAD, DELETE, OPTIONS, GET, PUT) -> userresource>,...]
# 访问 http://127.0.0.1:5000/user
api.add_resource(UserResource, '/user', endpoint='all_user')
# 添加路径传参类
# 访问 http://127.0.0.1:5000/user/1
api.add_resource(UserSimpleResource, '/user/<int:id>', endpoint='single_user')

api.add_resource(UserFriendResource, '/friend/<int:id>', endpoint='user_friend')
# python app.py runserver启动