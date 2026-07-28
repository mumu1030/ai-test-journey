import requests

# ===== get 请求 =====
r = requests.get("https://httpbin.org/get", params={"feature": "login", "count": 5})
print(f"GET 状态码: {r.status_code}")
print(f"URL: {r.url}")
print(f"response: {r.json()}")

# ===== POST 请求 =====
data = {"username": "test_user", "action": "login", "platform": "Android"}
r = requests.post("https://httpbin.org/post", json=data)
print(f"\nPOST 状态码: {r.status_code}")
print(f"发送的数据: {r.json()['json']}")

#=====请求头======
headers = {"Content-Type":"application/json","User-Agent":"TestBot/1.0"}
r = requests.get("https://httpbin.org/headers",headers=headers)
print(f"服务器收到的 headers:{r.json()['headers']}")

#======异常处理=====

def safe_request(url:str,method: str = "GET", **kwargs) -> dict:
    try:
        r = requests.request(method, url, timeout=10, **kwargs)
        r.raise_for_status()
        return{"success":True,"status_code":r.status_code,"data":r.json()}
    except requests.exceptions.Timeout:
        return{"success":False,"error":"请求超时"}
    except requests.exceptions.HTTPError as e:
        return{"success":False,"error":f"HTTP错误:{e.response.status_code}"}
    except requests.exceptions.ConnectionError:
        return{"success":False,"error":"连接失败"}
print(safe_request("https://httpbin.org/get"))
print(safe_request("https://httpbin.org/status/404"))
print(safe_request("https://httpbin.org/status/500"))