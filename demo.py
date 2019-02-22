'''
@File: demo.py
@Author: leon.li(l2m2lq@gmail.com)
@Date: 2019-02-22 14:22:38
'''

from zentaohelper import ZentaoHelper

if __name__ == "__main__":
  zentao = ZentaoHelper("host:port")
  zentao.login("Username", "Password")
  zentao.create_bug({
    "product": 84,
    "module": 523,
    "project": 88,
    "openedBuild[]": "trunk",
    "assignedTo": "Leon",
    "deadline": "2019-02-28",
    "type": "codeerror",
    "title": "【win】【CI】自动创建BUG测试5",
    "severity": 3,
    "pri": 3,
    "steps": """<p>[步骤]</p>
    <p>1. 步骤1</p>
    <p>2. 步骤2</p>
    <p>3. 步骤3</p>
    <p>[结果]</p>
    <p>这是结果</p>
    <p>[期望]</p>
    <p>这是期望</p>
    """
  })