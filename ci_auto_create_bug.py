from zentaohelper import ZentaoHelper
from datetime import datetime, timedelta
import argparse

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='CI - Auto Create Bug')
  parser.add_argument('-s', '--host', type=str, required=True, help='Zentao Host')
  parser.add_argument('-u', '--username', type=str, required=True, help='User Name')
  parser.add_argument('-p', '--password', type=str, required=True, help='User Password')
  parser.add_argument('-t', '--title', type=str, required=True, help='Bug Title')
  parser.add_argument('-w', '--warnings', type=str, required=True, help='Bug Steps')
  args = vars(parser.parse_args())
  
  deadline = datetime.now() + timedelta(days=7)
  deadline = deadline.strftime("%Y-%m-%d")
  steps = "<p>[步骤]</p><p>CI - 每日构建</p><p>[结果]</p><p>{warnings}</p><p>[期望]</p><p>0 error, 0 warning.</p>".format(warnings=args['warnings'])

  zentao = ZentaoHelper(args['host'])
  zentao.login(args['username'], args['password'])
  zentao.create_bug({
    "product": 84,
    "module": 523,
    "project": 88,
    "openedBuild[]": "trunk",
    "assignedTo": "Leon",
    "deadline": deadline,
    "type": "codeerror",
    "title": args['title'],
    "severity": 3,
    "pri": 3,
    "steps": steps
  })