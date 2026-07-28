import requests

# ==========================================================
# ① GET 请求 —— 从服务器“拿”数据
# 参数：想带什么查询条件去请求服务器
# params 会被自动拼到 URL 后面，变成 ?feature=login&count=5
params = {"feature": "login", "count": 5}

r = requests.get("https://httpbin.org/get", params=params)

print("=" * 40)
print("GET 请求结果")
print(f"  状态码: {r.status_code}")     # 200 = 成功，404 = 找不到，500 = 服务器崩了
print(f"  URL: {r.url}")                # 你实际请求的那条 URL，包含 params
print(f"  响应体: {r.json()}")            # 服务器返回的数据，转成 Python 字典
print()

# ==========================================================
# ② POST 请求 —— 给服务器“塞”数据
# ==========================================================

data = {
    "username": "test_user",
    "action": "login",
    "platform": "Android"
}

r = requests.post("https://httpbin.org/post", json=data)

print("=" * 40)
print("POST 请求结果")
print(f"  状态码: {r.status_code}")
print(f"  服务器收到的 json: {r.json()['json']}")  # 看看服务器返回什么
print()

# ==========================================================
# ③ 请求头（Headers）—— 告诉服务器你是谁
# ==========================================================

headers = {
    "Content-Type": "application/json",   # 告诉服务器：我发的是 JSON 格式
    "User-Agent": "TestBot/1.0"          # 告诉服务器：我是 TestBot 机器人
}

r = requests.get("https://httpbin.org/headers", headers=headers)

print("=" * 40)
print("Headers 请求结果")
print(f"  服务器收到的 headers: {r.json()['headers']}")
print()
