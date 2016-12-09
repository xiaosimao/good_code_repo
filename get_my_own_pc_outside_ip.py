# coding:utf-8
import re
import requests


class GetIp(object):
    def __init__(self, test_url_1="http://httpbin.org/ip",
                 test_url_2="http://www.ip.cn/"):
        self.test_url_1 = test_url_1
        self.test_url_2 = test_url_2

    def get_ip(self):
        try:
            myip = self.request(self.test_url_1)
        except:
            try:
                myip = self.request(self.test_url_2)
            except:
                myip = "So sorry!!!"
        return myip

    def request(self, url):
        req = requests.get(url)
        if url == req.url:
            result = req.content
        return re.search('\d+\.\d+\.\d+\.\d+', result).group(0)


if __name__ == "__main__":
    get_ip = GetIp()
    print getip.getip()
