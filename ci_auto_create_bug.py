from zentaohelper import ZentaoHelper
from datetime import datetime, timedelta
import argparse, os, sys, re

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='CI - Auto Create Bug')
  parser.add_argument('-s', '--host', type=str, required=True, help='Zentao Host')
  parser.add_argument('-u', '--username', type=str, required=True, help='User Name')
  parser.add_argument('-p', '--password', type=str, required=True, help='User Password')
  parser.add_argument('-i', '--item', type=str, required=True, help='JenKins Item')
  parser.add_argument('-l', '--log', type=str, required=True, help='JenKins Build Log File')
  args = vars(parser.parse_args())

  log_filename = args['log']
  # 读取上次缓存的分析结果
  cache_result_filename = "{item}_cache_warnings_result.log".format(item=args['item'])
  cache_result = ""
  if os.path.isfile(cache_result_filename):
    with open(cache_result_filename, 'r') as f:
      cache_result = f.read()
  if not os.path.isfile(log_filename):
    print('{cfg} not found'.format(cfg=log_filename))
    sys.exit(1)
  with open(log_filename, 'r') as f:
    content = f.readlines()
  # 从构建日志中提取告警和错误信息
  warnings = [x for x in content if re.findall(r'\(\d+\)\:\swarning', x)]
  errors = [x for x in content if re.findall(r'\(\d+\)\:\serror', x) or (": fatal error" in x)]
  
  log_result = ""
  if warnings:
    log_result += ("<strong>Warnings</strong>: <br />"+''.join(warnings)+"<br />")
  if errors:
    log_result += ("<strong>Errors</strong>: <br />"+''.join(errors))
  # 如果本次分析出的结果和上次一样，则不重新提BUG
  if cache_result == log_result:
    sys.exit(1)
  # 缓存构建结果到文件
  with open(cache_result_filename, 'w+') as f:
    f.write(log_result)

  if len(warnings) == 0 and len(errors) == 0:
    sys.exit(0)

  deadline = datetime.now() + timedelta(days=7)
  deadline = deadline.strftime("%Y-%m-%d")
  
  title = "【winserver2012】【CI】{item}每日构建({time})问题".format(item = args['item'], time=datetime.now().strftime("%Y-%m-%d"))
  if "linux" in title:
    title = "【centos6】【CI】{item}每日构建问题".format(item = args['item'])
  steps = "<p>[步骤]</p><p>CI - 每日构建({time})</p><p>[结果]</p><p>{result}</p><p>[期望]</p><p>0 error, 0 warning.</p>".format(time=datetime.now().strftime("%Y-%m-%d"), result=log_result)

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
    "title": title,
    "severity": 3,
    "pri": 3,
    "steps": steps
  })