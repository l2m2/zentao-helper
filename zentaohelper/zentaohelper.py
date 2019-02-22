'''
@File: zentaohelper.py
@Author: leon.li(l2m2lq@gmail.com)
@Date: 2019-02-22 11:34:40
'''

import requests
import string
import random

class ZentaoHelper:
  """
  禅道助手
  """

  def __init__(self, host):
    self._host = host
    self._headers = {
      "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
      "Accept-Encoding": "gzip, deflate",
      "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
      "Cache-Control": "max-age=0",
      "Connection": "keep-alive",
      "Host": self._host,
      "Upgrade-Insecure-Requests": "1",
      "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    }
    self._session = requests.Session()

  def _rand_chars(self, length=12, allow_chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(allow_chars) for i in range(length))
    
  def login(self, account, password):
    headers = self._headers
    headers["Referer"] = "http://{host}/zentao/user-login.html".format(host = self._host)
    post_data = {
      "account": account,
      "password": password,
      "referer": "http://{host}//zentao/my/".format(host=self._host)
    }
    try:
      r = self._session.post("http://{host}/zentao/user-login.html".format(host = self._host), headers=headers,data=post_data)
      r.raise_for_status()
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
      print("Cannot connect to server.")
    except requests.exceptions.HTTPError:
      print("4xx, 5xx")
    else:
      print('Login successful.')

  def create_bug(self, bug):
    if not self._session.cookies:
      print("please call login() first.")
      return
    headers = self._headers
    headers["Referer"] = "http://{host}/zentao/bug-browse-{product}.html".format(host = self._host, product = bug['product'])
    post_data = bug
    post_data['uid'] = self._rand_chars(13, string.digits+string.ascii_lowercase)
    print(post_data)
    try:
      url = "http://{host}/zentao/bug-create-{product}-0-moduleID=0.html".format(host = self._host, product = bug['product'])
      r = self._session.post(url, headers=headers,data=post_data)
      print(r)
      r.raise_for_status()
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
      print("Cannot connect to server.")
    except requests.exceptions.HTTPError:
      print("4xx, 5xx")
    else:
      print('Create bug successful.')
    
  def create_sprint_build(self):
    print("Not yet implemented.")

  def close_session(self):
    self._session.close()