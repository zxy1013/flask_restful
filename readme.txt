安装
  pip install flask-restful
手册参照
  https://flask-restful.readthedocs.io/en/latest/

RESTful(表现层状态转化) adds support for quickly building REST APIs
rest api是前后端分离的最佳实践，是开发的一套标准或规范，不是框架。
1、轻量，直接通过http，不需要额外的协议，通常有post/get/put/delete操作。http协议无状态，所有状态均保存在服务器端。
2、面向资源，请求即会返回数据链接URI。
3、数据描述简单，通过json(后端向前端返回数据)或者xml(ajax请求 前端向后端)做数据通讯。

RESTful架构
（1）每一个URI代表一种资源，要获取这个资源，访问它的URI就可以，因此URI就成了每一个资源的地址或独一无二的识别符。
（2）是客户端和服务器之间，传递这种资源的某种表现层；
（3）客户端通过四个HTTP动词(GET获取资源,POST新建资源,PUT更新资源,DELETE删除资源,[PATCH])，对服务器端资源进行操作，实现"表现层状态转化"。

使用Postman模拟前端api客户端展示,不使用html页面,可能会有静态的交互,比如图片等。
下载 https://www.postman.com/downloads/
C:\Users\Administrator\AppData\Local\Postman\Postman.exe中，登录后进入初始界面
可以设置get或者post等请求 并相应添加请求头及请求体


REST前后端分离：
前端：app，小程序，pc页面
后端：没有页面，围绕mv实现：模型 视图
  视图：使用api构建视图

  exts的init创建api对象
  api = Api()
  apps的init初始化api对象
  api.init_app(app=app)

  定义类视图：
  from flask_restful import Resource
  class UserResource(Resource):
    # 定义get请求的处理
    @marshal_with(user_fields) # 也适用于列表 定制返回值格式
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
    def post(self):
        return {'msg': '------>post'}

    # 定义put请求的处理
    def put(self):
        return {'msg': '------>put'}

    # 定义delete请求的处理
    def delete(self):
        return {'msg': '------>delete'}

  绑定,将类加入到api中,使用http://127.0.0.1:5000/user访问
  api.add_resource(UserResource,'/user')

flask url传参
  http://127.0.0.1:5000/user?id = 1
  @app.route('/user/')
  def user():
    id = request.args.get('id')

  http://127.0.0.1:5000/user/1
  @app.route('/user/<id>/')
  def item(id):
     return 'user{}详情'.format(id)


api class类url传参
  http://127.0.0.1:5000/user/1
  # 定义传参测试类
  class UserSimpleResource(Resource):
    @marshal_with(user_fields)  # 将user转成一个序列化的对象，
    def get(self, id):
        user = User.query.get(id)
        return user

    def put(self, id):
        # 使用endpoint找路由
        print('endpoint的使用：', url_for('all_user')) # endpoint的使用： /user
        return {'msg': 'ok'}

    def delete(self, id):
        pass

  api.add_resource(UserResource, '/user', endpoint='all_user')
  api.add_resource(UserSimpleResource, '/user/<int:id>', endpoint='single_user')
  # put访问 http://127.0.0.1:5000/user/1


postman
    Params中的参数添加是添加到url上的
    Body中的参数添加是请求体的内容传输
    纯文本添加选择x-www-form 有文件的选择form-data form-data的key栏中可以选择text/file
    当add_argument中没有限制location=['form']时，两种方式均可传值，但是设置后会只接受body中的传值


api class类请求参数传入post
    创建RequestParser对象：
    parser = reqparse.RequestParser(bundle_errors=True)
    给解析器添加参数：
    通过parser.add_argument('名字'，type=类型，required=是否必须填写，help=错误的提示信息，location=表明获取的位置 form就是post表单提交)
    type的位置可以添加一些正则的验证。
    例如：
    parser.add_argument('password', type=inputs.regex(r'^\d{6,12}$'), required=True, help='必须输入6~12位数字密码',location=['form'])
    在请求的函数中获取数据：
    可以在get，post，put等中获取数据，通过parser对象.parse_args()
    args = parser.parse_args() # args是一个字典底层的结构，因此获取具体的数据时可以通过get
    password = args.get('password')


结果返回前端
定义字典，字典的格式就是给客户端看的格式
user_fields = {
    'id': fields.Integer,
    # 取数据库username的值 若无 默认为匿名 返回前端为name
    'name': fields.String(attribute='username',default='匿名'),
    'pwd': fields.String(attribute='password'),
    'udatetime': fields.DateTime(dt_format='rfc822')
}
客户端能看到的是：id，username，pwd，udatetime这四个key
默认key的名字是跟model中的模型属性名一致，如果不想让前端看到命名，则可以修改结合attribute='模型的字段名'

自定义fields 继承Raw 重写方法format
class IsDelete(fields.Raw):
    def format(self, value):
        return '删除' if value else '未删除'
user_fields = {
    '是否删除': IsDelete(attribute='isdelete'),
}

# get "http://127.0.0.1:5000/user" 返回 userlist ----->点击具体的一个获取详情 ------> 详情
定义两个user_fields
    1.用于获取用户的列表信息结构的fields：
    user_fields_1 = {
        'id': fields.Integer,
        'username': fields.String(default='匿名'),
        'uri': fields.Url('single_user', absolute=True)  # 参数使用的就是endpoint的值 产生一个个的链接
    }

    2.具体用户信息展示的fields
    user_fields = {
        'id': fields.Integer,
        'username': fields.String(default='匿名'),
        'pwd': fields.String(attribute='password'),
        'isDelete': fields.Boolean(attribute='isdelete'),
        'isDelete1': IsDelete(attribute='isdelete'),
        'udatetime': fields.DateTime(dt_format='rfc822')
    }
    # 此时id需要与fields中的数据name一致，不然无法拼接url
    api.add_resource(UserSimpleResource, '/user/<int:id>', endpoint='single_user')

return data 套叠结构
    data必须是符合json格式
    {
      'aa':10,
      'bb':[
         {
           'id':1,
           'friends':[
                    {},{}
                  ]
         },
         。。。
      ]
    }
    如果想要直接返回，则里面不能有自定义的对象，否则not JSON serializable
    如果有这种对象，需要使用marchal()或 marchal_with()帮助进行转换。
    1 marshal(friend_list,user_fields) # 用user_fields格式化friend_list后返回 字典的输出格式
    2 marchal_with() 作为装饰器修饰请求方法
        @marshal_with(user_friend_fields)
        def get(self, id):
            ...
            return data
    例如：
    user_friend_fields = {
        'username': fields.String,
        'nums': fields.Integer,
        'friends': fields.List(fields.Nested(user_fields))
    }
    fields.Nested(fields.String) ----> ['str1','str2','str3']
    fields.Nested(user_fields)  ----> user_fields是一个字典结构，将里面的每一个对象转成user_fields结构