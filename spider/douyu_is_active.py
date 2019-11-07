# @author:林海
# @date:2019-11-07
# -*- coding: utf-8 -*-
import time
from selenium import webdriver

from app import db
from app.models import Douyu


class DouyuSpider(object):
    def __init__(self):
        # self.start_rul = 'https://www.douyu.com/directory/all'
        self.driver = webdriver.Chrome(
            executable_path="C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome\\Application\\chromedriver.exe")

    def get_status_and_subscribe(self, room):
        is_active = 1
        subscribe = 0
        url = room.room_source
        self.driver.get(url)
        time.sleep(30)
        last_seen = self.driver.find_elements_by_class_name("Title-lastLiveTimeText")[0].text
        subscribe = self.driver.find_elements_by_class_name("Title-followNum")[0].text
        if last_seen:
            is_active = 0
        db.session.query(Douyu).filter(Douyu.room_number == room.room_number).update(
            {"is_active": is_active, "subscribe": int(subscribe)})
        db.session.commit()
        print(room.room_number, ' updated!')

    def run(self):
        # 实现主要逻辑
        # 发送请求，获取响应
        rooms = Douyu.query.all()
        self.driver.maximize_window()
        for room in rooms:
            self.get_status_and_subscribe(room)


if __name__ == '__main__':
    douyu = DouyuSpider()
    douyu.run()
