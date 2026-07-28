#导入标准库
import os,json,random
from datetime import datetime
from pathlib import Path
import requests

print(os.getcwd()) #当前目录
print(datetime.now().isoformat()) #当前时间


r = requests.get("https://httpbin.org/get")
print(r.status_code)