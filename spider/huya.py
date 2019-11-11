# @author:林海
# @date:2019-11-07
# -*- coding: utf-8 -*-
import time
from selenium import webdriver
import requests
import json
import re

from app import db
from app.models import Huya


class HuyaSpider(object):
    def __init__(self):
        self.start_rul = 'https://www.huya.com/cache.php?m=LiveList&do=getLiveListByPage&tagAll=0&page='

    def get_room_list(self, url):
        time.sleep(2)
        rooms = []
        data = requests.get(url).text
        room_list = json.loads(data)['data']['datas']
        if len(room_list) <= 1:
            return rooms
        for room in room_list:
            item = {}
            item['room_number'] = int(room['profileRoom'])
            item['room_source'] = 'https://www.huya.com/' + str(room['profileRoom'])
            item['room_title'] = self.change_to_utf8(room['roomName'])
            item['room_category'] = str(room['gameFullName'])
            item['author'] = self.change_to_utf8(room['nick'])
            item['popularity'] = int(room['totalCount'])
            item['platform'] = '虎牙TV'
            item['is_active'] = 1
            item['last_active'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            item['subscribe'] = 0
            item['room_cover'] = self.format_str(room['screenshot'])
            a = Huya(room_number=item['room_number'], room_source=item['room_source'], room_title=item['room_title'],
                     room_category=item['room_category'], author=item['author'], popularity=item['popularity'],
                     platform=item['platform'], is_active=item['is_active'], last_active=item['last_active'],
                     subscribe=item['subscribe'], room_cover=item['room_cover'])
            rooms.append(a)
            # print(room)
        return rooms

    def save_content_list(self, all_rooms):
        # print(all_rooms)
        for room in all_rooms:
            try:
                db.session.add(room)
                db.session.commit()
                print('room ' + str(room.room_number) + ' inserted!')
            except Exception as e:
                # print(e)
                db.session.rollback()
                db.session.query(Huya).filter(Huya.room_number == room.room_number).update(
                    {"room_source": room.room_source,
                     "room_title": room.room_title,
                     "room_category": room.room_category,
                     "popularity": room.popularity,
                     "is_active": room.is_active,
                     "last_active": room.last_active,
                     "room_cover": room.room_cover})
                db.session.commit()
                print('room ' + str(room.room_number) + ' updated!')

    def run(self):
        # 实现主要逻辑
        this_page = 1
        while True:
            rooms = self.get_room_list(self.start_rul + str(this_page))
            print(self.start_rul + str(this_page))
            if len(rooms) < 1:
                print('complete!')
                break
            self.save_content_list(rooms)
            print('the ' + str(this_page) + ' page successed!')
            this_page += 1

    def change_to_utf8(self, str1):
        return str1.encode('utf-8').decode('utf-8')

    def format_str(self, str1):
        return eval(repr(str1).replace('\\', ''))


if __name__ == '__main__':
    douyu = HuyaSpider()
    douyu.run()
