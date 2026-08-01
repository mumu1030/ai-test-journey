import requests #导入requests库，发http请求用
import os 
from dotenv import load_dotenv #从.env文件加载配置
load_dotenv()

#======从环境变量取api key
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY") #从环境变量取key

#======函数定义
def call_llm(prompt:str,system:str = "你是一名资深的测试工程师") -> str: #定义函数，传参：问题、角色设定，不设就是默认；函数返回一个字符串
    headers = {
        "Authorization":f"Bearer {DEEPSEEK_API_KEY}", #身份证明
        "Content-Type" : "application/json", #告诉服务器我要发的是json
    }
    data = {
        "model":"deepseek-chat", #用哪个模型
        "messages":[
            {"role":"system","content":system}, #角色设定
            {"role":"user","content":prompt}, #你的问题
        ],
        "temperature":0.7, #创意值
    }
    r = requests.post("https://api.deepseek.com/chat/completions",headers=headers,json=data,timeout=30)
    r.raise_for_status() #如果返回4xx/5xx直接抛异常，不往下执行

    response_json = r.json()
    content = response_json["choices"][0]["message"]["content"]
    tokens = response_json["usage"]["total_tokens"]
    print(f"token消耗:{tokens}")
    return content

#测试调用
if __name__ == "__main__":
    result = call_llm("请为'用户注册'功能生成3条P0级测试用例,输出Markdown表格")
    print(result)
    with open("test_cases.md","w",encoding="utf-8") as f:
        f.write(result)