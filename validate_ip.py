# coding:utf-8
import threading
import urllib2
import os
import requests
import urlparse
import Queue
import random
from twisted.internet import reactor, task
from datetime import *
import lxml.html as H
import re
from db_manager import DBManager
from db_config import db_info
from get_outside_ip import GetIp


queue_without_limit = Queue.Queue()


class MyThread(threading.Thread):
    def __init__(self, func):
        super(MyThread, self).__init__()
        self.func = func

    def run(self):
        self.func()


def parse_url(url_to_parse):
    result = urlparse.urlparse(url_to_parse)
    host = result.netloc
    USER_AGENTS = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    ]

    header = {'Host': host,
              'User-Agent': random.choice(USER_AGENTS)
              }
    return header


def worker():
    while not queue_without_limit.empty():
        ip, url = queue_without_limit.get()
        test_ip(ip, url)
        queue_without_limit.task_done()


def test_ip(ip, url):
    headers = parse_url(url)
    local_ip = GetIp().get_ip()

    proxies = {"http": "http://%s" % ip.strip(), "https": "http://%s" % ip.strip()}
    try:
        check_ip_type = requests.get("http://httpbin.org/ip", proxies=proxies, timeout=2, allow_redirects=False)
        if check_ip_type.status_code == 200 and local_ip not in check_ip_type.content and 'html' not in check_ip_type.content:
            print check_ip_type.content
            content = requests.get(url, proxies=proxies, timeout=2, headers=headers)
            if content.status_code == 200 and '雪球，实时行情' in content.content:
                content_again = requests.get(url, proxies=proxies, timeout=2, headers=headers)
                if content_again.status_code == 200 and '雪球，实时行情' in content_again.content:
                    # print content_again.content
                    print ip
                ip_list.append(ip)
    except Exception:
        pass


def get_ip_from_66ip():
    api_url = 'http://www.66ip.cn/getzh.php?getzh=2016051141120&getnum=100&isp=1&anonymoustype=0&start=&ports=80%2C8080&export=&ipaddress=&area=1&proxytype=0&api=https'
    all_ip_list = []
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US;rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    proxy_support = urllib2.ProxyHandler(None)
    opener = urllib2.build_opener(proxy_support)
    urllib2.install_opener(opener)
    i_headers = {'User_Agent': user_agent}
    req = urllib2.Request(api_url, headers=i_headers)
    try:
        data = urllib2.urlopen(req).read()
        ip_list = data.split('<br>\n')
        for ip in ip_list:
            ip = ip.strip()
            ip = ip.replace('<br>', '')
            ip = str(ip.replace('\n', ', '))
            all_ip_list.append(ip)
        return all_ip_list
    except Exception as e:
        print str(e)


def get_ip_from_daili666():
    api_url = 'http://qsdrk.daili666api.com/ip/?tid=558465838696598&num=100&delay=5&foreign=none&ports=80,8080,3128'
    all_ip_list = []
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US;rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    proxy_support = urllib2.ProxyHandler(None)
    opener = urllib2.build_opener(proxy_support)
    urllib2.install_opener(opener)
    i_headers = {'User_Agent': user_agent}
    req = urllib2.Request(api_url, headers=i_headers)
    try:
        data = urllib2.urlopen(req).read()
        ip_port__list = data.split('\r\n')
        for ip_port in ip_port__list:
            # 将json中的IP信息存入all_IP_list
            all_ip_list.append(ip_port)
        return all_ip_list
    except Exception as e:
        print str(e)


def get_ip_from_ip002():
    api_url = 'http://www.ip002.com/api?order=1563356743683088&num=100&line=%E7%94%B5%E4%BF%A1&speed=%E5%BF%AB%E9%80%9F&port=80,8080'

    all_ip_list = []
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US;rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    proxy_support = urllib2.ProxyHandler(None)
    opener = urllib2.build_opener(proxy_support)
    urllib2.install_opener(opener)
    i_headers = {'User_Agent': user_agent}
    req = urllib2.Request(api_url, headers=i_headers)
    try:
        data = urllib2.urlopen(req).read()
        ip_list = data.split('\r\n')
        for ip in ip_list:
            all_ip_list.append(ip)
        return all_ip_list
    except Exception as e:
        print str(e)


def get_ip_from_youdaili():
    session = requests.session()
    header_guonei = {'Host': "www.youdaili.net",
                     'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0",
                     'Referer': "http://www.youdaili.net/Daili/guonei/"}

    header_webpage = {'Host': "www.youdaili.net",
                      'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0",
                      'Cookie': "Hm_lvt_f8bdd88d72441a9ad0f8c82db3113a84=1479697240; Hm_lpvt_f8bdd88d72441a9ad0f8c82db3113a84=1479697373"}

    url_orgin = 'http://www.youdaili.net/Daili/guonei'
    link_content = session.get(url_orgin, headers=header_guonei)
    doc = H.document_fromstring(link_content.text)
    link = doc.xpath('//div[@class="chunlist"]/ul/li[1]/p/a[1]')
    url = link[0].get('href')
    Ip_content = session.get(url, headers=header_guonei)
    doc_page_num = H.document_fromstring(Ip_content.text)
    try:
        page_num = doc_page_num.xpath('//ul[@class="pagelist"]/li[1]/a/text()')[0].encode('utf-8')
        page_nums = re.findall(r'\d+', page_num)
    except Exception:
        page_nums = ['1']

    for i in range(1, int(page_nums[0]) + 1):
        # 根据网页页数不同构建网址
        if i == 1:
            pagelink = url
        else:
            pagelink = url[:-5] + '_%s.html' % i
        # print 'The url is %s' % pagelink
        html = requests.get(pagelink, headers=header_webpage).text
        # 匹配IP
        ipss = re.findall(r'\d+\.\d+\.\d+\.\d+\:\d+', html)
    return ipss


def main(msg, thread_num=5, save_name="ips.txt"):
    global ip_list

    update_day = str(datetime.strftime(datetime.now(), "%Y-%m-%d"))

    ip_list = []
    threads = []

    url = msg["url"]

    thread_num = msg["thread_num"]

    print 'collecting ips......'
    ips = get_ip_from_ip002()
    ips.extend(get_ip_from_daili666())
    # ips.extend(get_ip_from_youdaili())

    print 'ips', len(ips)
    if ips:
        for ip in ips:
            queue_without_limit.put((ip, url))
        for i in range(thread_num):
            thread = MyThread(worker)
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
        queue_without_limit.join()

        filename = '%s_%s' % (update_day, save_name)
        print ip_list
        if len(ip_list):
            # try:
            #     os.remove(filename)
            # except:
            #     pass
            # finally:
            #     print "saving"
            #
            #     with open(filename, 'w+') as file_ip:
            #         ip_list = list(set(ip_list))
            #         for ip in ip_list:
            #             file_ip.write(ip + '\n')
            pass


if __name__ == '__main__':
    url = 'https://xueqiu.com'
    l = task.LoopingCall(main, {"url": url, "thread_num": 100})
    l.start(3600.0)
    reactor.run()
