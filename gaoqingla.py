from bs4 import BeautifulSoup
import urllib.request
import re
import mysql.connector


class Gaoqing(object):
    def __init__(self, url, page):
        self.url = url
        self.page = page

    # 获得所有电影的url
    def get_page_url(self):
        movie_url = []
        data = urllib.request.urlopen(self.url + str(self.page)).read()
        content = data.decode('utf-8')
        soup = BeautifulSoup(content, 'html.parser')
        tag = soup.find_all(class_="article")
        for link in tag:
            single_url = link.find_all('a')
            for movie in single_url:
                movie_url.append(movie.get('href'))
        print('所有电影链接下载完毕...')
        return movie_url

    # 得到电影的属性信息区域
    def page_detail(self, movie_url):
        info_area = []
        number = len(movie_url)
        print('得到所有电影链接')
        for i, url in enumerate(movie_url):
            print('正在分析第 %s 个电影' % str(i+1))
            data = urllib.request.urlopen(url).read()
            content = data.decode('utf-8')
            soup = BeautifulSoup(content, 'html.parser')
            list = soup.find(id="post_content").find_all('span')
            info_area.append(list)
        print('电影信息区域解析完毕...')
        return info_area

    # 获取电影属性信息并将其存入数据库
    def get_data(self, info_area):
        conn = mysql.connector.connect(user='root', password='newlife!', database='test')
        cursor = conn.cursor()
        print('数据库已连接...')
        if self.page == 1:
            cursor.execute('create table movie(id int(5) primary key auto_increment,'
                           ' translated_name varchar(256), movie_name varchar(256),'
                           ' movie_date varchar(256), movie_country varchar(256),'
                           ' movie_type varchar(256), movie_time varchar(256),'
                           ' movie_director varchar(1024), movie_actor varchar(1024))')
            print('数据表创建完毕...')
        for x in info_area:
            for one in x:
                single = one.get_text()
                dataset = re.findall('.*?◎[^\x00-\xff]..[^\x00-\xff].(.*)', single, re.S)
                re_single = re.findall('.*?◎([^\x00-\xff]..[^\x00-\xff]).*?', single, re.S)
                str_translated = ''.join(re_single)
                if str_translated == '译　　名':
                    translated_name = ''.join(dataset)
                elif str_translated == '片　　名':
                    movie_name = ''.join(dataset)
                elif str_translated == '年　　代':
                    movie_date = ''.join(dataset)
                elif str_translated == '国　　家':
                    movie_country = ''.join(dataset)
                elif str_translated == '类　　别':
                    movie_type = ''.join(dataset)
                elif str_translated == '片　　长':
                    movie_time = ''.join(dataset)
                elif str_translated == '导　　演':
                    movie_director = ''.join(dataset)
                elif str_translated == '主　　演':
                    movie_actor = ''.join(dataset)

            sql = 'insert into movie (translated_name, movie_name, movie_date,' \
                  ' movie_country, movie_type, movie_time,movie_director,'\
                  ' movie_actor) values (%s, %s, %s, %s, %s, %s, %s, %s)'
            try:
                cursor.execute(sql, [translated_name, movie_name, movie_date, movie_country,
                                     movie_type, movie_time, movie_director, movie_actor])
                conn.commit()
                print('开始下一个电影存储...')
            except UnboundLocalError:
                pass
            except TimeoutError:
                pass
        conn.close()
        print('开始第%s页电影存储' % str(self.page+1))

url = 'http://gaoqing.la/720p/page/'
page = 2
while page <= 94:
    gaoqing = Gaoqing(url, page)
    a = gaoqing.page_detail(gaoqing.get_page_url())
    gaoqing.get_data(a)
    page += 1
