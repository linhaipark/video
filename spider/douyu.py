import time
from selenium import webdriver
import requests
import json
import re

from app import db
from app.models import Douyu


class DouyuSpider_no(object):
    def __init__(self):
        self.start_rul = 'https://www.douyu.com/directory/all'
        self.driver = webdriver.Chrome(
            executable_path="C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome\\Application\\chromedriver.exe")

    def get_room_list(self):
        time.sleep(10)
        li_list = self.driver.find_elements_by_xpath('//ul[@class="layout-Cover-list"]/li')
        rooms = []
        for li in li_list:
            item = {}
            item['room_source'] = li.find_element_by_xpath('.//a[@class="DyListCover-wrap"]').get_attribute('href')
            item['room_number'] = int(item['room_source'].split('/')[3])
            item['room_title'] = li.find_element_by_xpath('.//h3[@class="DyListCover-intro"]').text
            item['room_category'] = li.find_element_by_xpath('.//span[@class="DyListCover-zone"]').text
            item['author'] = li.find_element_by_xpath('.//h2[@class="DyListCover-user"]').text
            item['popularity'] = li.find_element_by_xpath('.//span[@class="DyListCover-hot"]').text
            item['platform'] = '斗鱼TV'
            item['is_active'] = True
            item['last_active'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            item['subscribe'] = 1
            item['room_cover'] = li.find_element_by_xpath('.//img[@class="DyImg-content is-normal "]').get_attribute(
                'src')
            a = Douyu(room_number=item['room_number'], room_source=item['room_source'], room_title=item['room_title'],
                      room_category=item['room_category'], author=item['author'], popularity=item['popularity'],
                      platform=item['platform'], is_active=item['is_active'], last_active=item['last_active'],
                      subscribe=item['subscribe'], room_cover=item['room_cover'])
            rooms.append(a)

        next_url = self.driver.find_elements_by_xpath('//li[@class=" dy-Pagination-next"]')
        next_url = next_url[0] if len(next_url) > 0 else None
        return rooms, next_url

    def save_content_list(self, rooms):
        print(type(rooms))
        db.session.add_all(rooms)
        db.session.commit()

    def run(self):
        # 实现主要逻辑
        # 发送请求，获取响应
        self.driver.maximize_window()
        self.driver.get(self.start_rul)
        # 提取数据，提取下一页的元素
        rooms, next_url = self.get_room_list()
        self.save_content_list(rooms)
        page_count = 0
        while next_url is not None:
            next_url.click()
            rooms, next_url = self.get_room_list()
            self.save_content_list(rooms)
            page_count += 1
            print('the ' + str(page_count) + ' page')


class DouyuSpider(object):
    def __init__(self):
        self.start_rul = 'https://www.douyu.com/gapi/rkc/directory/0_0/'

    def get_room_list(self, url):
        time.sleep(2)
        rooms = []
        html = requests.get(url).text
        # 获取网页的json数据
        data = re.findall(r'\[{.*}\]', html)
        try:
            data = '{' + '"my_json":' + data[0] + '}'
        except Exception as e:
            return rooms
        room_list = json.loads(data)['my_json']
        for room in room_list:
            item = {}
            item['room_number'] = room['rid']
            item['room_source'] = 'https://www.douyu.com/' + str(room['rid'])
            item['room_title'] = str(room['rn'])
            item['room_category'] = str(room['c2name'])
            item['author'] = str(room['nn'])
            item['popularity'] = int(room['ol'])
            item['platform'] = '斗鱼TV'
            item['is_active'] = 1
            item['last_active'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            item['subscribe'] = 0
            item['room_cover'] = str(room['rs1'])
            a = Douyu(room_number=item['room_number'], room_source=item['room_source'], room_title=item['room_title'],
                      room_category=item['room_category'], author=item['author'], popularity=item['popularity'],
                      platform=item['platform'], is_active=item['is_active'], last_active=item['last_active'],
                      subscribe=item['subscribe'], room_cover=item['room_cover'])
            rooms.append(a)
        return rooms

    def save_content_list(self, all_rooms):
        # print(all_rooms)
        for room in all_rooms:
            try:
                db.session.add(room)
                db.session.commit()
                print('room '+str(room.room_number) + ' inserted!')
            except Exception as e:
                # print(e)
                db.session.rollback()
                # id = db.session.query(Douyu).filter(Douyu.room_number == room.room_number).first().id
                # db.session.query(Douyu).filter(Douyu.room_number == room.room_number).delete()
                db.session.query(Douyu).filter(Douyu.room_number == room.room_number).update(
                    {"room_source": room.room_source,
                     "room_title": room.room_title,
                     "room_category": room.room_category,
                     "popularity": room.popularity,
                     "is_active": room.is_active,
                     "last_active": room.last_active,
                     "room_cover": room.room_cover})
                db.session.commit()
                print('room '+str(room.room_number)+' updated!')

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


if __name__ == '__main__':
    douyu = DouyuSpider()
    douyu.run()
