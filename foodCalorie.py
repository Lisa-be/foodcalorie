from gevent import monkey
monkey.patch_all() #让程序变成异步模式
import gevent
import requests
import bs4
import csv
from gevent.queue import Queue

csv_file = open('boohee.csv', 'w', encoding='utf-8-sig', newline='')
writer = csv.writer(csv_file)
writer.writerow(['食物', '热量', '链接'])

work = Queue()
url_1 = 'http://www.boohee.com/food/group/{type}?page={page}'
for x in range(1, 4):
    for y in range(1, 4):
        real_url = url_1.format(type=x, page=y)
        work.put_nowait(real_url) #

url_2 = 'http://www.boohee.com/food/view_menu?page={page}'
for x in range(1, 4):
    real_url = url_2.format(page=x)
    work.put_nowait(real_url)

def crawler():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
    }
    while not work.empty():
        url = work.get_nowait()
        res = requests.get(url, headers=headers)
        bs_res = bs4.BeautifulSoup(res.text, "html.parser")
        foods = bs_res.find_all('li', class_='item clearfix')
        for food in foods:
            food_name = food.find_all('a')[1]['title']
            food_url = 'http://www.boohee.com' + food.find_all('a')[1]['href']
            food_calorie = food.find('p').text
            writer.writerow([food_name, food_calorie, food_url])
            print(food_name)


tasks_list = []
for x in range(5):
    task = gevent.spawn(crawler)
    tasks_list.append(task)
gevent.joinall(tasks_list)


