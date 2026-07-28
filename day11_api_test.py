import requests

def safe_request(url:str,method: str = "GET", **kwargs) -> dict:
    try:
        r = requests.request(method, url, timeout=10, **kwargs)
        r.raise_for_status()
        try:
            data = r.json() #试着解析json
        except ValueError:
            data = None #解析不了，那就设为None, 不崩
        return{"success":True,"status_code":r.status_code, "data":data}
    except requests.exceptions.Timeout:
        return{"success":False,"error":"请求超时"}
    except requests.exceptions.HTTPError as e:
        return{"success":False,"error":f"HTTP错误:{e.response.status_code}"}
    except requests.exceptions.ConnectionError:
        return{"success":False,"error":"连接失败"}


#场景1 GET /get?name=test → 验证返回的 args 里有 name 字段

result = safe_request("https://httpbin.org/get",params={"name":"test"})
if result["success"] and result["data"]["args"]["name"] == "test" :
    print("场景1:[Pass]")
else:
    print("场景1:[Fail]")

#场景2 POST /post  →  验证发送的json原样返回
send_data ={"abc":"edf"}
result = safe_request("https://httpbin.org/post",method = "POST",json = send_data)
if result["success"] and result["data"]["json"] == send_data:
    print("场景2:[Pass]")
    print(f"{result['data']['json']}")
else:
    print("场景2:[Fail]")

#场景3 GET /status/200 → 验证状态码 200
result = safe_request("https://httpbin.org/status/200")
if result["success"] and result["status_code"] == 200:
    print("场景3:[Pass]")
else:
    print("场景3:[Fail]")

#场景4 GET /status/404  →  验证捕获到HTTP错误
result = safe_request("https://httpbin.org/status/404")
if not result["success"] and "HTTP错误" in result["error"]:
    print("场景4:[Pass]")
else:
    print("场景4:[Fail]")

#场景5 GET /delay/15  →  验证超时异常被捕获（timeout设为5秒）
result = safe_request("https://httpbin.org/delay/15",timeout=5)
if not result["success"] and "请求超时" in result["error"]:
    print("场景5:[Pass]")
else:
    print("场景5:[Fail]")