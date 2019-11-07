# -*- coding: utf-8 -*-
from app import db


class Douyu(db.Model):
    __tablename__ = 'douyu'

    id = db.Column(db.Integer, primary_key=True, comment='ID')
    # 房间号
    room_number = db.Column(db.Integer, index=True, unique=True, comment='房间号')
    # 房间链接
    room_source = db.Column(db.String(128), comment='房间链接')
    # 房间名
    room_title = db.Column(db.String(128), comment='房间名')
    # 分类
    room_category = db.Column(db.String(64), index=True, comment='分类')
    # 主播
    author = db.Column(db.String(128), index=True, comment='主播')
    # 人气
    popularity = db.Column(db.Integer, comment='人气')
    # 平台
    platform = db.Column(db.Enum('斗鱼TV', '虎牙TV', '熊猫TV', '触手TV', '全民TV', '龙珠TV', '战旗TV',
                                 'YY直播', '繁星直播', 'KK秀', '来疯直播', '么么直播', '六间房', 'AU直播',
                                 '映客直播', '花椒', '章鱼TV', '企鹅TV'), index=True, comment='平台')
    # 是否在播
    is_active = db.Column(db.Boolean, index=True, comment='是否在播')
    # 上次直播时间
    last_active = db.Column(db.DateTime, comment='上次直播时间')
    # 订阅
    subscribe = db.Column(db.Integer, index=True, comment='订阅')
    # 封面
    room_cover = db.Column(db.String(128), comment='封面')

    def __repr__(self):
        return '<Douyu %r>' % str(self.room_number)


class Huya(db.Model):
    __tablename__ = 'huya'

    id = db.Column(db.Integer, primary_key=True, comment='ID')
    # 房间号
    room_number = db.Column(db.Integer, index=True, unique=True, comment='房间号')
    # 房间链接
    room_source = db.Column(db.String(128), comment='房间链接')
    # 房间名
    room_title = db.Column(db.String(128), comment='房间名')
    # 分类
    room_category = db.Column(db.String(64), index=True, comment='分类')
    # 主播
    author = db.Column(db.String(128), index=True, comment='主播')
    # 人气
    popularity = db.Column(db.Integer, comment='人气')
    # 平台
    platform = db.Column(db.Enum('斗鱼TV', '虎牙TV', '熊猫TV', '触手TV', '全民TV', '龙珠TV', '战旗TV',
                                 'YY直播', '繁星直播', 'KK秀', '来疯直播', '么么直播', '六间房', 'AU直播',
                                 '映客直播', '花椒', '章鱼TV', '企鹅TV'), index=True, comment='平台')
    # 是否在播
    is_active = db.Column(db.Boolean, index=True, comment='是否在播')
    # 上次直播时间
    last_active = db.Column(db.DateTime, comment='上次直播时间')
    # 订阅
    subscribe = db.Column(db.Integer, index=True, comment='订阅')
    # 封面
    room_cover = db.Column(db.String(128), comment='封面')

    def __repr__(self):
        return '<Douyu %r>' % str(self.room_number)
