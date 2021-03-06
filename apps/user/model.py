import datetime
from exts import db

class Friend(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer, db.ForeignKey('user.id'))
    fid = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(12), nullable=False)
    phone = db.Column(db.String(11))
    icon = db.Column(db.String(150))
    isdelete = db.Column(db.Boolean())
    email = db.Column(db.String(100))
    udatetime = db.Column(db.DateTime, default=datetime.datetime.now)
    # 通过user.friends 取user的friends列表
    # 通过friend.user.* 取user的内容
    # 由于friend中有两个外键 所以需要确定取的是Friend.uid的内容
    friends = db.relationship('Friend', backref='user', foreign_keys=Friend.uid)
    def __str__(self):
        return self.username
