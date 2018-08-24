# _*_ coding:utf‐8 _*
import requests
from bs4 import BeautifulSoup
import os
import time
import datetime
import re
import random

se = requests.session()

class Pixiv():
    def __init__(self):
            self.base_url = 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index'
            self.login_url = 'https://accounts.pixiv.net/api/login?lang=zh'
            self.target_url = 'https://www.pixiv.net/ranking.php?mode=daily&content=illust&date='  #每日插画排行
            self.main_url = 'https://www.pixiv.net'
            self.headers = {
                'Referer': 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64)'
                              'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3514.0 Safari/537.36'
            }
            self.img_referer = 'https://www.pixiv.net/member_illust.php?mode=medium&illust_id='
            self.pixiv_id = 'xxxxxxx'
            self.password = '*******'
            self.post_key = []
            self.return_to = 'https://www.pixiv.net/'
            self.load_path = 'D:\xxx\xxx'
            self.ip_list = []
            self.ip_pool_url = 'http://xicidaili/nn/'

    def login(self):
        post_key_html = se.get(self.base_url, headers = self.headers).text
        post_key_soup = BeautifulSoup(post_key_html, 'lxml')
        self.post_key = post_key_soup.find('input')['value']  #  捕获post_key
        data = {
            'pixiv_id': self.pixiv_id,
            'password': self.password,
            'return_to': self.return_to,
            'post_key': self.post_key
        }
        se.post(self.login_url, data = data, headers = self.headers)

    def get_ip_list(self):
        html = requests.get(self.ip_pool_url, headers = self.headers)
        root_pattren = 'alt="Cn" /></td>([\d\D]*?)</tr>'
        root = re.findall(root_pattren, html.text)
        for i in range(len(root)):
            key = re.findall('<td>([\d\D]*?)</td>', root[i])
            self.ip_list.append(key[3].lower() + '://' + key[0] + ':' + key[1])
    
    def get_random_ip(self):
        self.get_ip_list()
        proxy = random.choice(self.ip_list)
        if 'https' in proxy:
            return {'https': proxy}
        else:
            return {'http': proxy}

    def get_html(self, url, timeout, proxy = None, num_entries = 5):
        if proxy is None:
            try:
                return se.get(url, headers = self.headers, timeout = timeout)
            except:
                if num_entries > 0:
                    print('获取网页出错,5秒后将会重新获取倒数第', num_entries, '次')
                    time.sleep(5)
                    return self.get_html(url, timeout, num_entries = num_entries - 1)
                else:
                    print('开始使用代理')
                    time.sleep(5)
                    ip = self.get_random_ip()
                    return self.get_html(url, timeout, proxy = ip)
        else:
            try:
                return se.get(url, headers = self.headers, proxies = proxy, timeout = timeout)
            except:
                if num_entries > 0:
                    print('正在更换代理,5秒后将会重新获取第', num_entries, '次')
                    time.sleep(5)
                    ip = self.get_random_ip()
                    return self.get_html(url, timeout, proxy = ip, num_entries = num_entries - 1)
                else:
                    print('使用代理失败,取消使用代理')
                    return self.get_html(url, timeout)

    def get_img(self, html, date):
        section_soup = BeautifulSoup(html, 'lxml')  # 传入日期date的html
        section_list = section_soup.find_all('section')   # 找到section
        for section in section_list:
            title = section['data-title']  #图片信息之标题
            name = section['data-user-name']  #图片信息之作者
            data_id = section['data-id']
            img_referer = self.img_referer + data_id  # 作为下载原图添加的referer
            href_temp = section.find('img')
            href = href_temp['data-src']  #由此改造成原图的地址
            url = href.replace('c/240x480/img-master', 'img-original').replace('_master1200', '')  #原图地址

            title = title.replace('?', '_').replace('/', '_').replace('\\', '_').replace('*', '_').replace('|', '_')\
                .replace('>', '_').replace('<', '_').replace(':', '_').replace('"', '_').strip()
            name = name.replace('?', '_').replace('/', '_').replace('\\', '_').replace('*', '_').replace('|', '_')\
                .replace('>', '_').replace('<', '_').replace(':', '_').replace('"', '_').strip()
            # 去掉那些不能在文件名里面的，加上strip()去掉换行
            save_name = title + '---' + name

            self.download_img(url, img_referer, date, save_name)  # 去下载这个图片

    def download_img(self, url, referer, date, save_name):
        headers = self.headers
        headers['Referer'] = referer  # 验证headers，主要是referer
        try:
            try:
                img = requests.get(url, headers = headers)
                total_size = int(img.headers['Content-Length'])
                if img.status_code == (404 or 403) :
                    img.raise_for_status()
                img_format = '.jpg'
            except:
                url = url.replace('jpg', 'png')
                img = requests.get(url, headers = headers)
                total_size = int(img.headers['Content-Length'])
                img_format = '.png'
        except:
            print('获取图片失败')
            return False

        if os.path.exists(os.path.join(self.load_path, date, save_name + img_format)):
            for i in range(1, 100):  # 如果重名就加上一个数字
                if not os.path.exists(os.path.join(self.load_path, date, save_name + str(i) + img_format)):
                    save_name = save_name + str(i)
                    break
        print('正在保存名为: ' + save_name + ' 的图片')
        temp_size = 0
        with open(save_name + img_format, 'wb') as f:
            for chunk in img.iter_content(chunk_size=1024):
                if chunk:
                    temp_size += len(chunk)
                    f.write(chunk)
                    f.flush()
                    done = int(50 * temp_size / total_size)
                    sys.stdout.write("\r|%s%s| %d%%" % ('█' * done, ' ' * (50 - done), 100 * temp_size / total_size))
                    sys.stdout.flush()
            f.close()
        print('\n该图片保存完毕')

    def mkdir(self, date):
        is_exist = os.path.exists(os.path.join(self.load_path, date))
        if not is_exist:
            print('创建名为' + date + '的文件夹')
            os.makedirs(os.path.join(self.load_path, date))
            os.chdir(os.path.join(self.load_path, date))
            return True
        else:
            print('名为' + date + '的文件夹已经存在')
            os.chdir(os.path.join(self.load_path, date))
            return False
    def mkdir(self, date):
        is_exist = os.path.exists(os.path.join(self.load_path, date))
        if not is_exist:
            print('创建名为' + date + '的文件夹')
            os.makedirs(os.path.join(self.load_path, date))
            os.chdir(os.path.join(self.load_path, date))
            return True
        else:
            print('名为' + date + '的文件夹已经存在')
            os.chdir(os.path.join(self.load_path, date))
            return False

    def work(self):
        self.login()
        for i in range(1, 6):  # 跑5页
            date = (datetime.date.today() + datetime.timedelta(days = - i)).strftime('%Y%m%d')  #设定每日插画排行网页的日期
            self.mkdir(date)  # 创建文件夹,每一天就开一个文件夹
            now_html = self.get_html(self.target_url + date, 3)  # 获取网页
            self.get_img(now_html.text, date)  # 获取图片
            print('于' + date + '的图片保存完毕')
            time.sleep(2)  # 防止太快被反


pixiv = Pixiv()
pixiv.work()